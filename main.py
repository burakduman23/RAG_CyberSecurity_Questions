import sys
from time import perf_counter
import glob
import pymupdf4llm
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path



def convert_pdf_to_markdown(pdf_files):
    mds=[]
    for pdf_file in pdf_files:
        mds.append(pymupdf4llm.to_markdown(pdf_file))
    return mds


if __name__ == "__main__":
    print(convert_pdf_to_markdown(glob.glob("./src/*.pdf")))

   









