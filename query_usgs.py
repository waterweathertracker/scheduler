import requests
import json

def parseWaterData(collection, state):
    req = requests.request('GET', 'http://waterservices.usgs.gov/nwis/iv/?format=json,1.1&stateCd=' +  state + '&parameterCd=00060,00065&siteType=ST,SP')
    dictData = req.json()
    for loc in dictData[u'value'][u'timeSeries']:
        if (len(loc[u'values']) > 0) and (len(loc[u'values'][0][u'value']) > 0):
            riverData={}
            riverData['name'] = loc[u'sourceInfo'][u'siteName'].encode('utf8')
            riverData['id'] = int(loc[u'sourceInfo'][u'siteCode'][0][u'value'].encode('utf8'))
            riverData['latitude'] = loc[u'sourceInfo'][u'geoLocation'][ u'geogLocation'][u'latitude']
            riverData['longitude'] = loc[u'sourceInfo'][u'geoLocation'][ u'geogLocation'][u'longitude']
            riverData['value'] = float(loc[u'values'][0][u'value'][0][u'value'].encode('utf8'))
            riverData['dateTime'] = loc[u'values'][0][u'value'][0][u'dateTime'].encode('utf8')
            riverData['stateId'] = loc[u'sourceInfo'][u'siteProperty'][2][u'value'].encode('utf8')
            riverData['countyId'] = loc[u'sourceInfo'][u'siteProperty'][3][u'value'].encode('utf8')
            riverData['state'] = state.upper()
            riverData['type'] = loc[u'variable'][u'unit'][u'unitAbbreviation'].encode('utf8')
            collection.append(riverData)

allRivers = []

stateList = ["al","ak","az","ar","ca","co","ct","de","dc","fl","ga","hi","id","il","in","ia","ks","ky","la","me","md","ma","mi","mn","ms","mo","mt","ne","nv","nh","nj","nm","ny","nc","nd","oh","ok","or","pa","ri","sc","sd","tn","tx","ut","vt","va","wa","wv","wi","wy","pr"]

for state in stateList:
    parseWaterData(allRivers,state)

print allRivers

with open('riverData.json', 'w') as outfile:
    json.dump(allRivers, outfile)
