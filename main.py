import chromadb
from sentence_transformers import SentenceTransformer
from agents import evaluateQuery, evaluateChunks, answerQuery

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def send_query_to_chromadb(query_embedding, top_k=8):
    collection = client.get_collection(name="data_chunks",
                                       embedding_function=None)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    return results

def answer(user_query):
    if(evaluateQuery(user_query).decision=="not_relevant"):
        return {
            "status": "not_relevant",
            "message": "The question is not related to the sources, and can not be answered."
        }
    
    
    
    return

if __name__ == "__main__":

    client = chromadb.PersistentClient(path="./chromadb_storage")
    run = True
    while run:
        user_query = input("Enter your query (or type 'exit' to quit): ")
        if user_query.lower() == "exit":
            run = False
            print("Exiting the program.")
        else:
            answer(user_query)
