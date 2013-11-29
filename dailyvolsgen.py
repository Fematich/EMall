#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Thu Nov 28 11:14:20 2013
"""

import sys, logging,os
from datetime import datetime
from whoosh.query import Term
from whoosh.sorting import Facets
from whoosh.index import open_dir
from whoosh import sorting
import numpy as np
from config import fdates, fvols, min_df, indexdir, fterm

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("dailyvols")

def main():
    ix = open_dir(indexdir)
    searcher=ix.searcher()
    reader=ix.reader()
    myfacet=Facets().add_field("date",maptype=sorting.Count)
    dts  = [datetime.strptime(date,'%Y%m%d').replace(hour=0, minute=0) for date in open(fdates,'r').read().strip().split()]
    dates=dict(zip(dts,range(len(dts))))
    with open(fvols,'w') as daily_vols:
        for term in open(os.path.join(fterm),'r'):
            term=term.rstrip('\n').decode('utf-8')
            try:
                docfreq=reader.doc_frequency('body',term)
                if docfreq>min_df:
                    res=searcher.search(Term('body',term),groupedby=myfacet)
                    vols=np.zeros(len(dts))
                    for day,count in res.groups().iteritems():
                        vols[dates[day]]+=count
                    daily_vols.write('%s %d %s\n'%(term.encode('utf-8'),docfreq,' '.join([str(int(v)) for v in vols])))
            except Exception, e:
                logger.error(e)
                pass
            
if __name__ == "__main__":
#    fpath=sys.argv[1]    
    main()