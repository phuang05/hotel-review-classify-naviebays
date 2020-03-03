

# use this file to classify using naive-bayes classifier
# Expected: generate nboutput.txt

from __future__ import division


from nblearn import modelPara
from numpy import *
import pickle
import sys
import os
import re
import nblearn

N  = 2
dir = os.path.join(os.getcwd(),"op_spam_training_data")
inputDir = os.path.join(os.getcwd(),"fold1")
pscount = 0
decount = 0
c = 0
trcount = 0
necount = 0
stopDic = [""]
#stopDic=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]



def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    return False


def loadfile(file):
    voc_set = set()
    inputWord = {}


    with open(file,'r') as f:
        for line in f.readlines():
            line = line.lower()
            # line = line.replace(',',' ').replace('.',' ').replace('!',' ').replace('(',' ').replace(')',' ') \
            #     .replace(':',' ').replace('"',' ').replace('?',' ').replace('--',' ').replace('/',' ').strip('\n').strip('.').strip().lower()
            # wordlist = line.split(' ')
            line = "#HEAD#" + line + "#END#"
            wordlist = re.split("\W+",line)
            for i in range(len(wordlist)):
                if is_number(wordlist[i]):
                    wordlist[i] = "#NUM#"
            for n in range(1,N+1):
                for i in range(len(wordlist) - n + 1):
                    word = ' '.join(wordlist[i:i + n])
                    if (inputWord.has_key(word)):
                        inputWord[word] = inputWord[word] + 1
                    else:
                        inputWord[word] = 1

                # count = count + 1
    # print inputWord
    return inputWord


def cal(inputWord,model,inputpath):
    # print negCount
    wordPosP = -log(model.posP)
    wordNegP = -log(model.negP)
    wordDecP = -log(model.decP)
    wordTruP = -log(model.truP)




    for word in inputWord:
        if word not in stopDic:
            # print posCount+vocCount
            if model.posWord.has_key(word):
                wordPosP = wordPosP + (-log((model.posWord[word] + 1) / (model.posCount + model.vocCount)))
            else:
                wordPosP = wordPosP + (-log((1) / (model.posCount + model.vocCount)))
            if (model.negWord.has_key(word)):
                wordNegP = wordNegP + (-log((model.negWord[word] + 1) / (model.negCount + model.vocCount)))
            else:
                wordNegP = wordNegP + (-log((1) / (model.negCount + model.vocCount)))
            if model.decWord.has_key(word):
                wordDecP = wordDecP + (-log((model.decWord[word] + 1) / (model.decCount + model.vocCount)))
            else:
                wordDecP = wordDecP + (-log((1) / (model.decCount + model.vocCount)))
            if (model.truWord.has_key(word)):
                wordTruP = wordTruP + (-log((model.truWord[word] + 1) / (model.truCount + model.vocCount)))
            else:
                wordTruP = wordTruP + (-log((1) / (model.truCount + model.vocCount)))


    if (wordTruP < wordDecP):
        output.write("truthful ")
    else:
        output.write("deceptive ")
    if (wordPosP < wordNegP):
        output.write("positive ")
    else:
        output.write("negative ")
        #c = c + 1
    output.write(inputpath + " \n")
    return


if __name__ == "__main__":
    model_file = "nbmodel.txt"
    output_file = "nboutput.txt"
    input_path = str(sys.argv[1])
    print input_path
    pkl_file = open(os.path.join(os.getcwd(), model_file),'rb')
    model = pickle.load(pkl_file)
    output =  open(os.path.join(os.getcwd(),output_file),"w")
    inputDir = os.path.join(os.getcwd(),input_path)
    for subs in os.listdir(inputDir):         #neg,pos
        if (os.path.isdir(os.path.join(inputDir,subs))):
            for sub in os.listdir(os.path.join(inputDir,subs)):         #dec,tru
                for fold in os.listdir(os.path.join(inputDir,subs,sub)):
                    for txt in os.listdir(os.path.join(inputDir,subs,sub,fold)):
                        inputpath = os.path.join(inputDir,subs,sub,fold,txt)
                        inputWord = loadfile(inputpath)
                        cal(inputWord, model,inputpath)

