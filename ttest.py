#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
@author:    Matthias Feys (matthias.feys@intec.ugent.be), IBCN
@date:      %(date)
"""
import logging,sys,subprocess
from pymongo import MongoClient
from scipy.stats import ttest_rel,ttest_ind

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("MWWtest")


client = MongoClient()
db = client['evaluation']
datastore = db['compare_event']

def ttest(name1,name2):
    for big in [True]:
        F1,F2=[],[]
        recalls1,recalls2=[],[]
        precisions1,precisions2=[],[]
        MAP1,MAP2=[],[]
        for res in datastore.find({"parameters.name":name1,"parameters.info.dataset":"event_mall","parameters.big":big}):
            recalls1.append(res['result']['recall'])
            precisions1.append(res['result']['precision'])
            F1.append(res['result']['F1'])
#            MAP1.append(res['result']['AP'])
        for res in datastore.find({"parameters.name":name2,"parameters.info.dataset":"event_mall","parameters.big":big}):
            recalls2.append(res['result']['recall'])
            precisions2.append(res['result']['precision'])
            F2.append(res['result']['F1'])
#            MAP2.append(res['result']['AP'])
#        with open('tmp/recall','w') as recallf:
#            for items in zip(recalls1,recalls2):
#                recallf.write("%f %f\n"%(items[0],items[1]))
#        subprocess.call('./wilcoxon tmp/recall 90.0',shell=True)
#        with open('tmp/precision','w') as precisionf:
#            for items in zip(precisions1,precisions2):
#                precisionf.write("%f %f\n"%(items[0],items[1]))
#        subprocess.call('./wilcoxon tmp/precision 90.0',shell=True)
        print len(precisions1),len(precisions2)
        print 'precisions '+str(big)
        print ttest_rel(precisions1,precisions2)#,equal_var=False)
        print 'recalls '+str(big)
        print ttest_rel(recalls1,recalls2)#,equal_var=False)
        print 'F1 '+str(big)
        print ttest_rel(F1,F2)#,equal_var=False)
#        with open('tmp/MAP','w') as MAPf:
#            for items in zip(MAP1,MAP2):
#                MAPf.write("%f %f\n"%(items[0],items[1]))
#        subprocess.call('./wilcoxon tmp/MAP',shell=True)

if __name__ == '__main__':    
    ttest(sys.argv[1],sys.argv[2])
