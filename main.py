import chromadb
from sentence_transformers import SentenceTransformer
from agents import evaluateQuery, evaluateChunks, answerQuery
client = chromadb.PersistentClient(path="./chromadb_storage")
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
    queryEval = evaluateQuery(user_query)
    if (queryEval.decision == "not_relevant"):
        return {
            "status": "not_relevant",
            "message": "The question is not related to the sources, and can not be answered."
        }
    if (queryEval.decision == "elaborate"):
        return {
            "status": "elaborate",
            "message": "The question is vague. Try to explain or rewrite."
        }
    else:
        query_embed = model.encode(user_query).tolist()
        results = send_query_to_chromadb(query_embed)

        formatted_results = []

        for index, chunk_id in enumerate(results["ids"][0]):
            metadata = results["metadatas"][0][index]

            formatted_results.append({
                "id": chunk_id,
                "text": results["documents"][0][index],
                "source_file": metadata["src_files"],
                "page_number": metadata["page_numbers"]
            })

        chunkEval = evaluateChunks(user_query, formatted_results)
        if (chunkEval.decision):
            allowed_ids = []
            for id in chunkEval.chunk_ids:
                allowed_ids.append(id)
            allowed_chunks = []
            for chunk in formatted_results:
                if chunk["id"] in allowed_ids:
                    allowed_chunks.append(chunk)
            answer_result = answerQuery(
                user_query,
                allowed_chunks
            )

            return {
                "status": "answered",
                "answer": answer_result.answer,
                "source_chunks": answer_result.source_chunks
            }
        else:
            return {
                "status": "aborted",
                "message": "There are not any information to answer this question"
            }


def print_answer(result):
    print("\n" + "=" * 60)

    if result["status"] != "answered":
        print("\nResult\n")
        print(result["message"])
        print("\n" + "=" * 60)
        return

    print("\nAnswer\n")
    print(result["answer"])

    print("\nSources\n")

    for index, source_id in enumerate(
        result["source_chunks"],
        start=1
    ):
        print(f"E{index}: {source_id}")

    print("\n" + "=" * 60)


if __name__ == "__main__":

    run = True
    while run:
        user_query = input("Enter your query (or type 'exit' to quit): ")
        if user_query.lower() == "exit":
            run = False
            print("Exiting the program.")
        else:
            ans = answer(user_query)
            print_answer(ans)
