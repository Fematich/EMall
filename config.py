#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Wed Nov 20 13:06:07 2013
"""
import os

envdir=os.path.abspath('../data/event_mall/')
datadir=os.path.join(envdir,'dat180')
indexdir=os.path.join(envdir,'test_small_index')

fdates=os.path.join(envdir,'dates')
fgvols=os.path.join(envdir,'gross_daily_volumes')
fvols=os.path.join(envdir,'daily_volumes')

fterm=os.path.join(envdir,'termlist')
fbursts=os.path.join(envdir,'bursts')
min_df=20