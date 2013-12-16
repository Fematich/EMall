#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Wed Dec 11 12:42:05 2013
"""
from mongostore.mongostore import MongoStore
import logging, subprocess, sys
from config import fgold, fevent_index, faevents
from utils import *

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("TODO")

def wccount(filename):
    out = subprocess.Popen(['wc', '-l', filename],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT
                         ).communicate()[0]
    return int(out.partition(b' ')[0])

def load_gold_events(goldpath=fgold):
    event_sets=[]
    old_id=-1
    with open(goldpath,'r') as goldfile:
        for line in goldfile:
            e_id,f_id=[int(nmbr) for nmbr in line.strip('\n').split(',')]
            if e_id!=old_id:
                event_sets.append(set([f_id]))
                old_id=e_id
            else:
                event_sets[-1].add(f_id)
    return event_sets

def load_event_sets(evfile=faevents):
    n_events=wccount(fevent_index)
    event_sets=[set([]) for tel in range(n_events)]
    with open(evfile,'r') as eventfile:
        for line in eventfile:
            blocks=line.strip('\n').split()
            f_id=int(blocks[0].split('=')[1])
            e_id=int(blocks[1].split('=')[1].split('/')[0])
            event_sets[e_id-1].add(f_id)
    return event_sets

@MongoStore
def compare_event(name,info,g_count,r_count,big):
    if big:
        gold_events=sig_set
    else:
        gold_events=mod_set
    ret={}
    ret['cos_sim']=cosine_similarity(gold_events[g_count],retrieved_events[r_count])
    ret['precision']=precision(gold_events[g_count],retrieved_events[r_count])
    ret['recall']=recall(gold_events[g_count],retrieved_events[r_count])
    ret['F1']=F1(ret['precision'],ret['recall'])
    return ret
    
@MongoStore
def compare_events(name,info,big):
    if big:
        gold_events=sig_set
    else:
        gold_events=mod_set
    ret={'cos_sim':0,'precision':0,'recall':0,'F1':0,}
    g_count=-1
    match_event=-1
    for g_event in gold_events:
        g_count+=1
        r_count=-1
        max_match=0
        for r_event in retrieved_events:
            r_count+=1
            if match(r_event,g_event)>max_match:
                match_event=r_count
                max_match=match(r_event,g_event)
        logger.info('comparing event %d with event %d'%(g_count,match_event))
        event_res=compare_event(name=name,info=info,g_count=g_count,r_count=match_event,big=big)
        for key in ret:
            ret[key]+=event_res[key]
    for key in ret:
        ret[key]=float(ret[key])/g_count
    return ret


if __name__ == '__main__':
    name=sys.argv[1]
    info = dict(x.split('=', 1) for x in sys.argv[2:])
    #load golden events
    gold_events=load_gold_events()
    #load retrieved events
    retrieved_events=load_event_sets()
    #match both
    sig_set=[st for st in gold_events if len(st)>=300]
    mod_set=[st for st in gold_events if 10<len(st)<=100]
    print compare_events(name=name,info=info, big=False)
    print compare_events(name=name, info=info, big=True)
    
    logger.info('done!!!')
