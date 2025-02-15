import os
import subprocess
import hashlib
import datetime

# Create a unique log file
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"incident_response_log_{timestamp}.txt"

def run_command(command):
    """Runs a system command and returns the output."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error running command {command}: {str(e)}"

def get_system_logs():
    """Collects system logs (auth, syslog) for anomalies."""
    logs = {
        "auth.log": run_command("tail -n 50 /var/log/auth.log"),
        "syslog": run_command("tail -n 50 /var/log/syslog")
    }
    return logs

def get_network_connections():
    """Checks active network connections and listening ports."""
    return run_command("netstat -tulnp")

def get_running_processes():
    """Lists all running processes."""
    return run_command("ps aux --sort=-%mem | head -n 20")

def get_suspicious_files():
    """Finds recently modified files (last 24 hours) for investigation."""
    return run_command("find / -type f -mtime -1 2>/dev/null")

def get_file_hashes(file_paths):
    """Computes SHA256 hashes of given files."""
    hashes = {}
    for file in file_paths:
        try:
            with open(file, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            hashes[file] = file_hash
        except Exception:
            hashes[file] = "Error reading file"
    return hashes

def collect_incident_data():
    """Runs all incident response checks and writes results to a log file."""
    data = {
        "System Logs": get_system_logs(),
        "Network Connections": get_network_connections(),
        "Running Processes": get_running_processes(),
        "Recent File Modifications": get_suspicious_files()
    }
    
    # Write results to file
    with open(log_filename, "w") as log_file:
        log_file.write(f"=== Incident Response Log ({timestamp}) ===\n\n")
        for section, content in data.items():
            log_file.write(f"--- {section} ---\n")
            if isinstance(content, dict):
                for key, value in content.items():
                    log_file.write(f"[{key}]\n{value}\n\n")
            else:
                log_file.write(content + "\n\n")
    
    print(f"Incident response log saved as {log_filename}")

if __name__ == "__main__":
    collect_incident_data()
