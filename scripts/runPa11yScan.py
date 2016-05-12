import os
import threading
import json
import collections

def scan(domain):
    resp = os.system('pa11y --ignore "warning;notice" --reporter csv ' + domain + ' > ' + domain + '.csv')
    return resp

def loadAndClean(doc):
    with open(doc) as infile:
        data = list(infile)
    output = []
    for row in data:
        output.append(row.replace('"', '').replace('\n', '').split(','))
    return output

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

def runScans(domainList, numThreads):
    threads = numThreads
    masterData = {}
    jobs = []
    for domain in domainList:
        thread = threading.Thread(target = scan(domain))
        temp = loadAndClean(domain + '.csv')
        data = jsonify(temp)
        masterData[domain] = data
        os.system('rm ' + domain + '.csv')
    return masterData

def writeJson(inputData, fileName):
    with open(fileName, 'w+') as outfile:
        json.dump(inputData, outfile, indent = 4)

domainList = ['gsa.gov', 'state.gov', 'cio.gov', 'dhs.gov', 'defense.gov', 'abmc.gov', 'aging.gov']

if __name__ == '__main__':
    data = runScans(domainList, 10)
    writeJson(data, 'test.json')