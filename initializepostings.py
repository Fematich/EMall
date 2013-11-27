#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Nov 26 15:13:33 2013
"""

import os, logging, datetime
from whoosh.index import create_in, open_dir
from whoosh.query import Term
from whoosh.sorting import FieldFacet
from config import indexdir,fdates,fgvols,fvols

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("getvolumes")

ix = open_dir(indexdir)
reader=ix.reader()
searcher=ix.searcher()

with open(fdates,'w') as datefile, open(fgvols,'w') as gvols:
    try:
        for date in reader.field_terms('date'):
            datefile.write(date.strftime('%Y%m%d')+'\t')
            postings=reader.postings('date',date)
            gvols.write(str(sum(1 for _ in postings.all_ids()))+'\t')
    except Exception:
        logger.error('datetime error!: '+str(date))