# RAG_CyberSecurity_Questions

A system for answering cybersecurity related questions only from provided pdfs. 5 strong sources from sources like CSI, NIST, and ITSM are used as the data source.
With splitters, those pdfs are first chunked, and then stored in vector database after they were embedded.
If user query is approved by evaluater agent, database's default similarity function returns the top 8 chunks to also be evaluated.
With all given, an answering agent evaluates both the query, the set of approved chunks to finalize an answer.

## This codespace utilizes:
- Python
- Ollama 
- Qwen3:4b
- all-miniLM-L6-v2
- Sentence Transformers
- PyMuPDF4LLM
- LangChain Text Splitters
- ChromaDB
- Pydantic

## File Structure

|- pdfs/&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;# Stores the source data\
|- chromadb_storage&emsp;&emsp;# Stores the local vector database\
|- exclusions.json&emsp;&emsp;&emsp;&ensp; # Marks the pages like contents, citations to exclude for reduced noise\
|- main.py &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;# Main workflow\
|- agents.py &emsp;&emsp;&emsp;&emsp;&emsp;&ensp; # Seperate agents for query, chunks, and answer evaluation\
|- ingestion.py &emsp;&emsp;&emsp;&emsp;&ensp; # Splitting, chunking, and embedding the sources\
|- clean_store &emsp;&emsp;&emsp;&emsp;&emsp; # Sanitizing tag strings and storing chunks in chromaDB\
>folders named ./chunks and ./md_files are for debugging

## Setup
Assuming you will use provided source set, pdfs folder contains the test set. 
If changed, exclusions.json, and agent instructions in agent.py also need change.

### 1. Create and move into virtual environment
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
### 2. Install dependencies
```
python -m pip install -r requirements.txt
```

### 3. Install Ollama
```
irm https://ollama.com/install.ps1 | iex
```

### 4. Install language model
```
ollama pull qwen3:4b
```
With these steps only after these steps>

### 5. Extract pdfs and store vectors
```
python ingestion.py
```
### 6. Run the system
```
python main.py
```
At the end of all these steps, there will be a command line prompt for you to ask your question.