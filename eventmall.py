#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Wed Nov 20 14:40:48 2013
"""

"""
module to handle the Eventmall dataset
"""


import os,logging,re
from datetime import datetime

import whoosh
from whoosh.fields import Schema, TEXT, NUMERIC, DATETIME,STORED, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.formats import Frequency

from chinesetokenizer import ChineseTokenizer
from config import datadir, indexdir


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("eventmall")

devline=re.compile('DEV-MUC(?P<ed>\d)-(?P<val>\d+)')
testline=re.compile('TST.*-MUC(?P<ed>\d)-(?P<val>\d+)')
descline=re.compile('(?P<loc>.*),(?P<date>.*)--(?P<msg>.*)')
infoblock=re.compile('\[[^]]*\]')

def next_field(fin):
    txt = ""
    while True:
        line = fin.readline()
        if not line: return None
        txt += line
        if line.endswith("\x1e\n"):
            return txt

class EventMallCorpus():
    def __init__(self):
        self.indexdir=indexdir
        self.datadir=datadir
        if not os.path.exists(self.indexdir):
            logger.info('creating index...')
            self.MakeIndex()
        self.ix=open_dir(self.indexdir)
        logger.info('corpus initialised/loaded')
        
    def __iter__(self):
        for fname in sorted(os.listdir(self.datadir)):
            with open(os.path.join(self.datadir,fname),'rb') as f:
                logger.info('opening: %s'%fname)
                while True:
                    offset=f.tell()
                    faid = next_field(f)
                    if faid == None: 
                        break
                    did = int(faid[3:-2])
                    date = datetime.strptime(next_field(f)[5:-2],'%Y%M%d')
                    durl = next_field(f)[4:-2]
                    title = next_field(f)[6:-2].decode('utf')#.decode('gbk')
                    body = next_field(f)[5:-2].decode('utf')#.decode('gbk')
                    frecord = f.readline()
                    yield did,date,durl,title,body,fname,offset
                
                    
        


    def MakeIndex(self):
        #create schema
        schema = Schema(
                        did=NUMERIC, 
                        date=DATETIME(stored=True),
                        durl=ID,
                        title=TEXT(phrase=False),
                        body=TEXT(analyzer=ChineseTokenizer(),phrase=False,vector=Frequency),
                        dfile=STORED,
                        offset=STORED
                        )
        #create index
        if not os.path.exists(self.indexdir):
            os.mkdir(self.indexdir)
            ix = create_in(self.indexdir, schema)
        else:
            logger.error('index already exists!')
            return
        #fill index with entries    
        writer = ix.writer(procs=4, limitmb=1024, multisegment=True) 
        cnt=0
        cnts=0
        for doc in self.__iter__():
            try:
                if cnts%1000==0:
                    logger.info('indexing document %d'%cnts)
                writer.add_document(did=doc[0],
                                    date=doc[1],
                                    durl=doc[2],
                                    title=doc[3],
                                    body=doc[4],
                                    dfile=doc[5],
                                    offset=doc[6],
                                )
                cnts+=1
            except Exception, e:
                print e,doc[3]
                cnt+=1
        writer.commit()
        print 'Failed documents:%d \t Succeeded:%d'%(cnt,cnts)


if __name__ == '__main__':
    emall=EventMallCorpus()
    logger.info('done!!!')

