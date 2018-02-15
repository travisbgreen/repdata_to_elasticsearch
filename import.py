#!/usr/bin/env python3
import json
import requests
import configparser
import sys
from datetime import datetime
from elasticsearch import Elasticsearch # sudo pip3 install elasticsearch

def get_ET_rep(config_dict):
    print(config_dict)
    r = requests.get(config_dict["url"].replace('oinkcode',config_dict["oinkcode"]))
    if config_dict["verbose"]: print(r.status_code)
    return r.json() # returns a dict

def load_ET_rep(repdata, config_dict):
    es = Elasticsearch() # defaults to localhost:9200
    es.indices.create(index=config_dict["es_index"], ignore=400) # ignore 400 (index already exists)
    for record, repdict in repdata.items():
        for category, score in repdict.items():
            if config_dict["verbose"]: print(record + ' ' + category + ':' + score)
            es.index(index=config_dict["es_index"], doc_type=config_dict["es_doc_type"], body={config_dict["es_rec_type"]: record, "timestamp": datetime.now(), "category": category, "score": score})    
    
def main():
    config = configparser.ConfigParser()
    config.read('./config.prv')

    repdata = get_ET_rep(dict(config["ETPro_domainrep"]))
    load_ET_rep(repdata, dict(config["ETPro_domainrep"]))
    
    repdata = get_ET_rep(dict(config["ETPro_iprep"]))
    load_ET_rep(repdata, dict(config["ETPro_iprep"]))

if __name__ == "__main__":
    main()
    