import chromadb

def send_query_to_chromadb(query, top_k=8):
    collection = client.get_collection(name="data_chunks")
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    return results


if __name__ == "__main__":

    client = chromadb.PersistentClient(path="./chromadb_storage")
    run = True
    while run:
        user_query = input("Enter your query (or type 'exit' to quit): ")
        if user_query.lower() == "exit":
            run = False
            print("Exiting the program.")
        else:
            results = send_query_to_chromadb(user_query, top_k=8)
            print("Top results:")
            for i, result in enumerate(results['documents'][0]):
                print(f"{i + 1}. {result}")
                print(f"   Page Number: {results['metadatas'][0][i]['page_numbers']}, Chunk Number: {results['metadatas'][0][i]['chunk_numbers']}, Source File: {results['metadatas'][0][i]['src_files']}")
