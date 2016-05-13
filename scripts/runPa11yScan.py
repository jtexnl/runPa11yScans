import os
import threading
import json
import collections
import csv
import datetime

class runner():
    def __init__(self):
        self.date = datetime.datetime.now().strftime('%Y%m%d')
        self.domains = self.loadDomains('../data/domains.csv')
        self.output = self.runScans(self.domains, 10)
    def loadDomains(self, path):
        with open(path) as infile:
            data = list(infile)
        clean = []
        for row in data[1:len(data)]:
            clean.append(row.replace('\n', '').split(','))
        return clean
    def scan(self, domain):
        resp = os.system('pa11y --ignore "warning;notice" --reporter csv ' + domain + ' > ' + domain + '.csv')
        return resp
    def loadAndClean(self, doc):
        with open(doc) as infile:
            data = list(infile)
        output = []
        for row in data:
            output.append(row.replace('"', '').replace('\n', '').split(','))
        return output
    def jsonify(self, dataSet):
        titleRow = dataSet[0]
        ln = len(titleRow) - 1
        outputList = []
        for row in dataSet[1:len(dataSet)]:
            output = collections.OrderedDict()
            for i in range(0, ln):
                output[titleRow[i]] = row[i]
            outputList.append(output)
        return outputList
    def runScans(self, domainList, numThreads):
        threads = numThreads
        masterData = {}
        jobs = []
        for row in domainList:
            site = row[0].lower()
            thread = threading.Thread(target = self.scan(site))
            temp = self.loadAndClean(site + '.csv')
            data = self.jsonify(temp)
            masterData[site] = data
            os.system('rm ' + site + '.csv')
        return masterData
    def writeJson(self, inputData, fileName):
        with open(fileName, 'w+') as outfile:
            json.dump(inputData, outfile, indent = 4)

if __name__ == '__main__':
    test = runner()
    test.writeJson(test.output, 'testRun.json')