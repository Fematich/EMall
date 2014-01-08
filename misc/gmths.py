#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Dec  3 11:01:44 2013
"""

import os, sys, logging, shutil, subprocess
import numpy as np

from dateutil import rrule
from datetime import datetime, timedelta

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("preprocess")
sys.path.append("../config.py")

def get_months(batchnumber, n_batches):
    '''
    returns a list of monthranges as part of the total monthranges 
    '''
    month_range=[]
    start = datetime(2000,1,1,0,0)
    end = datetime(2012,1,1,0,0)
    first=True
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start, until=end):
        if first:
            first=False
            last_dt=dt
            continue
        else:
            month_range.append('vectors'+last_dt.strftime('%Y%m%d')+'-'+dt.strftime('%Y%m%d'))
            last_dt=dt
    host_months=np.array_split(month_range, n_batches)
    for dir in host_months[batchnumber]:
        print dir
