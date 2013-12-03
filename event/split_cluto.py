#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Dec  3 11:01:44 2013
"""

import os, logging
import numpy as np
from whoosh.index import create_in, open_dir
from whoosh.query import Term
from whoosh.sorting import FieldFacet
from config import indexdir,fbursts
from dateutil import rrule
from datetime import datetime, timedelta

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("preprocess")

def get_months(batchnumber, n_batches)
    month_range=[]
    start = datetime(2000,1,1,0,0)
    end = datetime(2012,1,1,0,0)
    first=True
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start, until=end):
        if first:
            first=False
            last_dt=dt
            continue
        else:
            month_range.append((last_dt,dt))
            last_dt=dt
    host_months=np.array_split(month_range, n_batches)
    return host_months[batchnumber]

ix = open_dir(indexdir)
reader=ix.reader()
searcher=ix.searcher()

def load_bursts(currentmonth):
    termburst={}
    cnt=0
    with open(fbursts,'r') as bursts:
        for burst in bursts:
            cnt+=1
            if cnt%1000000==0:
                print 'processed %dM bursts'%cnt
            nv,start,end,term,startd,endd=burst.split()
            start_date=datetime.strptime(startd,'%Y%m%d')
            end_date=datetime.strptime(startd,'%Y%m%d')<currentmonth[1]
            if (start_date<currentmonth[1] and end_date>=currentmonth[0]):
                try:
                    termburst[term].append([(start_date,end_date),nv,start,end])
                except KeyError:
                    termburst[term]=[(start_date,end_date),nv,start,end]
    return termbursts

if __name__ == '__main__':
    get_months(int(args[1])
    emall=EventMallCorpus()
    logger.info('done!!!')
