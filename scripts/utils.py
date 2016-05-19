import collections
import json

def jsonify(dataSet):
    titleRow = dataSet[0]
    ln = len(titleRow) - 1
    outputList = []
    for row in dataSet[1:len(dataSet)]:
        output = collections.OrderedDict()
        for i in range(0, ln):
            output[titleRow[i]] = row[i]
        outputList.append(output)
    return outputList

def writeJson(inputData, fileName):
    with open(fileName, 'w+') as outfile:
        json.dump(inputData, outfile, indent = 4)