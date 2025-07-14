## 📚 Academic Supervisor — RAG App

An academic supervisor web app that lets you upload a PDF, retrieves relevant information from it using embeddings + FAISS, and answers your questions using LLaMA3 (via Groq).  

✅ Upload your academic paper (PDF)  
✅ Index and chunk it intelligently  
✅ Ask questions about the document  
✅ Get helpful, context-aware answers  

---

## 🚀 Features

- 🔗 **RAG (Retrieval-Augmented Generation):** Combines document retrieval with LLM generation.
- 📄 Upload and process PDF files.
- 🪄 Automatically chunks and indexes text using Sentence Transformers & FAISS.
- 🤖 Answers questions based only on your document using Groq LLaMA3.
- 🌐 Gradio-powered web interface.

---

## 🛠️ Tech Stack

- [Gradio](https://gradio.app/) — UI
- [Sentence Transformers](https://www.sbert.net/) — embeddings
- [FAISS](https://faiss.ai/) — vector store
- [Groq](https://console.groq.com/) — LLaMA3 LLM
- [PyPDF2](https://pypi.org/project/PyPDF2/) — PDF parsing

---

## 📦 Installation & Running Locally

### 1️⃣ Clone this repository:
```bash
git clone https://github.com/zara-shahid/Academic-Supervisor.git
cd Academic-Supervisor
2️⃣ Install dependencies:

pip install -r requirements.txt
3️⃣ Set your Groq API key:
You can export it as an environment variable:

export GROQ_API_KEY=your_actual_groq_api_key
Or you can modify app.py and replace:

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
with:

GROQ_API_KEY = "your_actual_groq_api_key"
4️⃣ Run the app:

python app.py
Open the Gradio link printed in the terminal.

🌟 Deployment
🚀 On Hugging Face Spaces:
You can deploy this app to Hugging Face Spaces:

Create a new Gradio Space.

Upload these files:

app.py

requirements.txt

README.md

Add your Groq API key as a secret in the Space settings:

Name: GROQ_API_KEY
Value: your_actual_groq_api_key
The Space will build and run automatically!

📄 Example
📄 Upload a PDF → 🪄 Get it indexed → ❓ Ask a question → 🤖 Get an answer.

📋 Notes
Works best with text-based PDFs (not scanned images).

Currently supports indexing one document per session.

Requires a valid Groq API key.

🙌 Credits
Built with ❤️ using open-source tools:

Gradio

FAISS

Sentence Transformers

Groq LLaMA3

📜 License
This project is licensed under the MIT License — feel free to use, modify, and share.
