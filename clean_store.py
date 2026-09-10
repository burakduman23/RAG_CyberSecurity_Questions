import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from sentence_transformers import SentenceTransformer
client = chromadb.PersistentClient(path="./chromadb_storage")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def visible_text_length(text):
    visible_text = re.sub(
        r"<!--.*?-->",
        "",
        text,
        flags=re.DOTALL
    )

    visible_text = re.sub(
        r"<[^>]+>",
        "",
        visible_text
    )

    return len(visible_text.strip())


def store_chunks_in_chromadb(chunks):
    print(len(chunks))
    embeddings = model.encode([chunk["text"] for chunk in chunks]).tolist()
    collection = client.get_or_create_collection(name="data_chunks", metadata={
                                          "description": "Chunks of PDF files"},
                                          embedding_function=None)

    collection.upsert(
        ids=[chunk["id"]
             for chunk in chunks if visible_text_length(chunk["text"]) > 40],
        documents=[chunk["text"]
                   for chunk in chunks if visible_text_length(chunk["text"]) > 40],
        embeddings=[embedding
                    for chunk, embedding in zip(chunks, embeddings) if visible_text_length(chunk["text"]) > 40],
        metadatas=[{
            "page_numbers": chunk["page_number"],
            "chunk_numbers": chunk["chunk_number"],
            "src_files": chunk["src_file"]
        } for chunk in chunks if visible_text_length(chunk["text"]) > 40]
    )
