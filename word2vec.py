import multiprocessing
from zipfDistribution import *
from nltk.tokenize import *
import json, os
import gensim, time
from gensim.models.callbacks import CallbackAny2Vec
from gensim.models.phrases import Phrases, Phraser
from gensim.models import FastText


num_document = 6205
filePath = "D:\IIR\HW1\Data\Pubmed_JSON\Pubmed_{}.json".format(num_document)
num_epoch = 200
win_size = 5
# By deriving a set from `raw_text`, we deduplicate the array
def Word2VecPreprocess(text):
    data = []
    for sentence in sent_tokenize(text):
        #Remove punctuation from text
        sentence = removePunc(sentence)
        #Remove stop-words from text
        text_without_stopword = removeStopWords(sentence)
        phrases = Phrases(text_without_stopword, min_count=10, progress_per=10000)
        bigram = Phraser(phrases)
        sentences = bigram[text_without_stopword]
        data.append(sentences)
    print(data)
    return data
def InputPreprocess(text):
    sentence = removePunc(text)
    text_without_stopword = removeStopWords(sentence)
    return text_without_stopword   
cores = multiprocessing.cpu_count() # Count the number of cores in a computer
def save_model(path, model, name):
    if not os.path.exists(path):
        print('save directories...', flush=True)
        os.makedirs(path)
    model.save(path + '\{}'.format(name))
class callback(CallbackAny2Vec):

  def __init__(self):
      self.epoch = 0
      self.loss_to_be_subed = 0

  def on_epoch_end(self, model):
      t = time.time()
      loss = model.get_latest_training_loss()
      loss_now = loss - self.loss_to_be_subed
      self.loss_to_be_subed = loss
      print('Loss after epoch {}: {}-----------'.format(self.epoch, loss_now), 'Time: ', time.time() - t)
      self.epoch += 1
def CBOWModel(data):
    t = time.time()
    #sg = 0 is CBOW model
    model1 = gensim.models.Word2Vec(
        data, 
        # min_count = 5,                        
        epochs = num_epoch,
        window=win_size,
        vector_size=300,
        sample=6e-5, 
        alpha=0.03, 
        min_alpha=0.0007, 
        workers=cores-5,
        compute_loss=True, 
        callbacks=[callback()],
        sg = 0)
    save_model("D:\IIR\HW1\Model1", model1, "cbow_{}doc_{}winsize_{}epochs".format(num_document, win_size, num_epoch))
    print("Total time: ", time.time() - t, "\n")
    return model1
def SkipgramModel(data):
    t = time.time()
    #sg = 1 is Skip gram Model
    model1 = gensim.models.Word2Vec(
        data, 
        # min_count = 5,                        
        epochs = num_epoch,
        window=win_size,
        vector_size=300,
        sample=6e-5, 
        alpha=0.03, 
        min_alpha=0.0007, 
        workers=cores-5,
        compute_loss=True, 
        callbacks=[callback()],
        sg = 1)
    save_model("D:\IIR\HW1\Model1", model1, "skipgram_{}doc_{}winsize_{}epochs".format(num_document, win_size, num_epoch))
    print("Total time: ", time.time() - t, "\n")
    return model1
def FasttextModel_Skipgram(data):
    t = time.time()
    model1 = FastText(
        data,                
        epochs = num_epoch,
        window=win_size,
        vector_size=300,
        sample=6e-5, 
        alpha=0.03, 
        min_alpha=0.0007, 
        workers=cores-5,
        sg = 1)
    save_model("D:\IIR\HW1\Model1", model1, "fastskipgram_{}doc_{}winsize_{}epochs".format(num_document, win_size, num_epoch))
    print("Total time: ", time.time() - t, "\n")
    return model1
def FasttextModel_CBOW(data):
    t = time.time()
    model1 = FastText(
        data,                
        epochs = num_epoch,
        window=win_size,
        vector_size=300,
        sample=6e-5, 
        alpha=0.03, 
        min_alpha=0.0007, 
        workers=cores-5,
        sg = 0)
    save_model("D:\IIR\HW1\Model1", model1, "fastcbow_{}doc_{}winsize_{}epochs".format(num_document, win_size, num_epoch))
    print("Total time: ", time.time() - t, "\n")
    return model1
def LoadJsonFiles(filePath):
    f = open(filePath, 'r', encoding="utf-8")
    data = json.load(f)
    fileFullText = ''
    for i, item in enumerate(data): 
        print("document: {}, Title: {}------------\n".format(i, item['Title']))       
        title = item['Title']
        abstract = item['Abstract']
        articleText = abstract + ' ' + title + '.' 
        fileFullText += articleText
    return fileFullText
# data = LoadJsonFiles(filePath)
# data = Word2VecPreprocess(data)
# cbowmodel = gensim.models.Word2Vec.load("D:\IIR\HW1\Model\cbow_7975doc_5winsize_200epochs")#
# cbowmodel = CBOWModel(data)
# skipgrammodel = SkipgramModel(data)
# fasttext_cbowmodel = FasttextModel_CBOW(data)
# fasttext_skipgrammodel = FasttextModel_Skipgram(data)
# fasttext_cbowmodel = FastText.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\fastcbow_6205doc_5winsize_200epochs")
#model = gensim.models.Word2Vec.load("D:\IIR\HW1\Model\cbow_5winsize_100epochs")
# print(model.wv.key_to_index.keys())
# print("CBOW:---------------------\n",cbowmodel.wv.most_similar("covid19", topn = 10))
# print("Skipgram:---------------------\n",skipgrammodel.wv.most_similar("covid19", topn = 10))
# print("FasttextModel_CBOW:---------------------\n",fasttext_cbowmodel.wv.most_similar("covid19", topn = 10))
# print("FasttextModel_Skipgram:---------------------\n",fasttext_skipgrammodel.wv.most_similar("covid19", topn = 10))
# cbow = gensim.models.Word2Vec.load("Model/cbow_model")
# print("CBOW:---------------------\n", cbow.wv.most_similar(positive=['spells'], topn = 5))
# print("Skip gram model:---------------------\n",SkipgramModel(raw_text).wv.most_similar(positive=['study'], topn = 5))

