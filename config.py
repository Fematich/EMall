#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Wed Nov 20 13:06:07 2013
"""
import os

envdir=os.path.abspath('/home/mfeys/work/data/event_mall/')
datadir=os.path.join(envdir,'dat180')

indexdir=os.path.join(envdir,'index')
burstindexdir=os.path.join(envdir,'burstindex')
vectorindexdir=os.path.join(envdir,'vectorindex')
docvectorindexdir=os.path.join(envdir,'docvectorindex')
dateindexdir=os.path.join(envdir,'dateindex')
termsindexdir=os.path.join(envdir,'termindex')
vectordir=os.path.join(envdir,'vectors')
dociddir=os.path.join(envdir,'docids')
splitdir=os.path.join(envdir,'splits')

fdates=os.path.join(envdir,'dates')
fgvols=os.path.join(envdir,'gross_daily_volumes')
fvols=os.path.join(envdir,'daily_volumes')
fainfo=os.path.join(envdir,'ainfo')
fgold=os.path.join(envdir,'event_file.csv')
feventdates=os.path.join(envdir,'event.csv')
fevent_index=os.path.join(envdir,'events_index')
faevents=os.path.join(envdir,'aevents')
fterm=os.path.join(envdir,'termlist')
fbursts=os.path.join(envdir,'bursts')
fterms=os.path.join(envdir,'subparts')
rel_event_dir=os.path.join(envdir,'eval/relevant')
irrel_event_dir=os.path.join(envdir,'eval/irrelevant')
fsig_eventlist=os.path.join(envdir,'eval/significant_events')
fmod_eventlist=os.path.join(envdir,'eval/moderate_events')

sourcedir='/users/mfeys/data/event_mall'
split_source='/home/mfeys/work/data/splits'
min_df=20
