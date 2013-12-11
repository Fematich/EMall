#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Dec 10 13:50:55 2013
"""

import os,logging,re,shutil
from datetime import datetime

import whoosh
from whoosh.fields import Schema, TEXT, NUMERIC, DATETIME,STORED, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.query import DateRange,Require
from whoosh.formats import Frequency
from config import indexdir, burstindexdir, fbursts
from datetime import datetime


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("Indexer")

def IndexBursts():
    schema = Schema(
                        start_date=DATETIME(stored=True,sortable=True),
                        end_date=DATETIME(stored=True,sortable=True),                        
                        cnt=STORED,
                        nv=STORED,
                        start=STORED,
                        end=STORED,
                        term=STORED
                        )
    #create index
    if not os.path.exists(burstindexdir):
        os.mkdir(burstindexdir)
        ix = create_in(burstindexdir, schema)
    else:
        logger.info('burstindex already exists! DELETING')
        return

    cnt=0
    writer = ix.writer(limitmb=1500)
    with open(fbursts,'r') as bursts:
        for burst in bursts:
            cnt+=1
            if cnt%1000==0:
                print 'indexed %d K bursts'%(cnt/1000)
            nv,start,end,term,startd,endd=burst.split()
            start_date=datetime.strptime(startd,'%Y%m%d').replace(hour=0, minute=0)
            end_date=datetime.strptime(endd,'%Y%m%d').replace(hour=0, minute=0)
            writer.add_document(start_date=start_date,
                                end_date=end_date,
                                cnt=cnt,
                                nv=nv,
                                start=start,
                                end=end,
                                term=term
                                )
    writer.commit()

def load_bursts(currentmonth):
    '''
    load the bursts from the burstsfile, for the bursts active in the current month, and also returns the total number of bursts
    '''
    termburst={}
    ix=open_dir(burstindexdir)
    searcher=ix.searcher()
    start = datetime(2000,1,1,0,0)
    end = datetime(2012,1,1,0,0)
    startRange=DateRange("start_date", start,currentmonth[1],endexcl=True)
    endRange=DateRange("end_date", currentmonth[0],end,endexcl=True)
    res=searcher.search(Require(startRange,endRange),limit=None,sortedby='date')
    for doc in res:
        try:
            termburst[doc['term']].append([doc['cnt'],(doc['start_date'],doc['end_date']),doc['nv'],doc['start'],doc['end']])
        except KeyError:
            termburst[doc['term']]=[[doc['cnt'],(doc['start_date'],doc['end_date']),doc['nv'],doc['start'],doc['end']]]
    return termburst,ix.doc_count()

if __name__ == '__main__':
    IndexBursts()
    logger.info('done!!!')