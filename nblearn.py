
# use this file to learn naive-bayes classifier
# Expected: generate nbmodel.txt



from __future__ import division
import os
import pickle
import re
import sys

N = 23
input_path = os.path.join(os.getcwd(),"op_spam_training_data")
model_file = "nbmodel.txt"
curDir = os.getcwd()
stopDic = [""]
#stopDic = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

class modelPara:
    def __init__(self, Word, posWord, negWord, decWord, truWord, posP, negP, decP,
                 truP, vocCount, posCount, negCount, decCount, truCount):
        self.Word = Word
        self.posWord = posWord
        self.negWord = negWord
        self.decWord = decWord
        self.truWord = truWord
        self.posP = posP
        self.negP = negP
        self.decP = decP
        self.truP = truP
        self.vocCount = vocCount
        self.posCount = posCount
        self.negCount = negCount
        self.decCount = decCount
        self.truCount = truCount



def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    return False

def loadvoc(dirName):

    voc = []
    voc_set = set()
    Word = {}
    negWord = {}
    posWord = {}
    decWord = {}
    truWord = {}
    count = 0
    posDocNum = 0 #positive docnum
    negDocNum = 0
    decDocNum = 0
    truDocNum = 0
    posCount = 0   #positive wordcount
    negCount = 0
    decCount = 0
    truCount = 0
    vocCount = 0

    for subs in os.listdir(dirName):         #neg,pos
        if (os.path.isdir(os.path.join(dirName,subs))):
            for sub in os.listdir(os.path.join(dirName,subs)):         #dec,tru
                for fold in os.listdir(os.path.join(dirName,subs,sub)):
                    for txt in os.listdir(os.path.join(dirName,subs,sub,fold)):
                        if ("positive" in subs):
                            posDocNum = posDocNum + 1
                        elif ("negative" in subs):
                            negDocNum = negDocNum + 1
                        if ("deceptive" in sub):
                            decDocNum = decDocNum + 1
                        elif ("truthful" in sub):
                            truDocNum = truDocNum + 1
                        with open(os.path.join(dirName,subs,sub,fold,txt),'r') as f:
                            for line in f.readlines():
                                # line = line.replace(',',' ').replace('.',' ').replace('!',' ').replace('(',' ').replace(')',' ') \
                                #     .replace(':',' ').replace('"',' ').replace('?',' ').replace('--',' ').replace('/',' ').strip('\n').strip('.').strip().lower()
                                line= line.lower()
                                line = "#HEAD#" + line + "#END#"
                                # wordlist = line.split(' ')
                                wordlist = re.split("\W+",line)
                                for i in range(len(wordlist)):
                                    if is_number(wordlist[i]):
                                        wordlist[i] = "#NUM#"
                                for n in range(1,N+1):
                                    for i in range(len(wordlist)- n + 1):
                                        word = ' '.join(wordlist[i:i + n])
                                        if word not in stopDic:
                                            if (Word.has_key(word)):
                                                Word[word] = Word[word] + 1
                                            else:
                                                Word[word] = 1

                                            if ("positive" in subs):
                                                posCount = posCount + 1
                                                if (posWord.has_key(word)):
                                                    posWord[word] = posWord[word] + 1
                                                else:
                                                    posWord[word] = 1
                                            elif ("negative" in subs):
                                                negCount = negCount + 1
                                                if (negWord.has_key(word)):
                                                    negWord[word] = negWord[word] + 1
                                                else:
                                                    negWord[word] = 1
                                            if ("deceptive" in sub):
                                                decCount = decCount + 1
                                                if (decWord.has_key(word)):
                                                    decWord[word] = decWord[word] + 1
                                                else:
                                                    decWord[word] = 1
                                            elif ("truthful" in sub):
                                                truCount = truCount + 1
                                                if (truWord.has_key(word)):
                                                    truWord[word] = truWord[word] + 1
                                                else:
                                                    truWord[word] = 1
                                        voc.append(word)





                                count = count + 1
    voc_set = set(voc)
    print len(voc_set)


    vocCount = len(voc_set)
    posP = posDocNum / count
    negP = negDocNum / count
    decP = decDocNum / count
    truP = truDocNum / count



    model = modelPara(voc, posWord, negWord, decWord, truWord, posP, negP, decP,
                      truP, vocCount, posCount, negCount, decCount, truCount)
    with open(os.path.join(curDir, model_file), 'wb')as f:
        pickle.dump(model, f)

    return

if __name__ == "__main__":
    model_file = "nbmodel.txt"
    input_path = str(sys.argv[1])
    # input_path = sys.argv[0]
    # voc = set()
    # readStop(os.path.join(os.getcwd(),"stop"))
    loadvoc(input_path)