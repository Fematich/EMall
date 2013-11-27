#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Wed Nov 27 21:24:06 2013
"""

import sys
from whoosh.index import open_dir
from config import indexdir

def main(separator='\t'):
    ix = open_dir(indexdir)
    reader=ix.reader()
    for term in reader.field_terms('body'):
        print term
        
if __name__ == "__main__":
    main()