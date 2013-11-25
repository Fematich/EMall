# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Wed Nov 20 14:40:48 2013
"""

"""
module to handle the Eventmall dataset
"""


import os,logging,re,shutil
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
        else:
            logger.info('deleting and creating index...')
            shutil.rmtree(self.indexdir)
            self.MakeIndex()
        self.ix=open_dir(self.indexdir)
        logger.info('corpus initialised/loaded')
        
    def __iter__(self):
#        for fname in sorted(os.listdir(self.datadir)):
#        for fname in ['dat'+str(tel) for tel in range(112)]:
        for fname in ['dat'+str(tel) for tel in range(112)]:
            with open(os.path.join(self.datadir,fname),'rb') as f:
                logger.info('opening: %s'%fname)
#                while True:
#                    try:
#                        offset=f.tell()
#                        faid = f.readline()
#                        if not faid: 
#                            break
#                        did = int(faid[3:-2].decode('utf',errors='replace'))
#                        date = datetime.strptime(f.readline().decode('utf',errors='replace')[5:-2],'%Y%M%d')
#                        durl = f.readline()[4:-2].decode('utf',errors='replace')
#                        title = f.readline()[6:-2].decode('utf',errors='replace')#.decode('gbk')
#                        body = f.readline()[5:-2].decode('utf',errors='replace')#.decode('gbk')
#                        frecord = f.readline()
#                    except Exception, e:
#                        print e, offset
#                    yield did,date,durl,title,body,fname,offset
                while True:
                    offset=f.tell()
                    faid = next_field(f)
                    if faid == None: 
                        break
                    try:
                        did = int(faid[3:-2].decode('utf',errors='replace'))#.decode('GB18030',errors='replace'))
                        date = datetime.strptime(next_field(f).decode('utf',errors='replace')[5:-2],'%Y%M%d')
                        durl = next_field(f)[4:-2].decode('utf',errors='replace')
                        title = next_field(f)[6:-2].decode('utf',errors='replace')#.decode('gbk')
                        body = next_field(f)[5:-2].decode('utf',errors='replace')#.decode('gbk')
                        frecord = f.readline()
#                        yield did,date,durl,title,body,fname,offset
                        yield did,date,body,fname,offset
                    except Exception, e:
                        logger.error(str(e)+': '+faid.decode('utf',errors='replace'))
                        continue
                    
        


    def MakeIndex(self):
        #create schema
        schema = Schema(
                        did=STORED, 
                        date=DATETIME(stored=True),
                        #durl=STORED(stored=False),
                        #title=STORED(stored=False),
#                        body=TEXT(analyzer=ChineseTokenizer(),phrase=False,vector=Frequency),
                        body=TEXT(phrase=False),#,vector=Frequency),
                        dfile=STORED,
                        offset=STORED
                        )
        #create index
        if not os.path.exists(self.indexdir):
            os.mkdir(self.indexdir)
            ix = create_in(self.indexdir, schema)
        else:
            logger.info('index already exists! DELETING')
            return
        #fill index with entries    
        writer = ix.writer(procs=4, limitmb=1024, multisegment=True) 
#        first=True
        cnt=0
        cnts=0
        for doc in self.__iter__():
            try:
                if cnts%1000==0:
#                    if first:
#                        first=False
#                    else:
#                        writer.commit()
#                        writer = ix.writer()
                    logger.info('indexing document %d'%cnts)
                writer.add_document(did=doc[0],
                                    date=doc[1],
                                    #durl=doc[2],
                                    #title=doc[3],
                                    body=doc[2],
                                    dfile=doc[3],
                                    offset=doc[4],
                                )
                cnts+=1
            except Exception, e:
                print e,doc
                cnt+=1
                writer.commit()
                writer = ix.writer()

        writer.commit()
        print 'Failed documents:%d \t Succeeded:%d'%(cnt,cnts)


if __name__ == '__main__':
    emall=EventMallCorpus()
    logger.info('done!!!')

