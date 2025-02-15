from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import os
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        pdf_reader = PdfReader(pdf_path)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {e}")


def split_text_into_chunks(text, chunk_size=1000, chunk_overlap=200):
    """Splits text into manageable chunks."""
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return text_splitter.split_text(text)


def create_embeddings_and_knowledge_base(chunks):
    """Creates embeddings and a vector knowledge base."""
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    return knowledge_base


def get_answer_from_question(knowledge_base, user_question):
    """Retrieves an answer from the knowledge base using the question."""
    docs = knowledge_base.similarity_search(user_question)
    llm = OpenAI()
    chain = load_qa_chain(llm, chain_type="stuff")
    with get_openai_callback() as cb:
        response = chain.run(input_documents=docs, question=user_question)
        print("API Call Info:", cb)
    return response


def save_response_to_markdown(question, response):
    """Saves the question and response to a Markdown file."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"response_{timestamp}.md"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"# Question\n{question}\n\n# Answer\n{response}\n")
    print(f"Response saved as: {filename}")


def main():
    print("=== Ask Your PDF CLI ===")
    pdf_path = input("Enter the path to the PDF file: ").strip()

    if not os.path.exists(pdf_path):
        print("Error: PDF file not found. Please check the path and try again.")
        return

    try:
        # Extract text from PDF
        print("Extracting text from PDF...")
        text = extract_text_from_pdf(pdf_path)

        # Split text into chunks
        print("Splitting text into manageable chunks...")
        chunks = split_text_into_chunks(text)

        if not chunks:
            print("No text chunks were extracted from the PDF. Exiting.")
            return

        # Create embeddings and knowledge base
        print("Creating embeddings and knowledge base...")
        knowledge_base = create_embeddings_and_knowledge_base(chunks)

        # Ask user for a question
        while True:
            user_question = input("Enter your question about the PDF (or type 'exit' to quit): ").strip()
            if user_question.lower() == "exit":
                print("Exiting program. Goodbye!")
                break

            # Get answer to the question
            print("Retrieving answer from the PDF...")
            response = get_answer_from_question(knowledge_base, user_question)

            # Display and save response
            print("\n=== Answer ===")
            print(response)
            save_response_to_markdown(user_question, response)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
