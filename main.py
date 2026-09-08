import glob
import pymupdf4llm
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

exclusions = json.load(open("exclusions.json", "r", encoding="utf-8"))


def convert_pdf_to_markdown_pages(pdf_files):
    for  pdf_file in pdf_files:
        included_pages = [i for i in range(exclusions[Path(
            pdf_file).stem]["total_pages"]) if i not in exclusions[Path(pdf_file).stem]["exclude_pages"]]
        pages=pymupdf4llm.to_markdown(pdf_file,
                                           footer=False,
                                           header=False,
                                           page_chunks=True,
                                           pages=included_pages)

        # Uncomment the following line to save the markdown files in the md_files folder
        #Path(f"./md_files/{Path(pdf_file).stem}.md").write_text(pages,encoding="utf-8")
        return chunking_markdown_pages(pages)

def chunking_markdown_pages(pages):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=35,
        length_function=len,
    )
    chunks = text_splitter.split_text(pages)
    return chunks


if __name__ == "__main__":
    convert_pdf_to_markdown_pages(glob.glob("./src/*.pdf"))
