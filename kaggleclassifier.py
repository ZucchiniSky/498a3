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
        tokens = processedFiles[filename]
        if fileIsJoke(filename):
            index = 2
            bayesData[0] += 1
            vocabTrue += len(tokens)
        else:
            vocabFalse += len(tokens)
        for token in tokens:
            if bayesData[index].get(token) is None:
                bayesData[index][token] = 0
            bayesData[index][token] += 1

def calcTokenProbability(index, classnum, token, joke):
    tokenCount = 0
    if index.get(token) is not None:
        tokenCount = index[token]
    if joke:
        vocab = vocabTrue
    else:
        vocab = vocabFalse
    return math.log(float(tokenCount + 1) / float(classnum + vocab))

def calcProbability(index, classnum, docnum, tokens, joke):
    global vocabTrue
    global vocabFalse
    prob = math.log(float(classnum) / docnum)
    for token in tokens:
        prob += calcTokenProbability(index, classnum, token, joke)
    return prob

def testNaiveBayes(file):
    global bayesData
    global processedFiles
    tokenSet = set(processedFiles[file])
    jokeProb = calcProbability(bayesData[2], bayesData[0], bayesData[1], tokenSet, True)
    mixProb = calcProbability(bayesData[3], bayesData[1] - bayesData[0], bayesData[1], tokenSet, False)
    if jokeProb > mixProb:
        return True
    else:
        return False

def fileIsJoke(filename):
    if re.match(".*joke", filename):
        return True
    if re.match(".*mix", filename):
        return False
    print "could not determine joke/mix"
    exit()

def main(args, rstop, stem):
    global processedFiles
    global bayesData
    if len(args) != 3:
        print "incorrect command line arguments"
    folderTraining = args[1]
    folderTest = args[2]
    trainingFiles = [folderTraining + filename for filename in listdir(folderTraining) if isfile(join(folderTraining, filename))]
    testFiles = [folderTest + filename for filename in listdir(folderTest) if isfile(join(folderTest, filename))]
    preprocess.generateStopwords()
    for filename in trainingFiles:
        sys.stderr.write("processing " + filename + "\n")
        filein = open(filename)
        processedFiles[filename] = preprocess.processText(filein.read(), rstop, stem)
        filein.close()
    for filename in testFiles:
        sys.stderr.write("processing " + filename + "\n")
        filein = open(filename)
        processedFiles[filename] = preprocess.processText(filein.read(), rstop, stem)
        filein.close()
    trainNaiveBayes(trainingFiles)
    print "File,Class"
    for filename in testFiles:
        sys.stderr.write("testing " + filename + "\n")
        answer = testNaiveBayes(filename)
        result = "joke"
        if not answer:
            result = "mix"
        print filename[len(folderTest):] + "," + result

if __name__ == '__main__':
    main(sys.argv, False, True)