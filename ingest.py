from pathlib import Path
import shutil

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

documents_folder = Path("documents")
chroma_folder = Path("chroma_db")

text_files = list(documents_folder.glob("*.txt"))

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)

all_chunks = []
all_metadatas = []


for file_path in text_files:
    text = file_path.read_text(encoding="utf-8")

    chunks = splitter.split_text(text)

    print(f"{file_path.name}: {len(chunks)} chunks")

    for chunk in chunks:
        all_chunks.append(chunk)

        all_metadatas.append({
            "source": file_path.name
        })


if not all_chunks:
    print("No text documents found.")
    raise SystemExit


if chroma_folder.exists():
    shutil.rmtree(chroma_folder)
    print("Old ChromaDB deleted.")


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)


vector_store = Chroma.from_texts(
    texts=all_chunks,
    embedding=embeddings,
    metadatas=all_metadatas,
    persist_directory="chroma_db"
)


print(f"{len(all_chunks)} chunks embedded and stored in ChromaDB!")