import os
import threading
import json
import collections
import csv
import datetime
import utils

mistakes = []

class runner():
    def __init__(self):
        self.date = datetime.datetime.now().strftime('%Y%m%d')
        self.domains = self.loadDomains('../data/domains.csv')
        #self.domains = ['gsa.gov', 'dhs.gov', 'cio.gov', 'eop.gov', 'whitehouse.gov', 'aids.gov', 'house.gov', 'senate.gov', 'americorps.gov', 'arctic.gov', 'amtrakoig.gov', 'bea.gov', 'bpa.gov']
        self.output = self.runScans(self.domains)
    #Loads the domain file and cleans up the output, yielding a clean list
    def loadDomains(self, path):
        with open(path) as infile:
            data = list(infile)
        clean = []
        for row in data[1:len(data)]:
            clean.append(row.replace('\n', '').split(','))
        return clean
    #Runs the bash command to scan a single domain, yielding a csv report. json is also available, but is not working on AWS.
    def scan(self, domain):
        resp = os.system('pa11y --ignore "warning;notice" --reporter csv ' + domain + ' > ' + domain + '.csv')
        return resp
    #Function for loading one of the scanner output reports and cleaning it up
    def loadAndClean(self, doc):
        with open(doc) as infile:
            data = list(infile)
        output = []
        for row in data:
            output.append(row.replace('"', '').replace('\n', '').split(','))
        return output
    #Function to run the scanner on a list of domains. Threading functions need some work. Outputs the data as a dict.
    def runScans(self, domainList):
        masterData = {}
        jobs = []
        for row in domainList:
            site = row.lower()
            try:
                self.scan(site)
                temp = self.loadAndClean(site + '.csv')
                try:
                    data = utils.jsonify(temp)
                except IndexError:
                    data = 'File Error'
                masterData[site] = data
                os.system('rm ' + site + '.csv')
            except:
                print('error: ' + site)
                mistakes.append(site)
        return masterData

if __name__ == '__main__':
    test = runner()
    utils.writeJson(test.output, 'scanResults.json')
    for row in mistakes:
        print(row)