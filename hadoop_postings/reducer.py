#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Wed Nov 27 21:24:32 2013
"""

import sys, datetime
from whoosh.query import Term
from whoosh.sorting import Facets
from whoosh.index import open_dir
from whoosh import sorting
import numpy as np
from config import indexdir,fdates,min_df

def main():
    ix = open_dir(indexdir)
    searcher=ix.searcher()
    reader=ix.reader()
    myfacet=Facets().add_field("date",maptype=sorting.Count)
    dts  = [datetime.strptime(date,'%Y%m%d').replace(hour=0, minute=0) for date in open(fdates,'r').read().strip().split()]
    dates=dict(zip(dts,range(len(dts))))
    
    for term in sys.stdin:
#        try:
        docfreq=reader.doc_frequency('body',term)
        if docfreq>min_df:
            res=searcher.search(Term('body',term),groupedby=myfacet)
            vols=np.zeros(len(dts))
            for day,count in res.groups().iteritems():
                vols[dates[day]]+=count
                print '%s %d %s\n'%(term.encode('utf-8'),docfreq,' '.join([str(int(v)) for v in vols]))
#        except Exception, e:
#            logger.error(e)
#            pass
            
if __name__ == "__main__":
    main()