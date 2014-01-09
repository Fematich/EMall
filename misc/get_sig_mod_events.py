# -*- coding: utf8 -*-
"""
@author:    Matthias Feys (matthiasfeys@spurrit.com), Spurrit
@date:      %(date)
"""
import logging, subprocess,os
from EMall.config import fmod_eventlist, fsig_eventlist, rel_event_dir, irrel_event_dir

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("get_sig_mod_events")

def wccount(filename):
    out = subprocess.Popen(['wc', '-l', filename],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT
                         ).communicate()[0]
    return int(out.partition(b' ')[0])

def get_eventlists():
    #significant events
    with open(fsig_eventlist,'w') as sig_eventf:
        for eventf in os.listdir(rel_event_dir):
            if wccount(os.path.join(rel_event_dir,eventf))>=300:
                sig_eventf.write("%s\n"%eventf)

    #moderate events
    with open(fmod_eventlist,'w') as mod_eventf:
        for eventf in os.listdir(rel_event_dir):
            if 10<wccount(os.path.join(rel_event_dir,eventf))<=100:
                mod_eventf.write("%s\n"%eventf)        

def filter_irrel_docsets():
    for eventf in os.listdir(irrel_event_dir):
        reldocs=set([])
        with open(os.path.join(rel_event_dir,eventf),'r') as rel_docf:
            for line in rel_docf:
                reldocs.add(int(line.strip('\n')))
        with open(os.path.join(irrel_event_dir,eventf),'r') as irrel_docf:
            with open(os.path.join('/home/mfeys/work/data/event_mall/eval/filtered',eventf),'w') as filtered_irrel_docf:
                for line in irrel_docf:
                    docid=int(line.strip('\n'))
                    if docid not in reldocs:
                        filtered_irrel_docf.write("%d\n"%docid)
if __name__ == '__main__':
#    get_eventlists()
    filter_irrel_docsets()