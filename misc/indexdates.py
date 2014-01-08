#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Dec 10 21:41:50 2013
"""

### Iterate over all documents and store their id with their date in index and in a file
from whoosh.fields import Schema, STORED, ID
from config import indexdir,fainfo, dateindexdir
from whoosh.index import open_dir, create_in
import logging, os

ix=open_dir(indexdir)
reader=ix.reader()

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("Indexer")


#schema = Schema(
#                    did=ID,
#                    date=STORED
#                    )
##create index
#if not os.path.exists(dateindexdir):
#    os.mkdir(dateindexdir)
#    ix = create_in(dateindexdir, schema)
#    writer = ix.writer(procs=4, limitmb=400, multisegment=True)
#else:
#    logger.info('burstindex already exists! DELETING')
#
#for _,doc in reader.iter_docs():
#    did=str(doc['did'])
#    writer.add_document(
#                        did=did,
#                        date=doc['date'].strftime('%Y%m%d')
#                        )
#writer.commit()
with open(fainfo,'w') as faif:
    for _,doc in reader.iter_docs():
        faif.write('%s %s\n'%(doc['did'],doc['date'].strftime('%Y%m%d')))
        