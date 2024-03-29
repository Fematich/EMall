# -*- coding: utf8 -*-
"""
@author:    Matthias Feys (matthiasfeys@spurrit.com), Spurrit
@date:      %(date)
"""
import logging, sys, pymongo

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("TODO")

db = pymongo.MongoClient()
evaluation=db.evaluation
big=True

def diffsign(cev1,cev2):
    val=(float(cev1['result']['precision'])-float(cev1['result']['recall']))*(float(cev2['result']['precision'])-float(cev2['result']['recall']))
    if val<0:
        return True
    else:
        return False

if __name__ == "__main__":
    #max_msim=$(python calc_min_msim.py $split_name $min_sim $min_msim $max_msim)
    split_name=sys.argv[1]
    min_sim=sys.argv[2]
    min_msim=sys.argv[3]
    max_msim=sys.argv[4]
    if float(min_msim)==0:
        cev_min={"result":{"precision":0,"recall":1},"parameters":{"info":{"min_sim":0}}}
    else:
        cev_min=evaluation.compare_events.find_one({"parameters.info.dataset" : "event_mall","parameters.info.splitname":split_name,"parameters.info.min_sim":min_msim,"parameters.big":big})
    if float(max_msim)==0.6:
        cev_max={"result":{"precision":1,"recall":0},"parameters":{"info":{"min_sim":0.6}}}
    else:
        cev_max=evaluation.compare_events.find_one({"parameters.info.dataset" : "event_mall","parameters.info.splitname":split_name,"parameters.info.min_sim":max_msim,"parameters.big":big})
    cev_new=evaluation.compare_events.find_one({"parameters.info.dataset" : "event_mall","parameters.info.splitname":split_name,"parameters.info.min_sim":min_sim,"parameters.big":big})
    if diffsign(cev_min,cev_new):
        print cev_min['parameters']['info']['min_sim']
    else:
        print cev_new['parameters']['info']['min_sim']