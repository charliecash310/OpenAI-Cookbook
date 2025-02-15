def split_text_into_chunks(text, max_size=4000):
    """ Split text into smaller chunks to fit OpenAI token limits. """
    return [text[i:i+max_size] for i in range(0, len(text), max_size)]

with open("otx_threat_data.json", "r", encoding="utf-8") as file:
    raw_text = file.read()  # Read full file as text

chunks = split_text_into_chunks(raw_text)

for idx, chunk in enumerate(chunks):
    chunk_file = f"split_otx_chunk_{idx+1}.txt"
    with open(chunk_file, "w", encoding="utf-8") as output:
        output.write(chunk)
    print(f"Saved: {chunk_file}")
