#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Dec 10 13:50:55 2013
"""

import os,logging,re,shutil
from datetime import datetime

import whoosh
from whoosh.fields import Schema,STORED, ID, KEYWORD
from whoosh.index import create_in, open_dir
from EMall.config import termsindexdir, fterms, indexdir



logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("Indexer")

def IndexTerms():
    schema = Schema(
                        term=ID(stored = True),
                        tid=STORED
                        )
    #create index
    if not os.path.exists(termsindexdir):
        os.mkdir(termsindexdir)
        ix = create_in(termsindexdir, schema)
    else:
        logger.info('termindex already exists! ABORTING')
        return

    writer = ix.writer(procs=1, limitmb=1024) 
    with open(fterms,'r') as terms:
        cnt=0
        for term in terms:
            if term[0] not in ['0','1','2','3','4','5','6','7','8','9']:
                term=term.replace('\n','')
                docfreq=reader.doc_frequency('body',term)
                if 20<docfreq<0.4*total_ndocs:
                    cnt+=1
                    writer.add_document(tid=cnt,
                                            term=term.decode('utf',errors='replace')
                                            )
                elif docfreq>0.4*total_ndocs:
                    print term,docfreq
        print cnt
        writer.commit()

if __name__ == '__main__':
    ix = open_dir(indexdir)
    reader=ix.reader()  
    total_ndocs=reader.doc_count()
    IndexTerms()
    logger.info('done!!!')