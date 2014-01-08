#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Dec 10 13:50:55 2013
"""

import os,logging,re,shutil
from datetime import datetime

import whoosh
from whoosh.fields import Schema, NUMERIC,STORED, ID
from whoosh.index import create_in
from EMall.config import indexdir, vectorindexdir, vectordir



logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("Indexer")

def IndexVectors():
    schema = Schema(
                        did=NUMERIC(int,signed=False,unique=True),
                        dfile=STORED,
                        offset=STORED

                        )
    #create index
    if not os.path.exists(vectorindexdir):
        os.mkdir(vectorindexdir)
        ix = create_in(vectorindexdir, schema)
    else:
        logger.info('burstindex already exists! DELETING')
        return

    writer = ix.writer(procs=4, limitmb=500, multisegment=True) 
    for fvector in os.listdir(vectordir):
        logger.info('indexing: '+fvector)
        with open(os.path.join(vectordir,fvector),'r') as vectors:
            for vector in vectors:
                writer.add_document(did=vector.split(' ')[0],
                                    dfile=fvector,
                                    offset=vectors.tell()
                                    )
    writer.commit()

if __name__ == '__main__':
    IndexVectors()
    logger.info('done!!!')