# -*- coding: utf8 -*-
"""
@author:    Matthias Feys (matthiasfeys@spurrit.com), Spurrit
@date:      %(date)
"""
#sys.path.insert(0, os.path.abspath(".."))
import logging, os
from datetime import datetime

from whoosh.index import open_dir
from whoosh.query import DateRange
from EMall.config import indexdir,fgold, rel_event_dir, irrel_event_dir
from EMall.utils import load_dates

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("get_irrelevant_docs")

# load date-ranges for events from event?
#def load_date_ranges(event_dates_path=feventdates):
#    dates={}
#    with open(event_dates_path,'r') as dates_f:
#        for line in dates_f:
#            vals=[nmbr for nmbr in line.strip('\n').split(',')]
#            print vals[1],vals[2]
#            dates[int(vals[0])]=(datetime.strptime(vals[1],"%Y%m%d"),datetime.strptime(vals[2],"%Y%m%d"))
#    return dates
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

def load_date_ranges():
    gold_events=load_gold_events()
    gold_dates={}
    for event_id in gold_events:
        dateset=set([])
        with open(os.path.join(rel_event_dir,str(event_id)),'w') as ev_file:
            for doc in gold_events[event_id]:
                try:
                    dateset.add(dates[doc])
                    ev_file.write('%d\n'%doc)
                except KeyError:
                    continue
        gold_dates[event_id]=(min(dateset),max(dateset))
    return gold_dates
        
    
if __name__ == "__main__":
    dates=load_dates()
    dateranges=load_date_ranges()
    ix = open_dir(indexdir)
    searcher=ix.searcher()
    for event_id in dateranges:
        daterange=dateranges[event_id]
        with open(os.path.join(irrel_event_dir,str(event_id)),'w') as ev_file:
            res=searcher.search(DateRange("date", datetime.strptime(str(daterange[0]),"%Y%m%d"),datetime.strptime(str(daterange[1]),"%Y%m%d"),endexcl=False),limit=None,sortedby='date')
            for doc in res:
                ev_file.write('%d\n'%doc['did'])

