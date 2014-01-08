#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Dec  3 12:58:55 2013
"""

import os, logging, sys
import numpy as np
from whoosh.index import open_dir
from whoosh.query import DateRange
from config import indexdir, datadir,vectordir, dociddir
from dateutil import rrule
from datetime import datetime
from collections import Counter

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("preprocess")


def next_field(fin):
    txt = ""
    while True:
        line = fin.readline()
        if not line: return None
        txt += line
        if line.endswith("\x1e\n"):
            return txt

def getdocvector(dfile,offset):
    with open(os.path.join(datadir,dfile),'r') as f:
        f.seek(offset)
        _=next_field(f)
        _=next_field(f)
        _=next_field(f)
        _=next_field(f)
        body=next_field(f)[5:-2].decode('utf',errors='replace')
        text=body.lower().split()
        return Counter(text)

def get_months(batchnumber, n_batches):
    '''
    returns a list of monthranges as part of the total monthranges 
    '''
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

def getdocvectors(month):
    '''
    generate file with the vectors of the documents of the current month
    '''
    ix = open_dir(indexdir)
    searcher=ix.searcher()
    res=searcher.search(DateRange("date", month[0],month[1],endexcl=True),limit=None,sortedby='date')
    for doc in res:
        yield doc
    
def generatevecs(month):
    '''
    generate a partial docids and vectors-file for the specific month
    '''
    fvectors=os.path.join(vectordir,'vectors%s-%s'%(month[0].strftime('%Y%m%d'),month[1].strftime('%Y%m%d')))
    fdocids=os.path.join(dociddir,'docids%s-%s'%(month[0].strftime('%Y%m%d'),month[1].strftime('%Y%m%d')))
    with open(fvectors,'w') as vecs, open(fdocids,'w') as docids:
        for doc in getdocvectors(month):
            vc=getdocvector(doc['dfile'],doc['offset'])
            vbody=' '.join(['%s %d'%(term.encode('utf-8'), vc[term]) for term in vc ])
            vecs.write('%s %s %s\n'%(doc['did'],doc['date'],vbody))
            docids.write(str(doc['did'])+'\n')


if __name__ == '__main__':
    monthlist=get_months(int(sys.argv[1]),int(sys.argv[2]))
    for month in monthlist:
        generatevecs(month)
    
    logger.info('done!!!')
