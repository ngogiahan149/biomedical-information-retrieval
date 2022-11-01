from ast import Compare
from os import remove
from tkinter import filedialog
from tkinter import *
import gensim
from word2vec import *
from zipfDistribution import removePunc, removeStopWords
from gensim.models import FastText
def OpenModel():
    filetypes = (
        ('model files', "*"),
    )

    fileName = filedialog.askopenfile(
        title='Choose a model file',
        initialdir='/',
        filetypes=filetypes)
    return fileName

def Analyze(input, compare1, compare2, modelFrame, modelName, predictFrame):
    for widget in predictFrame.winfo_children():
        widget.destroy()
    for widget in modelFrame.winfo_children():
        widget.destroy()
    num_document = 0
    name_model = ''
    num_epoch = 0

    # if "cbow_400doc_5winsize_200epochs" in modelName:
    #     name_model = "CBOW"
    #     num_document = 400
    #     num_epoch = 200
    # elif "cbow_2000doc_5winsize_200epochs" in modelName:
    #     name_model = "CBOW"
    #     num_document = 2000
    #     num_epoch = 200
    # elif "cbow_8000doc_5winsize_200epochs" in modelName:
    #     name_model = "CBOW"
    #     num_document = 7975
    #     num_epoch = 200
    # elif "skipgram_400doc_5winsize_200epochs" in modelName:
    #     name_model = "Skipgram"
    #     num_document = 400
    #     num_epoch = 200
    # elif "skipgram_2000doc_5winsize_200epochs" in modelName:
    #     name_model = "Skipgram"
    #     num_document = 2000
    #     num_epoch = 200
    # elif "skipgram_8000doc_5winsize_200epochs" in modelName:
    #     name_model = "Skipgram"
    #     num_document = 7975
    #     num_epoch = 200
    # elif "cbow_2000doc_5winsize_50epochs" in modelName:
    #     name_model = "CBOW 50 epochs"
    #     num_document = 2000
    #     num_epoch = 50
    # elif "cbow_2000doc_5winsize_800epochs" and "800epo" in modelName:
    #     name_model = "CBOW 800 epochs"
    #     num_document = 2000
    #     num_epoch = 800
    # elif "cbow_2000doc_5winsize_1000epochs" and "1000epo" in modelName:
    #     name_model = "CBOW 1000 epochs"
    #     num_document = 2000
    #     num_epoch = 1000
    # elif "skipgram_2000doc_5winsize_50epochs" in modelName:
    #     name_model = "Skipgram 50 epochs"
    #     num_document = 2000
    #     num_epoch = 50
    # elif "skipgram_2000doc_5winsize_800epochs" in modelName:
    #     name_model = "Skipgram 800 epochs"
    #     num_document = 2000
    #     num_epoch = 800
    # elif "skipgram_2000doc_5winsize_1000epochs" in modelName:
    #     name_model = "Skipgram 1000 epochs"
    #     num_document = 2000
    #     num_epoch = 1000
    type = 0
    if "cbow_6205doc_5winsize_200epochs" in modelName:
        name_model = "CBOW Word2vec"
        num_document = 6205
        num_epoch = 200
    elif "skipgram_6205doc_5winsize_200epochs" in modelName:
        name_model = "Skipgram Word2vec"
        num_document = 6205
        num_epoch = 200
    elif "fastcbow_6205doc_5winsize_200epochs" in modelName:
        name_model = "Fasttext CBOW"
        num_document = 6205
        num_epoch = 200
        type = 1
    elif "fastskipgram_6205doc_5winsize_200epochs" in modelName:
        name_model = "Fasttext Skipgram"
        num_document = 6205
        num_epoch = 200
        type = 1
    if type == 0:
        model = gensim.models.Word2Vec.load(modelName)
        input = [w for w in InputPreprocess(input) if w in model.wv.index_to_key]
    else:
        model = gensim.models.FastText.load(modelName)
        input = [w for w in InputPreprocess(input)]
    # input = [w for w in InputPreprocess(input) if w in model.wv.index_to_key]
    similar_word = model.wv.most_similar(input, topn = 10)
    #---Model frame-------------------------------------------
    ModelInfor = Label(modelFrame, text='MODEL INFOR')
    ModelInfor.grid(row=0, column=0, padx=5, pady=5)
    Vocabulary = Label(modelFrame, text='Vocabulary:')
    Vocabulary.grid(row=1, column=0, padx=5, pady=5)
    WindowSize = Label(modelFrame, text='Window Size:')
    WindowSize.grid(row=2, column=0, padx=5, pady=5)
    Epoch = Label(modelFrame, text='Epochs:')
    Epoch.grid(row=3, column=0, padx=5, pady=5)
    Documents = Label(modelFrame, text='Training documents:')
    Documents.grid(row=4, column=0, padx=5, pady=5)

    # Labels to show results on the right side
    ModelName = Label(modelFrame, text=name_model)
    ModelName.grid(row=0, column=1, padx=5, pady=5)
    NumVocab = Label(modelFrame, text=len(model.wv.index_to_key))
    NumVocab.grid(row=1, column=1, padx=5, pady=5)
    NumWinSize = Label(modelFrame, text="5")
    NumWinSize.grid(row=2, column=1, padx=5, pady=5)
    NumEpoch = Label(modelFrame, text=num_epoch)
    NumEpoch.grid(row=3, column=1, padx=5, pady=5)
    NumDoc = Label(modelFrame, text=str(num_document) + " documents")
    NumDoc.grid(row=4, column=1, padx=5, pady=5)
    #---End Model frame---------------------------------------

    #---Analysis frame-----------------------------------------
    SimilarWords = Label(predictFrame, text='Top 10 similar words')
    SimilarWords.grid(row=0, column=0, padx=5, pady=5, columnspan = 2)
    WordTitle = Label(predictFrame, text='Word')
    WordTitle.grid(row=1, column=0, padx=5, pady=5)
    PercentageTitle = Label(predictFrame, text='Scores')
    PercentageTitle.grid(row=1, column=1, padx=5, pady=5)

    if len(compare1.split()) > 1 or len(compare2.split()) > 1:
        if type == 0:
        #Preprocess compare word 1 and 2
            compare1_words= [w for w in InputPreprocess(compare1) if w in model.wv.index_to_key]
            compare2_words = [w for w in InputPreprocess(compare2) if w in model.wv.index_to_key]
        else:
            compare1_words= [w for w in InputPreprocess(compare1)]
            compare2_words = [w for w in InputPreprocess(compare2)]
        #Count cosine similarity between 2 compare words
        similarity = '%.4f' % model.wv.n_similarity(compare1_words, compare2_words)
    else:
        compare1_words = removePunc(compare1)
        compare2_words = removePunc(compare2)
        similarity = '%.4f' % model.wv.similarity(compare1_words, compare2_words)
    i = 1
    list_word ={}
    list_score = {}
    for (word, score) in similar_word:
        list_word[i] = Label(predictFrame, text=word)
        list_word[i].grid(row=i+1, column=0, padx=5, pady=5)
        list_score[i] = Label(predictFrame, text='%.4f' % score)
        list_score[i].grid(row=i+1, column=1, padx=5, pady=5)
        i += 1
    CompareTitle = Label(predictFrame, text='Similarity between 2 inputs')
    CompareTitle.grid(row=i, column=0, padx=5, pady=5, columnspan = 2)
    CompareSimilarity = Label(predictFrame, text=similarity)
    CompareSimilarity.grid(row=i+1, column=0, columnspan = 2)
    

def AnalyzeAll(input, compare1, compare2, modelFrame, predictFrame):
    for widget in predictFrame.winfo_children():
        widget.destroy()
    for widget in modelFrame.winfo_children():
        widget.destroy()
    #Define name models
    # name_model = ["CBOW 400", "CBOW 2000", 
    # "CBOW 7975", "Skipgram 400", "Skipgram 2000", "Skipgram 7975", 
    # "CBOW 50 epochs", "CBOW 800 epochs", "CBOW 1000 epochs", 
    # "Skipgram 50 epochs", "Skipgram 800 epochs", "Skipgram 1000 epochs",]
    name_model = ["CBOW Word2vec", "Skipgram Word2vec", "Fasttext CBOW", "Fasttext Skipgram"]
    #Load models
    # cbow_400 = gensim.models.Word2Vec.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\cbow_400doc_5winsize_200epochs")
    # skipgram_400 = gensim.models.Word2Vec.load(r"D:\NCKU\Biomedical Informattion Retrieval\HW1\Model\skipgram_400doc_5winsize_200epochs")
    # cbow_2000 = gensim.models.Word2Vec.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\cbow_2000doc_5winsize_200epochs")
    # skipgram_2000 = gensim.models.Word2Vec.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\skipgram_2000doc_5winsize_200epochs")
    # cbow_7975 = gensim.models.Word2Vec.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\cbow_8000doc_5winsize_200epochs")
    # skipgram_7975 = gensim.models.Word2Vec.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\skipgram_8000doc_5winsize_200epochs")
    # cbow_50epo = gensim.models.Word2Vec.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\cbow_2000doc_5winsize_50epochs")
    # cbow_800epo = gensim.models.Word2Vec.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\cbow_2000doc_5winsize_800epochs")
    # cbow_1000epo = gensim.models.Word2Vec.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\cbow_2000doc_5winsize_1000epochs")
    # skipgram_50epo = gensim.models.Word2Vec.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\skipgram_2000doc_5winsize_50epochs")
    # skipgram_800epo = gensim.models.Word2Vec.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\skipgram_2000doc_5winsize_800epochs")
    # skipgram_1000epo = gensim.models.Word2Vec.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\skipgram_2000doc_5winsize_1000epochs")
    skipgram = gensim.models.Word2Vec.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\skipgram_6205doc_5winsize_800epochs")
    cbow = gensim.models.Word2Vec.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\cbow_6205doc_5winsize_1000epochs")
    fasttext_cbow =FastText.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\fastcbow_6205doc_5winsize_1000epochs")
    fasttext_skipgram = FastText.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\fastskipgram_6205doc_5winsize_1000epochs")

    #---Model frame-------------------------------------------
    ModelInfor = Label(modelFrame, text='MODEL INFOR')
    ModelInfor.grid(row=0, column=0, padx=5, pady=5)
    Vocabulary = Label(modelFrame, text='Vocabulary:')
    Vocabulary.grid(row=1, column=0, padx=5, pady=5)
    WindowSize = Label(modelFrame, text='Window Size:')
    WindowSize.grid(row=2, column=0, padx=5, pady=5)
    lb_Epoch = Label(modelFrame, text='Epochs:')
    lb_Epoch.grid(row=3, column=0, padx=5, pady=5)
    lb_Documents = Label(modelFrame, text='Training documents:')
    lb_Documents.grid(row=4, column=0, padx=5, pady=5)

    # Labels model 1
    lb_ModelName1 = Label(modelFrame, text=name_model[0])
    lb_ModelName1.grid(row=0, column=1, padx=5, pady=5)
    lb_NumVocab1 = Label(modelFrame, text=len(cbow.wv.index_to_key))
    lb_NumVocab1.grid(row=1, column=1, padx=5, pady=5)
    lb_NumWinSize1 = Label(modelFrame, text="5")
    lb_NumWinSize1.grid(row=2, column=1, padx=5, pady=5)
    lb_NumEpoch1 = Label(modelFrame, text='200 epochs')
    lb_NumEpoch1.grid(row=3, column=1, padx=5, pady=5)
    lb_NumDoc1 = Label(modelFrame, text='6205 documents')
    lb_NumDoc1.grid(row=4, column=1, padx=5, pady=5)

    # Labels model 2
    lb_ModelName2 = Label(modelFrame, text=name_model[1])
    lb_ModelName2.grid(row=0, column=2, padx=5, pady=5)
    lb_NumVocab2 = Label(modelFrame, text=len(skipgram.wv.index_to_key))
    lb_NumVocab2.grid(row=1, column=2, padx=5, pady=5)
    lb_NumWinSize2 = Label(modelFrame, text="5")
    lb_NumWinSize2.grid(row=2, column=2, padx=5, pady=5)
    lb_NumEpoch2 = Label(modelFrame, text='200 epochs')
    lb_NumEpoch2.grid(row=3, column=2, padx=5, pady=5)
    lb_NumDoc2 = Label(modelFrame, text='6205 documents')
    lb_NumDoc2.grid(row=4, column=2, padx=5, pady=5)

    # Labels model 3
    lb_ModelName3 = Label(modelFrame, text=name_model[2])
    lb_ModelName3.grid(row=0, column=3, padx=5, pady=5)
    lb_NumVocab3 = Label(modelFrame, text=len(fasttext_cbow.wv.index_to_key))
    lb_NumVocab3.grid(row=1, column=3, padx=5, pady=5)
    lb_NumWinSize3 = Label(modelFrame, text="5")
    lb_NumWinSize3.grid(row=2, column=3, padx=5, pady=5)
    lb_NumEpoch3 = Label(modelFrame, text='200 epochs')
    lb_NumEpoch3.grid(row=3, column=3, padx=5, pady=5)
    lb_NumDoc3 = Label(modelFrame, text='6205 documents')
    lb_NumDoc3.grid(row=4, column=3, padx=5, pady=5)

    # Labels model 4
    lb_ModelName4 = Label(modelFrame, text=name_model[3])
    lb_ModelName4.grid(row=0, column=4, padx=5, pady=5)
    lb_NumVocab4 = Label(modelFrame, text=len(fasttext_skipgram.wv.index_to_key))
    lb_NumVocab4.grid(row=1, column=4, padx=5, pady=5)
    lb_NumWinSize4 = Label(modelFrame, text="5")
    lb_NumWinSize4.grid(row=2, column=4, padx=5, pady=5)
    lb_NumEpoch4 = Label(modelFrame, text='200 epochs')
    lb_NumEpoch4.grid(row=3, column=4, padx=5, pady=5)
    lb_NumDoc4 = Label(modelFrame, text='6205 documents')
    lb_NumDoc4.grid(row=4, column=4, padx=5, pady=5)

    # # Labels model 5
    # lb_ModelName5 = Label(modelFrame, text=name_model[4])
    # lb_ModelName5.grid(row=0, column=5, padx=5, pady=5)
    # lb_NumVocab5 = Label(modelFrame, text=len(skipgram_2000.wv.index_to_key))
    # lb_NumVocab5.grid(row=1, column=5, padx=5, pady=5)
    # lb_NumWinSize5 = Label(modelFrame, text="5")
    # lb_NumWinSize5.grid(row=2, column=5, padx=5, pady=5)
    # lb_NumEpoch5 = Label(modelFrame, text='200 epochs')
    # lb_NumEpoch5.grid(row=3, column=5, padx=5, pady=5)
    # lb_NumDoc5 = Label(modelFrame, text='2000 documents')
    # lb_NumDoc5.grid(row=4, column=5, padx=5, pady=5)

    # # Labels model 6
    # lb_ModelName6 = Label(modelFrame, text=name_model[5])
    # lb_ModelName6.grid(row=0, column=6, padx=5, pady=5)
    # lb_NumVocab6 = Label(modelFrame, text=len(skipgram_7975.wv.index_to_key))
    # lb_NumVocab6.grid(row=1, column=6, padx=5, pady=5)
    # lb_NumWinSize6 = Label(modelFrame, text="5")
    # lb_NumWinSize6.grid(row=2, column=6, padx=5, pady=5)
    # lb_NumEpoch6 = Label(modelFrame, text='200 epochs')
    # lb_NumEpoch6.grid(row=3, column=6, padx=5, pady=5)
    # lb_NumDoc6 = Label(modelFrame, text='7975 documents')
    # lb_NumDoc6.grid(row=4, column=6, padx=5, pady=5)
    
    # # Labels model 7
    # lb_ModelName7 = Label(modelFrame, text=name_model[6])
    # lb_ModelName7.grid(row=0, column=7, padx=5, pady=5)
    # lb_NumVocab7 = Label(modelFrame, text=len(cbow_50epo.wv.index_to_key))
    # lb_NumVocab7.grid(row=1, column=7, padx=5, pady=5)
    # lb_NumWinSize7 = Label(modelFrame, text="5")
    # lb_NumWinSize7.grid(row=2, column=7, padx=5, pady=5)
    # lb_NumEpoch7 = Label(modelFrame, text='50 epochs')
    # lb_NumEpoch7.grid(row=3, column=7, padx=5, pady=5)
    # lb_NumDoc7 = Label(modelFrame, text='2000 documents')
    # lb_NumDoc7.grid(row=4, column=7, padx=5, pady=5)

    # # Labels model 8
    # lb_ModelName8 = Label(modelFrame, text=name_model[7])
    # lb_ModelName8.grid(row=0, column=8, padx=5, pady=5)
    # lb_NumVocab8 = Label(modelFrame, text=len(cbow_800epo.wv.index_to_key))
    # lb_NumVocab8.grid(row=1, column=8, padx=5, pady=5)
    # lb_NumWinSize8 = Label(modelFrame, text="5")
    # lb_NumWinSize8.grid(row=2, column=8, padx=5, pady=5)
    # lb_NumEpoch8 = Label(modelFrame, text='800 epochs')
    # lb_NumEpoch8.grid(row=3, column=8, padx=5, pady=5)
    # lb_NumDoc8 = Label(modelFrame, text='2000 documents')
    # lb_NumDoc8.grid(row=4, column=8, padx=5, pady=5)

    # # Labels model 9
    # lb_ModelName9 = Label(modelFrame, text=name_model[8])
    # lb_ModelName9.grid(row=0, column=9, padx=5, pady=5)
    # lb_NumVocab9 = Label(modelFrame, text=len(cbow_1000epo.wv.index_to_key))
    # lb_NumVocab9.grid(row=1, column=9, padx=5, pady=5)
    # lb_NumWinSize9 = Label(modelFrame, text="5")
    # lb_NumWinSize9.grid(row=2, column=9, padx=5, pady=5)
    # lb_NumEpoch9 = Label(modelFrame, text='1000 epochs')
    # lb_NumEpoch9.grid(row=3, column=9, padx=5, pady=5)
    # lb_NumDoc9 = Label(modelFrame, text='2000 documents')
    # lb_NumDoc9.grid(row=4, column=9, padx=5, pady=5)

    # # Labels model 10
    # lb_ModelName10 = Label(modelFrame, text=name_model[9])
    # lb_ModelName10.grid(row=0, column=10, padx=5, pady=5)
    # lb_NumVocab10 = Label(modelFrame, text=len(skipgram_50epo.wv.index_to_key))
    # lb_NumVocab10.grid(row=1, column=10, padx=5, pady=5)
    # lb_NumWinSize10 = Label(modelFrame, text="5")
    # lb_NumWinSize10.grid(row=2, column=10, padx=5, pady=5)
    # lb_NumEpoch10 = Label(modelFrame, text='50 epochs')
    # lb_NumEpoch10.grid(row=3, column=10, padx=5, pady=5)
    # lb_NumDoc10 = Label(modelFrame, text='2000 documents')
    # lb_NumDoc10.grid(row=4, column=10, padx=5, pady=5)

    # # Labels model 11
    # lb_ModelName11 = Label(modelFrame, text=name_model[10])
    # lb_ModelName11.grid(row=0, column=11, padx=5, pady=5)
    # lb_NumVocab11 = Label(modelFrame, text=len(skipgram_800epo.wv.index_to_key))
    # lb_NumVocab11.grid(row=1, column=11, padx=5, pady=5)
    # lb_NumWinSize11 = Label(modelFrame, text="5")
    # lb_NumWinSize11.grid(row=2, column=11, padx=5, pady=5)
    # lb_NumEpoch11 = Label(modelFrame, text='800 epochs')
    # lb_NumEpoch11.grid(row=3, column=11, padx=5, pady=5)
    # lb_NumDoc11 = Label(modelFrame, text='2000 documents')
    # lb_NumDoc11.grid(row=4, column=11, padx=5, pady=5)

    # # Labels model 12
    # lb_ModelName12 = Label(modelFrame, text=name_model[11])
    # lb_ModelName12.grid(row=0, column=12, padx=5, pady=5)
    # lb_NumVocab12 = Label(modelFrame, text=len(skipgram_1000epo.wv.index_to_key))
    # lb_NumVocab12.grid(row=1, column=12, padx=5, pady=5)
    # lb_NumWinSize12 = Label(modelFrame, text="5")
    # lb_NumWinSize12.grid(row=2, column=12, padx=5, pady=5)
    # lb_NumEpoch12 = Label(modelFrame, text='1000 epochs')
    # lb_NumEpoch12.grid(row=3, column=12, padx=5, pady=5)
    # lb_NumDoc12 = Label(modelFrame, text='2000 documents')
    # lb_NumDoc12.grid(row=4, column=12, padx=5, pady=5)

    #---End Model frame---------------------------------------

    #---Analysis frame-----------------------------------------
    SimilarWords = Label(predictFrame, text='Top 10 similar words')
    SimilarWords.grid(row=0, column=0, padx=5, pady=5, columnspan = 24)
    CompareTitle = Label(predictFrame, text='Similarity between 2 inputs')
    CompareTitle.grid(row=14, column=0, padx=5, pady=5, columnspan = 24)
    # models = [cbow_400, cbow_2000, cbow_7975, skipgram_400, skipgram_2000, skipgram_7975, cbow_50epo, cbow_800epo, cbow_1000epo, skipgram_50epo, skipgram_800epo, skipgram_1000epo]
    models = [cbow, skipgram, fasttext_cbow, fasttext_skipgram]
    pos_column = 0
    pos = 0
    list_word = {}
    list_score = {}
    similar_word = {}
    WordTitle = {}
    PercentageTitle = {}
    ModelTitle = {}
    CompareSimilarity = {}
    for item in models:
        i = 0
        if len(input.split()) > 1:
            input_words = [w for w in InputPreprocess(input) if w in item.wv.index_to_key]
            
        else:
            input_words = input
        similar_word[pos] = item.wv.most_similar(input_words, topn = 10)
        ModelTitle[pos] = Label(predictFrame, text=name_model[pos], borderwidth=3, relief="solid")
        
        ModelTitle[pos].grid(row=1, column=pos_column, columnspan = 2)
        WordTitle[pos] = Label(predictFrame, text='Word')
        WordTitle[pos].grid(row=2, column=pos_column)
        PercentageTitle[pos] = Label(predictFrame, text='Scores')
        PercentageTitle[pos].grid(row=2, column=pos_column+1)
        for (word, score) in similar_word[pos]:
            list_word[i] = Label(predictFrame, text=word)
            list_word[i].grid(row=i+3, column=pos_column)
            list_score[i] = Label(predictFrame, text='%.4f' % score)
            list_score[i].grid(row=i+3, column=pos_column + 1)
            i += 1
        if len(compare1.split()) > 1 or len(compare2.split()) > 1:
            compare1_words= [w for w in InputPreprocess(compare1) if w in item.wv.index_to_key]
            print(compare1_words,"-----------\n")
            compare2_words = [w for w in InputPreprocess(compare2) if w in item.wv.index_to_key]
            print(compare2_words)
            similarity = '%.4f' % item.wv.n_similarity(compare1_words, compare2_words)
        else:
            compare1_words = removePunc(compare1)
            compare2_words = removePunc(compare2)
            similarity = '%.4f' % item.wv.similarity(compare1_words, compare2_words)
        CompareSimilarity[pos] = Label(predictFrame, text=similarity)
        CompareSimilarity[pos].grid(row=15, column=pos_column, columnspan = 2)
        pos_column += 2
        pos += 1

def Check(input, modelFrame, predictFrame, fasttext_cbow, fasttext_skipgram, cbow, skipgram):
    for widget in predictFrame.winfo_children():
        widget.destroy()
    for widget in modelFrame.winfo_children():
        widget.destroy()
    name_model = ["CBOW Word2vec", "Skipgram Word2vec", "Fasttext CBOW", "Fasttext Skipgram"]
    #---Model frame-------------------------------------------
    #Gastroenteritis
    ModelInfor = Label(modelFrame, text='MODEL INFOR')
    ModelInfor.grid(row=0, column=0, padx=5, pady=5)
    Vocabulary = Label(modelFrame, text='Vocabulary:')
    Vocabulary.grid(row=1, column=0, padx=5, pady=5)
    WindowSize = Label(modelFrame, text='Window Size:')
    WindowSize.grid(row=2, column=0, padx=5, pady=5)
    lb_Epoch = Label(modelFrame, text='Epochs:')
    lb_Epoch.grid(row=3, column=0, padx=5, pady=5)
    lb_Documents = Label(modelFrame, text='Training documents:')
    lb_Documents.grid(row=4, column=0, padx=5, pady=5)

    # Labels model 1
    lb_ModelName1 = Label(modelFrame, text=name_model[0])
    lb_ModelName1.grid(row=0, column=1, padx=5, pady=5)
    lb_NumVocab1 = Label(modelFrame, text=len(cbow.wv.index_to_key))
    lb_NumVocab1.grid(row=1, column=1, padx=5, pady=5)
    lb_NumWinSize1 = Label(modelFrame, text="5")
    lb_NumWinSize1.grid(row=2, column=1, padx=5, pady=5)
    lb_NumEpoch1 = Label(modelFrame, text='200 epochs')
    lb_NumEpoch1.grid(row=3, column=1, padx=5, pady=5)
    lb_NumDoc1 = Label(modelFrame, text='6205 documents')
    lb_NumDoc1.grid(row=4, column=1, padx=5, pady=5)

    # Labels model 2
    lb_ModelName2 = Label(modelFrame, text=name_model[1])
    lb_ModelName2.grid(row=0, column=2, padx=5, pady=5)
    lb_NumVocab2 = Label(modelFrame, text=len(skipgram.wv.index_to_key))
    lb_NumVocab2.grid(row=1, column=2, padx=5, pady=5)
    lb_NumWinSize2 = Label(modelFrame, text="5")
    lb_NumWinSize2.grid(row=2, column=2, padx=5, pady=5)
    lb_NumEpoch2 = Label(modelFrame, text='200 epochs')
    lb_NumEpoch2.grid(row=3, column=2, padx=5, pady=5)
    lb_NumDoc2 = Label(modelFrame, text='6205 documents')
    lb_NumDoc2.grid(row=4, column=2, padx=5, pady=5)

    # Labels model 3
    lb_ModelName3 = Label(modelFrame, text=name_model[2])
    lb_ModelName3.grid(row=0, column=3, padx=5, pady=5)
    lb_NumVocab3 = Label(modelFrame, text=len(fasttext_cbow.wv.index_to_key))
    lb_NumVocab3.grid(row=1, column=3, padx=5, pady=5)
    lb_NumWinSize3 = Label(modelFrame, text="5")
    lb_NumWinSize3.grid(row=2, column=3, padx=5, pady=5)
    lb_NumEpoch3 = Label(modelFrame, text='200 epochs')
    lb_NumEpoch3.grid(row=3, column=3, padx=5, pady=5)
    lb_NumDoc3 = Label(modelFrame, text='6205 documents')
    lb_NumDoc3.grid(row=4, column=3, padx=5, pady=5)

    # Labels model 4
    lb_ModelName4 = Label(modelFrame, text=name_model[3])
    lb_ModelName4.grid(row=0, column=4, padx=5, pady=5)
    lb_NumVocab4 = Label(modelFrame, text=len(fasttext_skipgram.wv.index_to_key))
    lb_NumVocab4.grid(row=1, column=4, padx=5, pady=5)
    lb_NumWinSize4 = Label(modelFrame, text="5")
    lb_NumWinSize4.grid(row=2, column=4, padx=5, pady=5)
    lb_NumEpoch4 = Label(modelFrame, text='200 epochs')
    lb_NumEpoch4.grid(row=3, column=4, padx=5, pady=5)
    lb_NumDoc4 = Label(modelFrame, text='6205 documents')
    lb_NumDoc4.grid(row=4, column=4, padx=5, pady=5)

    #---Analysis frame-----------------------------------------
    SimilarWords = Label(predictFrame, text='Top 10 similar words')
    SimilarWords.grid(row=0, column=0, padx=5, pady=5, columnspan = 24)
    # models = [cbow_400, cbow_2000, cbow_7975, skipgram_400, skipgram_2000, skipgram_7975, cbow_50epo, cbow_800epo, cbow_1000epo, skipgram_50epo, skipgram_800epo, skipgram_1000epo]
    models = [cbow, skipgram, fasttext_cbow, fasttext_skipgram]
    pos_column = 0
    pos = 0
    list_word = {}
    list_score = {}
    similar_word = {}
    WordTitle = {}
    PercentageTitle = {}
    ModelTitle = {}
    if len(input.split()) > 1:
        input_words = [w for w in InputPreprocess(input)]
        for item in models:
            i = 0
            if any(word not in item.wv.index_to_key for word in input_words):
                if pos<=1:
                    WordTitle[pos] = Label(predictFrame, text='Cannot find similar words')
                    WordTitle[pos].grid(row=2, column=pos_column, columnspan = 2)
                else:
                    similar_word[pos] = item.wv.most_similar(input_words, topn = 10)
                    WordTitle[pos] = Label(predictFrame, text='Word')
                    WordTitle[pos].grid(row=2, column=pos_column)
                    PercentageTitle[pos] = Label(predictFrame, text='Scores')
                    PercentageTitle[pos].grid(row=2, column=pos_column+1)
                    for (word, score) in similar_word[pos]:
                        list_word[i] = Label(predictFrame, text=word)
                        list_word[i].grid(row=i+3, column=pos_column)
                        list_score[i] = Label(predictFrame, text='%.4f' % score)
                        list_score[i].grid(row=i+3, column=pos_column + 1)
                        i += 1
            else:
                similar_word[pos] = item.wv.most_similar(input_words, topn = 10)
                WordTitle[pos] = Label(predictFrame, text='Word')
                WordTitle[pos].grid(row=2, column=pos_column)
                PercentageTitle[pos] = Label(predictFrame, text='Scores')
                PercentageTitle[pos].grid(row=2, column=pos_column+1)
                for (word, score) in similar_word[pos]:
                    list_word[i] = Label(predictFrame, text=word)
                    list_word[i].grid(row=i+3, column=pos_column)
                    list_score[i] = Label(predictFrame, text='%.4f' % score)
                    list_score[i].grid(row=i+3, column=pos_column + 1)
                    i += 1
            ModelTitle[pos] = Label(predictFrame, text=name_model[pos], borderwidth=3, relief="solid")
            ModelTitle[pos].grid(row=1, column=pos_column, columnspan = 2)
            pos_column += 2
            pos += 1
    else:
        input_words = input
        for item in models:
            i = 0
            if input_words not in item.wv.index_to_key:
                if pos<=1:
                    WordTitle[pos] = Label(predictFrame, text='Cannot find similar words')
                    WordTitle[pos].grid(row=2, column=pos_column, columnspan = 2)
                else:
                    similar_word[pos] = item.wv.most_similar(input_words, topn = 10)
                    WordTitle[pos] = Label(predictFrame, text='Word')
                    WordTitle[pos].grid(row=2, column=pos_column)
                    PercentageTitle[pos] = Label(predictFrame, text='Scores')
                    PercentageTitle[pos].grid(row=2, column=pos_column+1)
                    for (word, score) in similar_word[pos]:
                        list_word[i] = Label(predictFrame, text=word)
                        list_word[i].grid(row=i+3, column=pos_column)
                        list_score[i] = Label(predictFrame, text='%.4f' % score)
                        list_score[i].grid(row=i+3, column=pos_column + 1)
                        i += 1
            else:
                similar_word[pos] = item.wv.most_similar(input_words, topn = 10)
                WordTitle[pos] = Label(predictFrame, text='Word')
                WordTitle[pos].grid(row=2, column=pos_column)
                PercentageTitle[pos] = Label(predictFrame, text='Scores')
                PercentageTitle[pos].grid(row=2, column=pos_column+1)
                for (word, score) in similar_word[pos]:
                    list_word[i] = Label(predictFrame, text=word)
                    list_word[i].grid(row=i+3, column=pos_column)
                    list_score[i] = Label(predictFrame, text='%.4f' % score)
                    list_score[i].grid(row=i+3, column=pos_column + 1)
                    i += 1
            ModelTitle[pos] = Label(predictFrame, text=name_model[pos], borderwidth=3, relief="solid")
            ModelTitle[pos].grid(row=1, column=pos_column, columnspan = 2)
            pos_column += 2
            pos += 1