#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Dec 10 10:26:40 2013
"""

import os, sys, logging, shutil, subprocess
import numpy as np
from whoosh.index import create_in, open_dir
from whoosh.query import Term
from whoosh.sorting import FieldFacet
from config import indexdir, vectordir, sourcedir, splitdir, eventmall_dir, fbursts
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



 
def generate_matrix(month):
    '''
    1. number of rows, number of columns, nnz
    2.Note that the columns are numbered starting from 1
    Example:
        see cluto pdf
    '''
    sdir=os.path.join(splitdir,'split-%s-%s'%(month[0].strftime('%Y%m%d'),month[1].strftime('%Y%m%d')))
    fmatrix=os.path.join(sdir,'matrix')
    ndocs=subprocess.call('wc',['-l',fmatrix])
    
    bashcommand='echo "%s\n$(cat %s)" > %s'%(' '.join([str(ndocs),str(nbursts),str(nnz)]),fmatrix,fmatrix)
    subprocess.call(bashcommand,shell=True)
    #TODO: complete the vcluster statement and copy vcluster from ...  
    nclusters=clusters * int(np.sqrt(ndocs))
    prog = "%s/bin/vcluster %s %d -clustfile=%s -cltreefile=%s -showtree -zscores -colmodel=none -showfeatures"%(eventmall_dir, sdir+"/matrix", nclusters, sdir+"/clust", sdir+"/tree")
    with open(os.path.join(sdir,"features"), 'w') as fout:
        subprocess.call(prog,shell=True,stdout=fout)

if __name__ == '__main__':    
    monthlist=get_months(int(sys.argv[1]),int(sys.argv[2]))
    clusters=int(sys.argv[3])
    minlen=int(sys.argv[4])   
    if not os.path.exists(splitdir):
        os.mkdir(splitdir)
    for month in monthlist:
        spr='split-%s-%s'%(month[0].strftime('%Y%m%d'),month[1].strftime('%Y%m%d'))
        if spr not in os.listdir(os.getcwd()):
            shutil.copytree(os.path.join(splitdir,spr),os.path.join(sourcedir,'splits','split-%s-%s'%(month[0].strftime('%Y%m%d'),month[1].strftime('%Y%m%d'))),vectordir)
            generate_matrix(month)
            shutil.copytree(os.path.join(splitdir,spr),os.path.join(sourcedir,'splits','split-%s-%s'%(month[0].strftime('%Y%m%d'),month[1].strftime('%Y%m%d'))),vectordir)
    logger.info('done!!!')