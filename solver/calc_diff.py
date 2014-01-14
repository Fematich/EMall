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

if __name__ == "__main__":
    #diff=$(python calc_diff.py $split_name $min_sim)
    split_name=sys.argv[1]
    min_sim=sys.argv[2]
    cev=evaluation.compare_events.find_one({"parameters.info.dataset" : "event_mall","parameters.info.splitname":split_name,"parameters.info.min_sim":min_sim,"parameters.big":big})
    diff = abs(float(cev['result']['precision'])-float(cev['result']['recall']))
    print diff