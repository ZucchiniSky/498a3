import sys
import re
import preprocess
from os import listdir
from os.path import isfile, join

processedFiles = {}
bayesData = [0, 0, {}, {}]
vocab = 0

def trainNaiveBayes(files):
    global bayesData
    global processedFiles
    global vocab
    bayesData = [0, 0, {}, {}]
    bayesData[1] = len(files)
    vocab = 0
    tokens = set()
    for filename in files:
        index = 3
        if fileIsTruth(filename):
            index = 2
            bayesData[0] += 1
        tokenSet = processedFiles[filename]
        for token in tokenSet:
            if bayesData[index].get(token) is None:
                bayesData[index][token] = 0
            bayesData[index][token] += 1
            tokens.add(token)
    vocab = len(tokens)

def calcProbability(index, classnum, docnum, tokens):
    global vocab
    prob = float(classnum) / docnum
    for token in tokens:
        tokenCount = 0
        if index.get(token) is not None:
            tokenCount = index[token]
        prob *= float(tokenCount + 1) / float(classnum + vocab)
    return prob

def testNaiveBayes(file):
    global bayesData
    global processedFiles
    tokenSet = processedFiles[file]
    truthProb = calcProbability(bayesData[2], bayesData[0], bayesData[1], tokenSet)
    lieProb = calcProbability(bayesData[3], bayesData[1] - bayesData[0], bayesData[1], tokenSet)
    if truthProb > lieProb:
        return True
    else:
        return False

def fileIsTruth(filename):
    if re.match("truth", filename):
        print filename + " is true"
        return True
    if re.match("lie", filename):
        print filename + " is lie"
        return False

def main(args, rstop, stem):
    global processedFiles
    if len(args) != 2:
        print "incorrect command line arguments"
    folder = args[1]
    files = [folder + filename for filename in listdir(folder) if isfile(join(folder, filename))]
    for filename in files:
        filein = open(filename)
        processedFiles[filename] = set(preprocess.processText(filein.read(), rstop, stem))
        filein.close()
    correct = 0
    total = 0
    for filename in files:
        trainNaiveBayes([file for file in files if file != filename])
        answer = testNaiveBayes(filename)
        result = "truth"
        if not fileIsTruth(filename):
            result = "lie"
        if (not fileIsTruth(filename) and not answer) or (fileIsTruth(filename) and answer):
            correct += 1
        total += 1
        print filename + " " + result
    print str(correct) + " / " + str(total) + " = " + str(correct/total)

if __name__ == '__main__':
    main(sys.argv, False, False)