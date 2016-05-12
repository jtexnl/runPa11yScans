import os
import threading
import json

def scan(domain):
    resp = os.system('pa11y --ignore "warning;notice" --reporter json ' + domain + ' > ' + domain + '.json')
    return resp

def runScans(domainList, numThreads):
    threads = numThreads
    masterData = {}
    jobs = []
    for domain in domainList:
        thread = threading.Thread(target = scan(domain))
        data = json.load(open(domain + '.json'))
        masterData[domain] = data
        os.system('rm ' + domain + '.json')
    return masterData

def writeJson(inputData, fileName):
    with open(fileName, 'w+') as outfile:
        json.dump(inputData, outfile, indent = 4)

domainList = ['gsa.gov', 'state.gov', 'cio.gov', 'dhs.gov', 'defense.gov', 'abmc.gov', 'aging.gov']

if __name__ == '__main__':
    data = runScans(domainList, 10)
    writeJson(data, 'test.json')