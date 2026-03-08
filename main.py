from fastapi import FastAPI,HTTPException,UploadFile,File
from pydantic import BaseModel
from constants import UPLOAD_DIR,MAX_FILES
import os
import shutil
import uvicorn
from utils import extract_text_from_pdf,chunk_text,create_embeddings,client,model
from ai_summarizer import summarize_query

MAP = {}
CURRENT_USER = None
USER_DIR = None

app = FastAPI(title="Convert Pdf to a Search DB",version="1.0")
os.makedirs(UPLOAD_DIR, exist_ok=True)



def store_vectors(chunks,embeddings,collection_name):
    collection = client.get_or_create_collection(collection_name)
    
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i].tolist()],
            ids=[str(i)]
        )
    
@app.get("/")
def root():
    return {"message": "PDF Vector Search API Running"}


class UserRequest(BaseModel):
    username: str


@app.post("/start-session/")
def start_session(user: UserRequest):

    global CURRENT_USER, USER_DIR, MAP

    CURRENT_USER = user.username
    USER_DIR = os.path.join(UPLOAD_DIR, CURRENT_USER)

    os.makedirs(USER_DIR, exist_ok=True)

    MAP.clear()

    for file in os.listdir(USER_DIR):

        if file.endswith(".pdf"):

            file_path = os.path.join(USER_DIR, file)

            text = extract_text_from_pdf(file_path)
            chunks = chunk_text(text)
            embeddings = create_embeddings(chunks)

            collection_name = f"{CURRENT_USER}_{file}"

            store_vectors(chunks, embeddings, collection_name)

            MAP[file] = collection_name

    return {"message": f"Session started for {CURRENT_USER}"}


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):

    if len(MAP) >= MAX_FILES:
        raise HTTPException(
            status_code=400,
            detail="Max PDF uploads reached. Delete a PDF first."
        )

    if file.filename in MAP:
        raise HTTPException(
            status_code=400,
            detail="PDF already uploaded"
        )
    
    if CURRENT_USER is None:
        raise HTTPException(
            status_code=400,
            detail="Start a session first"
        )

    file_path = os.path.join(USER_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)
    embeddings = create_embeddings(chunks)

    collection_name = f"{CURRENT_USER}_{file.filename}"

    store_vectors(chunks, embeddings, collection_name)

    MAP[file.filename] = collection_name

    return {"message": "PDF processed and indexed"}


@app.get("/list-of-pdfs/")
def list_pdfs():

    return {
        "pdfs": list(MAP.keys())
    }

@app.delete("/delete-pdf/{pdf_name}")
def delete_pdf(pdf_name: str):

    if pdf_name not in MAP:
        raise HTTPException(status_code=404, detail="PDF not found")

    collection_name = MAP[pdf_name]

    client.delete_collection(collection_name)

    
    file_path = os.path.join(USER_DIR, pdf_name)
    if os.path.exists(file_path):
        os.remove(file_path)

    del MAP[pdf_name]

    return {"message": f"{pdf_name} deleted successfully"}

@app.get("/query/")
def query_docs(query: str, collection: str):

    if collection not in MAP:
        raise HTTPException(status_code=404, detail="PDF not found")

    collection_obj = client.get_collection(MAP[collection])

    query_embedding = model.encode([query])[0]

    results = collection_obj.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=3
    )
    print(results)
    reply = summarize_query(query, results)

    return {"AiReply": reply}


@app.post("/end-session/")
def end_session():

    global CURRENT_USER, USER_DIR

    for key in list(MAP.keys()):

        collection_name = MAP[key]
        client.delete_collection(collection_name)

        del MAP[key]

    CURRENT_USER = None
    USER_DIR = None

    return {"success": "Session Ended"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
