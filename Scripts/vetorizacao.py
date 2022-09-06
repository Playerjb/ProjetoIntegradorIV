from asyncore import write
import pandas as pd
import sklearn as sk
#from doctest import DocTestFailure
import math
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


#----------- funções

def remove_punctuations(line):
    for character in string.punctuation:
        line = line.replace(character, "")
    return line

def writeFile(dict, archiveName):
    arquivo = open('.\DataBase\\'+archiveName+".txt",'w', encoding="utf8")
    for word, tf in dict.items():
        sentence = f"{word}:{tf}\n"
        arquivo.write(sentence)
    arquivo.close()

#------------- funções

# ------------------------- TF -------------------

filepath = ".\DataBase\Presidenciaveis.txt"
word_count = {}

with open(filepath, 'r', encoding="utf8") as fi:
    for line in fi:
        line = remove_punctuations(line)
        words = line.split()

        for word in words:
            word = word.lower()
            if word not in word_count:
                word_count[word] = 0
            word_count[word] += 1

#print(word_count)

#pd.DataFrame([word_count]) #não sei se essa linha ta funcionando

def computeTF(wordDict, doc):
    tfDict = {}
    corpusCount = len(doc)
    for word, count in wordDict.items():
        tfDict[word] = count/float(corpusCount)
    return(tfDict)

totalTf = computeTF(word_count, filepath)
writeFile(totalTf, "TF")

#--------------------------IDF --------------------------------
#não tenho ctz se o idf está certo
def computeIDF(docList):
    idfDict = {}
    N = len(docList)
    
    #idfDict = dict.fromkeys(docList[1].keys, 0)
    for word, val in docList.items():
        idfDict[word] = math.log10(N / (float(val) + 1))
        
    return(idfDict)

totalIDF = computeIDF(word_count)
writeFile(totalIDF, "IDF")

#-----------------------------TF - IDF -------------------

def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val*idfs[word]
    return(tfidf)

totalTfIdf = computeTFIDF(word_count, totalIDF)
writeFile(totalTfIdf, "TFIDF")


