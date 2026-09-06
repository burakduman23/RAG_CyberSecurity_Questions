import pymupdf4llm
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path


src1 = "./src/CSI-PHISHING-GUIDANCE.pdf"
src2 = "./src/get-cyber-safe-guide-small-businesses-v2-e.pdf"
src3 = "./src/NIST.SP.800-124r2.pdf"

print("Loading documents...")
md1 = pymupdf4llm.to_markdown(src1)
md2 = pymupdf4llm.to_markdown(src2)
md3 = pymupdf4llm.to_markdown(src3)

print("Writing markdown files...")

Path("output1.md").write_bytes(md1.encode())
Path("output2.md").write_bytes(md2.encode())
Path("output3.md").write_bytes(md3.encode())

print("Markdown files written successfully.")

if __name__ == "__main__":
    # Your main code logic here
    print("This is the main entry point of the program.")