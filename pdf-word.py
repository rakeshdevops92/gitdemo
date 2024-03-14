import os
import fitz  # PyMuPDF
import docx
from openai import AzureOpenAI

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Function to extract text from a Word document
def extract_text_from_word(doc_path):
    doc = docx.Document(doc_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Function to determine the document type and extract text accordingly
def extract_text(doc_path):
    if doc_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(doc_path)
    elif doc_path.lower().endswith('.docx'):
        return extract_text_from_word(doc_path)
    else:
        raise ValueError("Unsupported file type. Please provide a PDF or Word document.")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key="28ccd7f614334fc28bbb2d77b1d3eb06",
    api_version="2024-02-01",
    azure_endpoint="https://hackathonuser285.openai.azure.com"
)

# Input for PDF or Word document path
doc_path = input("Enter the path to your PDF or Word document: ")

# Extract text from the document
doc_text = extract_text(doc_path)

# Prepare the conversation with the extracted document text
conversation = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": doc_text}
]

# Input for question
question = input("What question would you like to ask about the document? ")

# Append the question to the conversation
conversation.append({"role": "user", "content": question})

# Request a completion from the deployed model
response = client.chat.completions.create(
    model="Hackathon285DeployModel",  # Use your deployed model name
    messages=conversation
)

# Print the model's response
print(response.choices[0].message.content)
