# -*- coding: utf8 -*-
"""
@author:    Matthias Feys (matthiasfeys@spurrit.com), Spurrit
@date:      %(date)
"""
import logging, sys, pymongo
import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("TODO")

db = pymongo.MongoClient()
evaluation=db.evaluation

def ndec(val):
    for res in [0,1,2,3,4,5,6]:
        if val==round(val*np.power(10,res))/np.power(10,res):
            return res

def cut_off(val,max_val,min_val):
    pw=max(ndec(min_val),ndec(max_val))
    cval=round(val*np.power(10,pw))/np.power(10,pw)
    if cval==max_val or cval==min_val:
        pw+=1
        cval=round(val*np.power(10,pw))/np.power(10,pw)
    return cval

if __name__ == "__main__":
    #min_sim=$(python calc_next_msim.py $split_name $min_msim $max_msim)
    split_name=sys.argv[1]
    min_msim=sys.argv[2]
    max_msim=sys.argv[3]
    cev_min=evaluation.compare_events.find_one({"parameters.info.dataset" : "event_mall","parameters.info.splitname":split_name,"parameters.info.min_sim":min_msim})
    cev_max=evaluation.compare_events.find_one({"parameters.info.dataset" : "event_mall","parameters.info.splitname":split_name,"parameters.info.min_sim":max_msim})
    new_msim=(float(cev_max['parameters']['info']['min_sim'])+float(cev_min['parameters']['info']['min_sim']))/2  
    print cut_off(new_msim, float(cev_max['parameters']['info']['min_sim']),float(cev_min['parameters']['info']['min_sim']))