#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Dec 10 13:50:55 2013
"""

import os,logging,re,shutil
from datetime import datetime

import whoosh
from whoosh.fields import Schema,STORED, ID, KEYWORD
from whoosh.index import create_in
from EMall.config import termsindexdir, fterms



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

    writer = ix.writer(procs=4, limitmb=1024, multisegment=True) 
    with open(fterms,'r') as terms:
        cnt=0
        for term in terms:
            cnt+=1
            writer.add_document(tid=cnt,
                                    term=term.split(' ')[0].decode('utf',errors='replace')
                                    )
    writer.commit()

if __name__ == '__main__':
    IndexTerms()
    logger.info('done!!!')