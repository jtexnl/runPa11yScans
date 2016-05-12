import os
import threading

def scan(domain):
    resp = os.system('pa11y --ignore "warning;notice" --reporter json ' + domain + ' > ' + domain + '.json')
    return resp

def runScans(domainList):
    masterData = {}
    for domain in domainList:
        scan(domain)
        data = json.load(open(domain + '.json'))
        masterData[domain] = data
        os.system('rm ' + domain + '.json')
    return masterData

domainList = ['gsa.gov', 'state.gov', 'cio.gov', 'dhs.gov']

if __name__ == '__main__':
    runScans(domainList)