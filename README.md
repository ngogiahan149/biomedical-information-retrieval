# Biomedical Information Retrieval
This is a project related to nlp in biomedical domain. There are search functions, tokenizer, ...
## Table of contents
* [Code](#code)
* [Data](#data)
* [Pretrained models](#pretrained-models)
* [Final project](#final-project)
## Code
This folder includes functions in information retrieval: skipgram, cbow, tokenization, semantic search, ... with simple Tkinter application
To run Tkinter application:
```
python gui.py
```
## Data
This folder includes data for the above code to train models and evaluate:
* Pubmed_JSON: include JSON format files for PMID documents
* Pubmed_XML: include XML format files for PMID documents
* Tweet_data: includes JSON format file for tweets
## Pretrained models
This folder includes pretrained models: skipgram and cbow with different epochs, winsize and training number of documents
## Final project
This folder includes the complete search tool with visualization for keywords relations from all documents.
![plot](https://github.com/ngogiahan149/biomedical-information-retrieval/blob/c91b62c6748d5741668c02de5cc6b9dc7c4cf0b7/Final%20project/graph_overall.png)
* Each edge represents there are connections between the paragraphs and its citation
* Node size represents how many connections from that node to other nodes

![plot_2](https://github.com/ngogiahan149/biomedical-information-retrieval/blob/c91b62c6748d5741668c02de5cc6b9dc7c4cf0b7/Final%20project/relation.png)
