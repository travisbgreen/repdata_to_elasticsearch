#!/usr/bin/env python3
import json
import requests
from datetime import datetime
from elasticsearch import Elasticsearch # sudo pip3 install elasticsearch
debug = True

# download fresh copy:
r = requests.get('https://rules.emergingthreatspro.com/PUT_OINKCODE_HERE/reputation/domainrepdata.json')
if debug: print(r.status_code)
repdata = r.json()

# or from local file:
#repdata = json.load(open('./domainrepdata.json'))

es = Elasticsearch() # defaults to localhost:9200
es.indices.create(index='domainrep', ignore=400) # ignore code 400 (index already exists)

for domain, repdict in repdata.items():
    for category, score in repdict.items():
        if debug: print(domain + ' ' + category + ':' + score)
        es.index(index="domainrep", doc_type="repdata", body={"domain": domain, "timestamp": datetime.now(), "category": category, "score": score})
        
