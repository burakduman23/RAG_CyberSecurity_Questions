from sentence_transformers import SentenceTransformer, util

sentences = ["This is an example sentence", 
             "Each sentence is converted",
             "This is a test sentence",
             "We both need to quit"]
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(sentences)

print(util.cos_sim(embeddings[0], embeddings[1]))
print("="*50)
print(util.cos_sim(embeddings[0], embeddings[2]))
print("="*50)
print(util.cos_sim(embeddings[0], embeddings[3]))
print("="*50)
print(util.cos_sim(embeddings[2], embeddings[3]))

exit()