import openai
import os

# Set up the OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the structure of the documents
design_doc_structure = [
    "Introduction",
    "Software Architecture",
    "Function Descriptions",
    "Flow Diagrams"
]

user_guide_structure = [
    "Introduction",
    "Installation Guide",
    "Usage Guide",
    "Troubleshooting"
]

def generate_section_content(section_title: str, source_code: str) -> str:
    """
    Generates the content for a specific section by sending a request to the OpenAI API.
    """
    messages = [
        {"role": "system", "content": f"You are an experienced software engineer with extensive knowledge in writing {section_title} sections for design documents."},
        {"role": "user", "content": f"Please generate a {section_title} section for the following Python code:\n\n{source_code}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2048,
        n=1,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()

def write_to_text_file(file_path: str, title: str, content: str):
    """
    Writes a section title and its content to a text file.
    """
    with open(file_path, 'a') as file:
        file.write(f"# {title}\n\n")
        file.write(content + "\n\n")

# Main script
if __name__ == "__main__":
    # Load the source code
    try:
        with open('source_code.py', 'r') as file:
            source_code = file.read()
    except FileNotFoundError:
        print("Error: The file 'source_code.py' was not found.")
        exit(1)

    # Create the design document as a text file
    design_doc_path = 'DesignDocument.txt'
    with open(design_doc_path, 'w') as file:
        file.write("Design Document\n\n")  # Add a title to the document

    for section in design_doc_structure:
        section_content = generate_section_content(section, source_code)
        write_to_text_file(design_doc_path, section, section_content)

    print(f"Design document saved to {design_doc_path}")

    # Create the user guide as a text file
    user_guide_path = 'UserGuide.txt'
    with open(user_guide_path, 'w') as file:
        file.write("User Guide\n\n")  # Add a title to the document

    for section in user_guide_structure:
        section_content = generate_section_content(section, source_code)
        write_to_text_file(user_guide_path, section, section_content)

    print(f"User guide saved to {user_guide_path}")
