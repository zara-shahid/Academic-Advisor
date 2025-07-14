import gradio as gr
import os
import faiss
import numpy as np
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from groq import Groq

# Load Groq API Key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Please set the GROQ_API_KEY as a secret/environment variable in the Hugging Face Space.")

groq_client = Groq(api_key=GROQ_API_KEY)

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Templates
SYSTEM_TEMPLATE = (
    "You are a helpful academic supervisor who helps a student understand their paper and answer questions based only on the document."
)
USER_TEMPLATE = (
    "Based on the provided document, answer the following question:\n\n{context}\n\nQuestion: {question}\n\nAnswer:"
)

# Globals
faiss_index = None
stored_chunks = []
dimension = 384  # embedding size

# PDF to text
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text if text.strip() else None

# Chunk text
def chunk_text(text, chunk_size=500):
    sentences = text.split(". ")
    chunks, current_chunk = [], ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# Upload & index
def upload_and_index(pdf):
    global faiss_index, stored_chunks
    if pdf is None:
        return "❌ No PDF uploaded. Please upload a file."

    try:
        text = extract_text_from_pdf(pdf.name)

        if text is None:
            return "❌ Failed to extract text. PDF may be scanned or empty."

        chunks = chunk_text(text)
        if not chunks:
            return "❌ Failed to split text into chunks."

        embeddings = embedder.encode(chunks)

        faiss_index = faiss.IndexFlatL2(dimension)
        stored_chunks.clear()
        stored_chunks.extend(chunks)
        faiss_index.add(np.array(embeddings, dtype=np.float32))

        return "✅ Document indexed successfully! You can now ask questions."
    except Exception as e:
        return f"❌ Error during upload/indexing: {e}"

# Answer question
def answer_question(question):
    global faiss_index, stored_chunks
    if faiss_index is None or faiss_index.ntotal == 0:
        return "❌ Please upload & index a document first."

    try:
        q_embedding = embedder.encode([question])
        distances, indices = faiss_index.search(np.array(q_embedding, dtype=np.float32), k=3)

        context = "\n\n".join(
            [stored_chunks[idx] for idx in indices[0] if idx < len(stored_chunks)]
        )

        if not context:
            return "❌ Could not find relevant context."

        prompt = USER_TEMPLATE.format(context=context, question=question)

        chat_completion = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": SYSTEM_TEMPLATE},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=512
        )

        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error while answering: {e}"

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## 📚 Academic Supervisor — Upload Paper & Ask Questions")
    with gr.Row():
        with gr.Column():
            pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
            upload_btn = gr.Button("Upload & Index")
            upload_output = gr.Textbox(label="Status")
        with gr.Column():
            question_input = gr.Textbox(label="Your Question")
            ask_btn = gr.Button("Get Answer")
            answer_output = gr.Textbox(label="Answer")

    upload_btn.click(upload_and_index, inputs=pdf_input, outputs=upload_output)
    ask_btn.click(answer_question, inputs=question_input, outputs=answer_output)

demo.launch()
