#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Nov 26 15:13:33 2013
"""

from whoosh.index import open_dir
ix = open_dir('../data/event_mall/index')
reader=ix.reader()
for term in reader.field_terms('body'):
    print term+'\n__________________________\n'
    postings=reader.postings('body',term)
    for docid in postings.all_ids():
        postings.
        print docid
        searcher=ix.searcher()
        searcher.stored_fields(docid)