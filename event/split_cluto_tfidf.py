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
from config import indexdir, vectordir, sourcedir, splitdir, eventmall_dir, fbursts, envdir, termsindexdir
from dateutil import rrule
from datetime import datetime, timedelta

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("preprocess")
sys.path.append("../config.py")


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

def getweight(tf,term):
    tf=float(int(tf))
    df=reader.doc_frequency('body',term)
    if tf_form==1:
        weight=tf * np.log(total_ndocs/df);
    else:
        weight=tf * np.log(total_ndocs/df) + 1
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
        shutil.copy2(os.path.join(sourcedir,'vectors','vectors%s-%s'%(month[0].strftime('%Y%m%d'),month[1].strftime('%Y%m%d'))),vectordir)
    if not os.path.exists(splitdir):
        os.mkdir(splitdir)
    sdir=os.path.join(splitdir,'split-%s-%s'%(month[0].strftime('%Y%m%d'),month[1].strftime('%Y%m%d')))
    if not os.path.exists(sdir):
        os.mkdir(sdir)
    fmatrix=os.path.join(sdir,'matrix')
    fdocids=os.path.join(sdir,'docids')
    fdocs=os.path.join(sdir,'docs')
    with open(fvectors,'r') as vectors, open(fmatrix,'w') as matrix, open(fdocids,'w') as docids, open(fdocs,'w') as docs:
        nnz=0
        ndocs=0
        for doc in vectors:
            nb=0
            vector=doc.split()
            date=datetime.strptime(vector[1],'%Y-%m-%d').replace(hour=0, minute=0)
            v=[vector[i:i+2] for i in range(3, len(vector), 2)]
            docscore=0            
            v_matrix=[]
            docstring=''
            for term, tf in v:
               if termsearcher.document(term=term)!=None:
                   nb+=1
                   score=getweight(tf,term)
                   docstring+='%s/%s/%s '%(term,tf,str(score))
                   docscore+=score
                   v_matrix.extend([str(termsearcher.document(term=term)['tid']),score])    
            if len(v_matrix)>2*minlen:
                ndocs+=1
                nnz+=nb
                docids.write(str(vector[0])+'\n')
                docs.write(str(vector[0])+' '+docstring+'\n')
                
                for i in range(1,len(v_matrix)+1,2):
                    v_matrix[i]=str(float(v_matrix[i])/docscore*100)
                matrix.write(' '.join(v_matrix)+'\n')
        # add first line to matrix-file
        docs.write(' '.join([str(ndocs),str(nterms),str(nnz)])+'\n')
    bashcommand='echo "%s\n$(cat %s)" > %s'%(' '.join([str(ndocs),str(nterms),str(nnz)]),fmatrix,fmatrix)
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
    tf_form=0
    ix=open_dir(indexdir)
    reader=ix.reader() 
    total_ndocs=reader.doc_count()
    term_ix=open_dir(termsindexdir)
    termreader=term_ix.reader()
    termsearcher=term_ix.searcher()
    nterms=termreader.doc_count()
    for month in monthlist:
        generate_matrix(month)
    logger.info('done!!!')
