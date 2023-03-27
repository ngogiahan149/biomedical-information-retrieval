import networkx as nx
import community as community_louvain

import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from embed import keyphraseExtract
import json
import numpy as np
import matplotlib.pyplot as plt
from embed import returnParagraphid, queryResult
import pickle
from PIL import Image
# Ignore warning when deploying web
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("Final project")
#Load model covid qa distillbert
model = SentenceTransformer('shainahub/covid_qa_distillbert')

# st.pyplot()
def main(model, doc_embedding, paperInfor):
    text_input = st.text_input(
        "Enter query 👇",
    )
    if text_input:
        st.write("Search query: ", text_input)
        result = queryResult(text_input, doc_embedding, model, 3)
        values, indices = result
        list_id = returnParagraphid(indices.numpy())
        for id in list_id:
            st.write(id)
            st.header(paperInfor.loc[paperInfor['id'] == id, "title"].values[0])
            st.write(paperInfor.loc[paperInfor['id'] == id, "authors"].values[0])
            st.subheader("Abstract")
            st.write(paperInfor.loc[paperInfor['id'] == id, "abstract"].values[0])
            st.write(paperInfor.loc[paperInfor['id'] == id, "textcontent"].values[0])
            st.write("Link: ", str(paperInfor.loc[paperInfor['id'] == id, "doi"].values[0]))

if __name__=="__main__":
    model = SentenceTransformer('shainahub/covid_qa_distillbert')
    image = Image.open('Picture1.png')

    st.image(image, caption='Dataset network')
    with open('corpus_embeddings.pickle', 'rb') as pkl:
        doc_embedding = pickle.load(pkl)
    paperInfor = pd.read_csv('./paragraphWithPaperInfor.csv')
    paperInfor.replace(np.nan, 0)
    main(model, doc_embedding, paperInfor)


