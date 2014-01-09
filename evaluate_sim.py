# -*- coding: utf8 -*-
"""
@author:    Matthias Feys (matthias.feys@intec.ugent.be), based on code of FAN Kai (fankai@net.pku.edu.cn), Peking University   
@date:      %(date)
"""
import os, sys, math, logging, shutil
from whoosh.fields import Schema, NUMERIC,STORED
from whoosh.index import create_in, open_dir
from mongostore.mongostore import MongoStore
from EMall.config import fmod_eventlist, fsig_eventlist, rel_event_dir, irrel_event_dir, docvectorindexdir, split_source

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger=logging.getLogger("evaluate_sim")

def index_docs():
    schema = Schema(
                        did=NUMERIC(int,signed=False,unique=True),
                        dfile=STORED,
                        offset=STORED

                        )
    #create index
    if not os.path.exists(docvectorindexdir):
        os.mkdir(docvectorindexdir)
        ix = create_in(docvectorindexdir, schema)
    else:
        logger.info('burstindex already exists! DELETING')
        shutil.rmtree(docvectorindexdir)
        os.mkdir(docvectorindexdir)
        ix = create_in(docvectorindexdir, schema)

    writer = ix.writer(procs=4, limitmb=500, multisegment=True) 
    for split_subdir in os.listdir(os.path.join(split_source,splitname)):
        logger.info('indexing: '+split_subdir)
        with open(os.path.join(split_source,splitname,split_subdir,'docs'),'r') as vectors:
            for vector in vectors:
                writer.add_document(did=int(vector.split(' ')[0]),
                                    dfile=split_subdir,
                                    offset=vectors.tell()
                                    )
    writer.commit()

def load_docs(event_id):
    relevant_docs=[]
    irrelevant_docs=[]
    with open(os.path.join(rel_event_dir,str(event_id)),'r') as docids:
        for docid in docids:
            docid=int(docid.strip('\n'))
            doc=searcher.document(did=docid)
            if doc!=None:
                with open(os.path.join(split_source,splitname,doc['dfile'],'docs'),'r') as f:
                    f.seek(doc['offset'])
                    line=f.readline()
                tokens = line.split()
    #            aid = int(tokens[0])
                relevant_docs.append({})
                for token in tokens[1:]:
                    if (token.find('-') == -1): continue
                    fields = []
                    fields = token.split("/")
                    term = fields[0]
    #                tf = fields[1]
                    score = fields[2]
                    relevant_docs[-1].setdefault(term, 0)
                    relevant_docs[-1][term] = float(score)
#    tel=0
    with open(os.path.join(irrel_event_dir,str(event_id)),'r') as docids:
        for docid in docids:
#            tel+=1
#            if tel%100==0:
#                logger.info("doc"+str(tel))
            docid=int(docid.strip('\n'))
            doc=searcher.document(did=docid)
            if doc!=None:
                with open(os.path.join(split_source,splitname,doc['dfile'],'docs'),'r') as f:
                    f.seek(doc['offset'])
                    line=f.readline()
                tokens = line.split()
    #            aid = int(tokens[0])
                irrelevant_docs.append({})
                for token in tokens[1:]:
                    if (token.find('-') == -1): continue
                    fields = []
                    fields = token.split("/")
                    term = fields[0]
    #                tf = fields[1]
                    score = fields[2]
                    irrelevant_docs[-1].setdefault(term, 0)
                    irrelevant_docs[-1][term] = float(score)
    logger.info("LOADED %d relevant and %d irrelevant docs"%(len(relevant_docs),len(irrelevant_docs)))
    return relevant_docs,irrelevant_docs

def cosine_similarity(tfa, tfb):
    if len(tfa) == 0 or len(tfb) == 0:
        return 0
    norma, normb = 0, 0
    product = 0
    for term, freq in tfa.iteritems():
        norma += freq ** 2
    for term, freq in tfb.iteritems():
        normb += freq ** 2
        if term in tfa:
            product += freq * tfa[term]
    return product/math.sqrt(norma*normb)

@MongoStore
def eventdocsimilarities(splitname,event_id):
    logger.info('analyzing event: '+str(event_id))
    intersim=0
    intrasim=0
    intercount=0
    intracount=0
    relevant_docs, irrelevant_docs =load_docs(event_id)
    for docid1,rel_doc in enumerate(relevant_docs):
        for docid2,rel_doc2 in enumerate(relevant_docs):
            if docid2<docid1:
                intersim+=cosine_similarity(rel_doc,rel_doc2)
                intercount+=1
            else:
                break
        for irrel_doc in irrelevant_docs:
            intrasim+=cosine_similarity(rel_doc,irrel_doc)
            intracount+=1
    return {'intersim':intersim/intercount,'intrasim':intrasim/intracount}

@MongoStore
def docsimilarities(splitname,big):
    if big:
        event_file=fsig_eventlist
    else:
        event_file=fmod_eventlist
    ret={'intersim':0,'intrasim':0}
    with open(event_file,'r') as moderate_eventlist:
        count=0
        for eventid in moderate_eventlist:
            eventid=int(eventid.strip('\n'))
            event_res=eventdocsimilarities(splitname=splitname,event_id=eventid)
            for key in event_res:
                ret[key]+=event_res[key]
                count+=1
        for key in ret:
            ret[key]/=count
    return ret

if __name__ == "__main__":
    #get correct docs
    splitname=sys.argv[1]
#    index_docs()
    ix=open_dir(docvectorindexdir)
    searcher=ix.searcher()

    #execute similarity-checks
    docsimilarities(splitname=splitname,big=False)
    docsimilarities(splitname=splitname,big=True)