import asyncio
import openai
import os
import socket
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# OpenAI API Key (Environment Variable Required)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to interact with ChatGPT
async def call_gpt(prompt):
    try:
        messages = [
            {"role": "system", "content": "You are a cybersecurity SOC analyst with more than 25 years of experience."},
            {"role": "user", "content": prompt}
        ]
        client = openai.OpenAI()
        response = await asyncio.to_thread(client.chat.completions.create,
                                           model="gpt-3.5-turbo",
                                           messages=messages,
                                           max_tokens=2048,
                                           temperature=0.7)
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error in OpenAI API call: {e}")
        return None

# Asynchronous function to handle incoming syslog messages
async def handle_syslog():
    UDP_IP = "0.0.0.0"
    UDP_PORT = 514

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    logging.info(f"Syslog listener started on UDP {UDP_PORT}")

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            log_entry = data.decode("utf-8").strip()
            logging.info(f"Received log from {addr}: {log_entry}")

            # Call GPT asynchronously
            analysis_result = await call_gpt(
                f"Analyze the following log entry for potential threats: {log_entry} \n\n"
                "If you believe there may be suspicious activity, start your response with 'Suspicious Activity: ' "
                "and then your analysis. Provide nothing else."
            )

            if analysis_result and "Suspicious Activity" in analysis_result:
                logging.warning(f"Alert: {analysis_result}")

        except Exception as e:
            logging.error(f"Syslog processing error: {e}")

        await asyncio.sleep(0.1)  # Small delay for cooperative multitasking

# Class to handle file system events
class LogWatcher:
    DIRECTORY_TO_WATCH = "/var/log/custom_logs"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = LogHandler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        logging.info(f"Watching directory: {self.DIRECTORY_TO_WATCH}")
        try:
            while True:
                asyncio.sleep(1)  # Keeps the observer running
        except KeyboardInterrupt:
            self.observer.stop()
            logging.info("Stopping log watcher.")

        self.observer.join()

class LogHandler(FileSystemEventHandler):
    async def process(self, event):
        if event.is_directory:
            return

        if event.event_type == "created":
            logging.info(f"New log file detected: {event.src_path}")
            await self.analyze_log(event.src_path)

    async def analyze_log(self, file_path):
        try:
            async with aiofiles.open(file_path, "r") as file:
                async for line in file:
                    analysis_result = await call_gpt(
                        f"Analyze the following log entry for potential threats: {line.strip()} \n\n"
                        "If you believe there may be suspicious activity, start your response with 'Suspicious Activity: ' "
                        "and then your analysis. Provide nothing else."
                    )

                    if analysis_result and "Suspicious Activity" in analysis_result:
                        logging.warning(f"Alert: {analysis_result}")

        except Exception as e:
            logging.error(f"Error reading log file {file_path}: {e}")

    def on_created(self, event):
        asyncio.create_task(self.process(event))

# Main function to run syslog listener and file watcher together
async def main():
    syslog_task = asyncio.create_task(handle_syslog())
    watcher = LogWatcher()
    watcher.run()

    await syslog_task  # Keeps script running

if __name__ == "__main__":
    asyncio.run(main())
