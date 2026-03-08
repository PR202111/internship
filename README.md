# 📚 Document Vector Search API

A **FastAPI-based Retrieval-Augmented Generation (RAG) system** that
allows users to upload **PDF and TXT documents**, convert them into
**vector embeddings**, and query them using semantic search with
AI-powered summarization.

The system extracts text from documents, splits them into chunks,
generates embeddings, stores them in a **vector database**, and
retrieves relevant information to answer user queries.

------------------------------------------------------------------------

# 🚀 Features

-   📄 Upload **PDF and TXT files**
-   🧠 Automatic **text extraction and chunking**
-   🔎 **Semantic search** using vector embeddings
-   🤖 AI-powered **query summarization**
-   👤 **User session management**
-   📂 Persistent document storage per user
-   🗑️ Delete uploaded documents
-   📋 List uploaded documents
-   ⚡ FastAPI backend for high performance

------------------------------------------------------------------------

# 🏗️ System Architecture

User Upload\
↓\
Document Storage (User Folder)\
↓\
Text Extraction (PDF / TXT)\
↓\
Text Chunking\
↓\
Embedding Generation (Sentence Transformer)\
↓\
Vector Database (ChromaDB)\
↓\
Query Embedding\
↓\
Vector Similarity Search\
↓\
AI Summarizer\
↓\
Final Answer

------------------------------------------------------------------------

# 📂 Project Structure

    project/
    │
    ├── main.py               # FastAPI application
    ├── utils.py              # Text extraction, chunking, embeddings
    ├── ai_summarizer.py      # AI response generation
    ├── constants.py          # Configuration variables
    │
    ├── uploads/              # User document storage
    │   └── username/
    │       ├── file1.pdf
    │       └── notes.txt
    │
    └── README.md

------------------------------------------------------------------------

# ⚙️ Installation

## 1. Clone the Repository

    git clone https://github.com/yourusername/document-vector-search.git
    cd document-vector-search

## 2. Create Virtual Environment

    python -m venv venv

    source venv/bin/activate     # Linux / Mac
    venv\Scripts\activate      # Windows

## 3. Install Dependencies

    pip install fastapi uvicorn chromadb sentence-transformers pydantic

------------------------------------------------------------------------

# ▶️ Running the Application

Start the FastAPI server:

    python main.py

or

    uvicorn main:app --reload

The API will run at:

    http://127.0.0.1:8000

Interactive API docs:

    http://127.0.0.1:8000/docs

------------------------------------------------------------------------

# 📡 API Endpoints

## Start Session

    POST /start-session/

Request Body:

    {
      "username": "john"
    }

------------------------------------------------------------------------

## Upload Document

Upload a **PDF or TXT file**.

    POST /upload-pdf/

Form Data:

    file: document.pdf

------------------------------------------------------------------------

## List Documents

    GET /list-of-pdfs/

Example Response:

    {
      "pdfs": ["book.pdf", "notes.txt"]
    }

------------------------------------------------------------------------

## Query Document

    GET /query/

Parameters:

    query=What is automata theory?
    collection=book.pdf

Example Response:

    {
      "AiReply": "Automata theory studies abstract machines and computation..."
    }

------------------------------------------------------------------------

## Delete Document

    DELETE /delete-pdf/{pdf_name}

Example:

    DELETE /delete-pdf/book.pdf

------------------------------------------------------------------------

## End Session

    POST /end-session/

------------------------------------------------------------------------

# 🧠 How It Works

1.  **Upload Document** -- User uploads a PDF or TXT file.\
2.  **Text Extraction** -- Text is extracted from the file.\
3.  **Chunking** -- The text is split into smaller pieces.\
4.  **Embedding Generation** -- Each chunk is converted into a vector
    using a sentence transformer model.\
5.  **Vector Storage** -- Vectors are stored in ChromaDB.\
6.  **Query Processing** -- User query is converted to an embedding and
    matched against stored vectors.\
7.  **AI Summarization** -- Retrieved chunks are summarized into a final
    answer.

------------------------------------------------------------------------

# 🛠️ Technologies Used

  Technology              Purpose
  ----------------------- ----------------------
  FastAPI                 Backend API
  ChromaDB                Vector database
  Sentence Transformers   Embedding generation
  Uvicorn                 ASGI server
  Python                  Core language

------------------------------------------------------------------------

# 📊 Example Workflow

1.  Start session
2.  Upload document
3.  Ask questions
4.  Receive AI-generated answer based on document content

------------------------------------------------------------------------

# 🔒 Limitations

-   Supports **PDF and TXT files**
-   Maximum uploads controlled by `MAX_FILES`
-   Uses **in-memory session tracking**
-   Vector collections reset when session ends

------------------------------------------------------------------------

# 🔮 Future Improvements

-   Multi-document search
-   Persistent vector database
-   Streamlit frontend
-   Chat interface
-   Document highlighting
-   Support for DOCX / Markdown
-   Authentication system

------------------------------------------------------------------------

# 📜 License

MIT License
