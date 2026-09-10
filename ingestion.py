
from glob import glob
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pymupdf4llm
from sentence_transformers import SentenceTransformer
from pathlib import Path
from clean_store import store_chunks_in_chromadb
import json

pdf_files = sorted(Path("./pdfs").glob("*.pdf"))
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)
exclusions = json.load(open("exclusions.json", "r", encoding="utf-8"))
client = chromadb.PersistentClient(path="./chromadb_storage")
COLLECTION_NAME = "data_chunks"
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=75,
    length_function=len,
    separators=[
        "\n## ",
        "\n### ",
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


def convert_pdf_to_markdown_pages(pdf_files):
    all_pages = []
    for pdf_file in pdf_files:
        included_pages = [i for i in range(exclusions[Path(
            pdf_file).stem]["total_pages"]) if i not in exclusions[Path(pdf_file).stem]["exclude_pages"]]
        pages = pymupdf4llm.to_markdown(pdf_file,
                                        footer=False,
                                        header=False,
                                        page_chunks=True,
                                        pages=included_pages,
                                        ignore_images=True)

        # Uncomment the following line to save the markdown files in the md_files folder
        # Path(f"./md_files/{Path(pdf_file).stem}.md").write_text(pages,encoding="utf-8")
        all_pages.extend(pages)
    return chunk_markdown_pages(all_pages)


def chunk_markdown_pages(pages):
    chunks = []

    for page in pages:
        page_text = page["text"]
        metadata = page["metadata"]
        page_number = metadata["page_number"]
        src_file = metadata["file_path"]
        page_chunks = text_splitter.split_text(page_text)

        for i, chunk in enumerate(page_chunks):
            # Convert numpy array to list
            chunks.append({
                "id": f"{Path(src_file).stem}_page_{page_number}_chunk_{i}",
                "text": chunk,
                "page_number": page_number,
                "chunk_number": i,
                "src_file": src_file
            })
            # Uncomment the following line to save the chunks in the chunks folder
            # Path(f"./chunks/{Path(src_file).stem}_page_{page_number}_chunk_{i}.txt").write_text(chunk, encoding="utf-8")
    store_chunks_in_chromadb(chunks)

def collection_exists():
    return COLLECTION_NAME in {
        collection.name
        for collection in client.list_collections()
    }


if __name__ == "__main__":
    if collection_exists():
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=None
        )

        print(
            f"Collection already exists with "
            f"{collection.count()} chunks."
        )
        print(
            "Delete chromadb_storage for rebuild? (y/n): "
        )
        response = input().lower()
        if response == "y":
            client.delete_collection(name=COLLECTION_NAME)
            convert_pdf_to_markdown_pages(pdf_files)
            
    else:
        convert_pdf_to_markdown_pages(pdf_files)
