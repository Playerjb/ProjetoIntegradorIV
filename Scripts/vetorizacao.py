"""
Installers
pandas: $pip install pandas
K-means: $pip install -U scikit-learn
Matplotlib: $python -m pip install -U matplotlib
nltk: $pip install nltk
"""

from asyncore import write
import pandas as pd
from doctest import DocTestFailure
import math
import string
from sklearn.cluster import KMeans
from sklearn.datasets._samples_generator import make_blobs

#----------- importando bibliotecas para tratar as palavras

#from worldcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from nltk.tokenize import word_tokenize
import nltk

#----------- funções

def remove_punctuations(line):
    for character in string.punctuation:
        line = line.replace(character, "")
    return line

def writeFile(dict, archiveName):
    arquivo = open(archiveName+".txt",'w')
    for word, tf in dict.items():
        sentence = f"{word}:{tf}\n"
        arquivo.write(sentence)
    arquivo.close()

def writeCSV(df, archiveName):
    f = open(".\DataBase\\"+archiveName+".csv", 'w', newline='', encoding="utf8")
    df.to_csv(".\DataBase\\"+archiveName+".csv", encoding="utf8", sep=';')


def countWords(wordsDoc, line): 
    wordsCopy = wordsDoc.copy() 
    words = line.split()
    for word in words:
        word = word.lower()
        wordsCopy[word] += 1
    return wordsCopy


#------------- funções de ponderação/vetorização

def computeTF(wordDict, doc):
    tfDict = {}
    corpusCount = len(doc)
    for word, count in wordDict.items():
        tfDict[word] = round(count/float(corpusCount), 3)
    return(tfDict)

def computeIDF(docList):
    idfDict = {}
    N = len(docList)
    
    #idfDict = dict.fromkeys(docList[1].keys, 0)
    for word, val in docList.items():
        idfDict[word] = round(math.log10(N / (float(val) + 1)), 3)
        
    return(idfDict)

def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = round(val*idfs[word], 3)
    return(tfidf)

#--------- pegando cada palavra dos posts 

filepath = ".\DataBase\Governamentais.txt"
word_count = {}
lines = []


with open(filepath, 'r', encoding="utf8") as fi:
    for line in fi:
        line = remove_punctuations(line)
        lines.append(line)
        words = line.split()

        for word in words:
            word = word.lower()
            if word not in word_count:
                word_count[word] = 0

#-----criando listas auxiliares
listTF = {}
listIDF = {}
listTF_IDF = {}
tweets = {}

#ponderação/vetorização
rowCount = 0
for line in lines:
    rowCount += 1
    rowName = "Tweet" + str(rowCount)
    totalCount = countWords(word_count, line)
    totalTF = computeTF(totalCount, line)
    listTF[rowName] = totalTF
    totalIDF = computeIDF(totalCount)
    listIDF[rowName] = totalIDF
    totalTF_IDF = computeTFIDF(totalCount, totalIDF)
    listTF_IDF[rowName] = totalTF_IDF
    tweets[rowName] = line

#------------ criando os dataframes

dfTF = pd.DataFrame.from_dict(listTF, orient='index', columns=word_count.keys())
dfIDF = pd.DataFrame.from_dict(listIDF, orient='index', columns=word_count.keys())
dfTF_IDF = pd.DataFrame.from_dict(listTF_IDF, orient='index', columns=word_count.keys())
dfTweets = pd.DataFrame.from_dict(tweets, orient='index', columns=['TEXT'])

#escrevendo no CSV

writeCSV(dfTweets, "Relação Tweets com Dataframe")
writeCSV(dfTF, "TF")
writeCSV(dfIDF, "IDF")
writeCSV(dfTF_IDF, "TF_IDF")

#clusterização --- TF

#validar com o professor
x = np.array(dfTF)
kmeans_model = KMeans (n_clusters=3, random_state=0, init='random', n_init=10, max_iter=300, tol=1e-04).fit(x) #dps perguntar pro prof se precisa de todos esses parametros
kmeans_model.labels_
kmeans_model.cluster_centers_

mydict = {i: np.where(kmeans_model.labels_ == i)[0] for i in range(kmeans_model.n_clusters)}
dictlist = []
for key, value in mydict.items():
    temp = [key,value]
    dictlist.append(temp)
