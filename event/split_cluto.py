#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Dec  3 11:01:44 2013
"""

import os, sys, logging, shutil, subprocess
import numpy as np
from whoosh.index import create_in, open_dir
from whoosh.query import Term
from whoosh.sorting import FieldFacet
from config import indexdir, vectordir, sourcedir, splitdir, fbursts
from dateutil import rrule
from datetime import datetime, timedelta

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("preprocess")

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

def load_bursts(currentmonth):
    '''
    load the bursts from the burstsfile, for the bursts active in the current month, and also returns the total number of bursts
    '''
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
                    termburst[term].append([cnt,(start_date,end_date),nv,start,end])
                except KeyError:
                    termburst[term]=[cnt,(start_date,end_date),nv,start,end]
    return termburst,cnt

def getweight(tf,term,burst):
    tf=float(int(tf))
    df=reader.doc_frequency('body',term)
    weight=tf * np.log(total_ndocs/df) + 1;
    return weight
    
def generate_matrix(month):
    '''
    1. number of rows, number of columns, nnz
    2.Note that the columns are numbered starting from 1
    Example:
        see cluto pdf
    '''
    fvectors=os.path.join(vectordir,'vectors%s-%s'%(month[0].strftime('%Y%m%d'),month[1].strftime('%Y%m%d')))   
    if not os.path.isfile(fvectors):
        shutil.copy2(os.path.join(sourcedir,'vectors%s-%s'%(month[0].strftime('%Y%m%d'),month[1].strftime('%Y%m%d'))),vectordir)
    if not os.path.exists(splitdir):
        os.mkdir(splitdir)
    sdir=os.path.join(splitdir,'vectors%s-%s'%(month[0].strftime('%Y%m%d'),month[1].strftime('%Y%m%d')))
    if not os.path.exists(sdir):
        os.mkdir(sdir)
    fmatrix=os.path.join(sdir,'matrix')
    with open(fvectors,'r') as vectors, open(fmatrix,'w') as matrix:
        nnz=0
        ndocs=0
        for doc in vectors:
            ndocs+=1
            vector=doc.split()
            date=datetime.strptime(vector[1],'%Y%m%d').replace(hour=0, minute=0)
            v=[vector[i:i+2] for i in range(3, len(vector), 2)]
            v_matrix=[]            
            for term, tf in v:
                if term in bursts:
                   for burst in bursts[term]:
                       if datetime.strptime(burst[1][0],'%Y%m%d').replace(hour=0, minute=0) <= date <= datetime.strptime(burst[1][1],'%Y%m%d').replace(hour=0, minute=0):
                           # term in burst: replace term-string by burst-id and compute new weight
                           nnz+=1
                           v_matrix.extend(burst[0],str(getweight(tf,term,burst)))    
            matrix.write(' '.join(v_matrix)+'\n')
    # add first line to matrix-file
    bashcommand='echo "%s\n$(cat %s)" > %s'%(' '.join([str(ndocs),str(nbursts),str(nnz)]),fmatrix,fmatrix)
    subprocess.call(bashcommand,shell=True)
    #TODO: complete the vcluster statement and copy vcluster from ...  
    #prog = "%s/bin/vcluster %s %d -clustfile=%s -cltreefile=%s -showtree -zscores -colmodel=none -showfeatures"%(options.runtime_dir, split_dir+"/matrix", nclusters, split_dir+"/clust", split_dir+"/tree")
if __name__ == '__main__':    
    monthlist=get_months(int(sys.argv[1]),int(sys.argv[2]))
    ix = open_dir(indexdir)
    reader=ix.reader()    
    total_ndocs=reader.doc_count()
    for month in monthlist:
        bursts,nbursts=load_bursts(month)
        generate_matrix(month)
    logger.info('done!!!')
