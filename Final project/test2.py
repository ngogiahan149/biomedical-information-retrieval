import pandas as pd
import pickle
from sentence_transformers import SentenceTransformer, util
import torch
def queryResult(query, corpus, corpus_embeddings, model, top_k):
    query_embedding = model.encode(query, convert_to_tensor=True)

    # We use cosine-similarity and torch.topk to find the highest 5 scores
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k) 
    print(cos_scores)
    values, indices = top_results
    print(values, indices)
    print("\n\n======================\n\n")
    print("Query:", query)
    print("\nTop 5 most similar sentences in corpus:")

    # for score, idx in zip(top_results[0], top_results[1]):
    #     print(corpus[idx], "(Score: {:.4f})".format(score))
    return top_results
model = SentenceTransformer('shainahub/covid_qa_distillbert')
clusterRep = pd.read_csv('./clusterRep.csv')
corpus = clusterRep['content']
# print(corpus)
# corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

# with open('corpus_embeddings_test.pickle', 'wb') as pkl:
#     pickle.dump(corpus_embeddings, pkl)
with open('corpus_embeddings.pickle', 'rb') as pkl:
    doc_embedding = pickle.load(pkl)
queryResult("hospital", corpus, doc_embedding, model, 5)