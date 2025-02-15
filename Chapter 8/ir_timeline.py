import openai
import re
import os
import numpy as np
import faiss

# Ensure API key is set globally
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_raw_log_to_json(raw_log_path):
    """Parses a raw log file and converts it into a JSON format."""
    timestamp_regex = r'\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\]'
    event_regex = r'Event: (.+)'
    json_data = []
    
    with open(raw_log_path, 'r') as file:
        for line in file:
            timestamp_match = re.search(timestamp_regex, line)
            event_match = re.search(event_regex, line)
            if timestamp_match and event_match:
                timestamp = timestamp_match.group().strip('[]')
                event_description = event_match.group(1)
                json_data.append({"Timestamp": timestamp, "Event": event_description})
    
    return json_data

def get_embeddings(texts):
    """Retrieves embeddings for a list of text inputs."""
    embeddings = []
    
    for text in texts:
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        
        # Extract embeddings correctly
        embedding = response["data"][0]["embedding"]
        embeddings.append(embedding)
    
    return np.array(embeddings, dtype=np.float32)

def create_faiss_index(embeddings):
    """Creates a FAISS index for a given set of embeddings."""
    d = embeddings.shape[1]  # Dimensionality of embeddings
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    return index

def analyze_logs_with_embeddings(log_data):
    """Analyzes logs by comparing log event embeddings to predefined templates."""
    suspicious_templates = [
        "Unauthorized access attempt detected",
        "Multiple failed login attempts"
    ]
    normal_templates = [
        "User logged in successfully",
        "System health check completed"
    ]
    
    # Get embeddings for templates
    suspicious_embeddings = get_embeddings(suspicious_templates)
    normal_embeddings = get_embeddings(normal_templates)
    
    # Combine embeddings and create FAISS index
    template_embeddings = np.vstack((suspicious_embeddings, normal_embeddings))
    index = create_faiss_index(template_embeddings)
    
    # Labels for classification
    labels = ['Suspicious'] * len(suspicious_embeddings) + ['Normal'] * len(normal_embeddings)
    
    categorized_events = []
    
    for entry in log_data:
        log_embedding = get_embeddings([entry["Event"]])
        _, indices = index.search(log_embedding, 1)  # Find nearest neighbor
        category = labels[indices[0][0]]
        categorized_events.append((entry["Timestamp"], entry["Event"], category))
    
    return categorized_events

# Sample log file path
raw_log_file_path = 'suricata.log'

# Parse log data
log_data = parse_raw_log_to_json(raw_log_file_path)

# Analyze logs
categorized_timeline = analyze_logs_with_embeddings(log_data)

# Print categorized results
for timestamp, event, category in categorized_timeline:
    print(f"{timestamp} - {event} - {category}")
