from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import csv
import pandas as pd
import torch
import pickle
import json
def keyphraseExtract(doc, top_n, diversity, model):
    n_gram_range = (4, 4)
    stop_words = "english"

    # Extract candidate words/phrases
    count = CountVectorizer(ngram_range=n_gram_range, stop_words=stop_words).fit([doc])
    candidates = count.get_feature_names_out()
    doc_embedding = model.encode([doc])
    word_embeddings = model.encode(candidates)
    distances = cosine_similarity(doc_embedding, word_embeddings)
    word_doc_similarity = cosine_similarity(word_embeddings, doc_embedding)
    word_similarity = cosine_similarity(word_embeddings)

    # Initialize candidates and already choose best keyword/keyphras
    keywords_idx = [np.argmax(word_doc_similarity)]
    candidates_idx = [i for i in range(len(candidates)) if i != keywords_idx[0]]

    for _ in range(top_n - 1):
        # Extract similarities within candidates and
        # between candidates and selected keywords/phrases
        candidate_similarities = word_doc_similarity[candidates_idx, :]
        target_similarities = np.max(word_similarity[candidates_idx][:, keywords_idx], axis=1)

        # Calculate MMR
        mmr = (1-diversity) * candidate_similarities - diversity * target_similarities.reshape(-1, 1)
        mmr_idx = candidates_idx[np.argmax(mmr)]

        # Update keywords & candidates
        keywords_idx.append(mmr_idx)
        candidates_idx.remove(mmr_idx)

    return [candidates[idx] for idx in keywords_idx]
def addKeyphrase(file):
    csv_data = csv.reader(open(file, 'r', encoding='utf8', errors='ignore'))
    csv_new = csv.writer(open('paragraphs_new.csv', 'w', encoding="utf8", errors='ignore', newline=''))
    for i, row in enumerate(csv_data):
        if i == 0:
            csv_new.writerow(row)
        else:
            keyphrase = keyphraseExtract(row[1], 1, 0.5)
            row.append(keyphrase[0])
            csv_new.writerow(row)
            print(i, ": ", row, "\n-------------------------------------------")
# addKeyphrase('./paragraphs.csv')
def queryResult(query, corpus_embeddings, model, top_k):
    query_embedding = model.encode(query, convert_to_tensor=True)

    # We use cosine-similarity and torch.topk to find the highest 5 scores
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)
    print(top_results)
    print("\n\n======================\n\n")
    print("Query:", query)
    print("\nTop 5 most similar sentences in corpus:")

    # for score, idx in zip(top_results[0], top_results[1]):
    #     print(corpus[idx], "(Score: {:.4f})".format(score))
    return top_results
# model = SentenceTransformer('shainahub/covid_qa_distillbert')
# clusterRep = pd.read_csv('./clusterRep.csv')
# corpus = clusterRep['content']
# # corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

# # with open('corpus_embeddings.pickle', 'wb') as pkl:
# #     pickle.dump(corpus_embeddings, pkl)
# with open('corpus_embeddings.pickle', 'rb') as pkl:
#     doc_embedding = pickle.load(pkl)
# result = queryResult('what is COVID-19?', doc_embedding, model, 5)
# values, indices = result
def returnParagraphid(cluster_list):
    paraid_list = []
    with open('paragraphCommunity.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for cluster_id in cluster_list:
            for item in data:
                # print(type(item))
                if str(item) == str(cluster_id):
                    for value in data[item]:
                        paraid_list.append(value)
    return paraid_list
# returnParagraphid(indices.numpy())