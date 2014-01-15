# -*- coding: utf8 -*-
"""
@author:    Matthias Feys (matthiasfeys@spurrit.com), Spurrit
@date:      %(date)
"""
import logging, pymongo,os, subprocess
import cPickle as pickle
from datetime import datetime
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("update mongo")

db = pymongo.MongoClient()
evaluation=db.evaluation

event_dirs=["/media/DB58-DB0C/event_mall/events","/home/mfeys/work/data/events"]
fgold=os.path.join('/home/mfeys/work/data/event_mall','event_file.csv')

def wccount(filename):
    out = subprocess.Popen(['wc', '-l', filename],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT
                         ).communicate()[0]
    return int(out.partition(b' ')[0])

def load_gold_events(goldpath=fgold):
    event_sets={}
    old_id=-1
    with open(goldpath,'r') as goldfile:
        for line in goldfile:
            e_id,f_id=[int(nmbr) for nmbr in line.strip('\n').split(',')]
            if e_id!=old_id:
                event_sets[e_id]=set([f_id])
                old_id=e_id
            else:
                event_sets[e_id].add(f_id)
    return event_sets

def add_g_ids():
    gold_events=load_gold_events()
    sig_set=[st for st in gold_events if len(gold_events[st])>=300]
    mod_set=[st for st in gold_events if 10<len(gold_events[st])<=100]
    compare_event=evaluation.compare_event
    for cev in compare_event.find({"parameters.info.dataset" : "event_mall"}):
        print cev
        if cev["parameters"]["big"]:
            g_id=sig_set[cev['parameters']['g_count']]
        else:
            g_id=mod_set[cev['parameters']['g_count']]
        compare_event.update({"_id":cev["_id"]}, {"$set": {"parameters.g_id":g_id }})

def get_n_events(name):
    if os.path.exists(os.path.join(event_dirs[0],name,'events_index')):
        return wccount(os.path.join(event_dirs[0],name,'events_index'))
    elif os.path.exists(os.path.join(event_dirs[1],name,'events_index')):
        return wccount(os.path.join(event_dirs[1],name,'events_index'))
    else:
        logger.info('no eventdir found')
def add_n_retrieved_events():
    compare_events=evaluation.compare_events
    for cev in compare_events.find({"parameters.info.dataset" : "event_mall","result.n_events":{"$exists":0}}):
        compare_events.update({"_id":cev["_id"]}, {"$set": {"result.n_events":get_n_events(cev["parameters"]["name"]) }}) 

def removeduplicates():
    compare_events=evaluation.compare_events
    compare_event=evaluation.compare_event
    for cev in compare_events.find({"parameters.info.dataset" : "event_mall"}):
        events=set([])
        for ce in compare_event.find({"parameters.info.dataset" : "event_mall","parameters.name":cev['parameters']['name']}):
            if ce["parameters"]["g_id"] in events:
                max_date='1990-01-01'            
                for ev in compare_event.find({"parameters.info.dataset" : "event_mall","parameters.name":cev['parameters']['name'],"parameters.g_id":ce["parameters"]["g_id"]}):
                    if ev["timestamp"]>max_date:
                        max_date=ev["timestamp"]
                print 'removing %s from %s with timestamp %s'%(ce["parameters"]["g_id"],cev['parameters']['name'],ev["timestamp"])
                compare_event.remove({"parameters.info.dataset" : "event_mall","parameters.name":cev['parameters']['name'],"parameters.g_id":ce["parameters"]["g_id"],"timestamp":max_date})
            events.add(ce["parameters"]["g_id"])


if __name__ == '__main__':   
#    add_g_ids()
    removeduplicates()