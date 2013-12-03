#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Wed Nov 20 13:06:07 2013
"""
import os

envdir=os.path.abspath('../data/event_mall/')
datadir=os.path.join(envdir,'dat180')
indexdir=os.path.join(envdir,'index')
vectordir=os.path.join(envdir,'vectors')
dociddir=os.path.join(envdir,'docids')
splitdir=os.path.join(envdir,'splits')
fdates=os.path.join(envdir,'dates')
fgvols=os.path.join(envdir,'gross_daily_volumes')
fvols=os.path.join(envdir,'daily_volumes')

fterm=os.path.join(envdir,'termlist')
fbursts=os.path.join(envdir,'bursts')

sourcedir='/users/mfeys/data/event_mall'
min_df=20