#SCOTT BOMMARITO
#uniqname: zucchini
#ASSIGNMENT 3
#EECS 498 WN 2015

import sys
import re
import math
import preprocess
from os import listdir
from os.path import isfile, join

processedFiles = {}
bayesData = [0, 0, {}, {}]
vocabTrue = 0
vocabFalse = 0

def trainNaiveBayes(files):
    global bayesData
    global processedFiles
    global vocabTrue
    global vocabFalse
    bayesData = [0, 0, {}, {}]
    bayesData[1] = len(files)
    vocabTrue = 0
    vocabFalse = 0
    for filename in files:
        index = 3
        tokenSet = processedFiles[filename]
        if fileIsTruth(filename):
            index = 2
            bayesData[0] += 1
            vocabTrue += len(tokenSet)
        else:
            vocabFalse += len(tokenSet)
        for token in tokenSet:
            if bayesData[index].get(token) is None:
                bayesData[index][token] = 0
            bayesData[index][token] += 1

def calcTokenProbability(index, classnum, token, truth):
    tokenCount = 0
    if index.get(token) is not None:
        tokenCount = index[token]
    if truth:
        vocab = vocabTrue
    else:
        vocab = vocabFalse
    return math.log(float(tokenCount + 1) / float(classnum + vocab))

def calcProbability(index, classnum, docnum, tokens, truth):
    global vocabTrue
    global vocabFalse
    prob = math.log(float(classnum) / docnum)
    for token in tokens:
        prob += calcTokenProbability(index, classnum, token, truth)
    return prob

def testNaiveBayes(file):
    global bayesData
    global processedFiles
    tokenSet = set(processedFiles[file])
    truthProb = calcProbability(bayesData[2], bayesData[0], bayesData[1], tokenSet, True)
    lieProb = calcProbability(bayesData[3], bayesData[1] - bayesData[0], bayesData[1], tokenSet, False)
    if truthProb > lieProb:
        return True
    else:
        return False

def fileIsTruth(filename):
    if re.match(".*true", filename):
        return True
    if re.match(".*lie", filename):
        return False
    print "could not determine true/lie"
    exit()

def tokenSort(x, y):
    if y[1] > x[1]:
        return 1
    if y[1] == x[1]:
        return 0
    return -1

def main(args, rstop, stem, output):
    global processedFiles
    global bayesData
    if len(args) != 2:
        print "incorrect command line arguments"
    folder = args[1]
    files = [folder + filename for filename in listdir(folder) if isfile(join(folder, filename))]
    preprocess.generateStopwords()
    for filename in files:
        filein = open(filename)
        processedFiles[filename] = preprocess.processText(filein.read(), rstop, stem)
        filein.close()
    correct = 0
    total = 0
    for filename in files:
        trainNaiveBayes([file for file in files if file != filename])
        answer = testNaiveBayes(filename)
        result = "true"
        if not answer:
            result = "lie"
        if (not fileIsTruth(filename) and not answer) or (fileIsTruth(filename) and answer):
            correct += 1
        total += 1
        print filename + " " + result
    print str(correct) + " / " + str(total) + " = " + str(float(correct)/float(total))
    if output:
        trainNaiveBayes(files)
        truthList = []
        lieList = []
        tokens = set()
        for key in bayesData[2]:
            tokens.add(key)
        for key in bayesData[3]:
            tokens.add(key)
        for token in tokens:
            truthList.append([token, calcTokenProbability(bayesData[2], bayesData[0], token, True)])
            lieList.append([token, calcTokenProbability(bayesData[3], bayesData[1] - bayesData[0], token, False)])
        truthList.sort(tokenSort)
        lieList.sort(tokenSort)
        for i in range(0, 10):
            print "most likely truth word no " + str(i+1) + ": " + str(truthList[i])
        for i in range(0, 10):
            print "most likely lie word no " + str(i) + ": " + str(lieList[i])
        tokenList = list(tokens)
        tokenList.sort()
        for token in tokenList:
            sum = 0
            if bayesData[2].get(token) is not None:
                sum += bayesData[2][token]
            if bayesData[3].get(token) is not None:
                sum += bayesData[3][token]
            print token + ": " + str(sum)


if __name__ == '__main__':
    main(sys.argv, False, False, True)