#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Wed Nov 27 23:54:40 2013
"""

from whoosh.index import open_dir
from config import indexdir

min_df=10

def main():
    ix = open_dir(indexdir)
    reader=ix.reader()
    with open('termlist','w') as termlist:
        for term in reader.field_terms('body'):
            docfreq=reader.doc_frequency('body',term)
            #print docfreq
            if docfreq>min_df:   
                for term in reader.field_terms('body'):
                    termlist.write(term.encode('utf-8')+'\n')
        
if __name__ == "__main__":
    main()
    