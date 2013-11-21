#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Wed Nov 20 15:22:12 2013
"""
import jpype,os
from whoosh.analysis import Token,Tokenizer
import logging

logger=logging.getLogger("ChineseTokenizer")

class ChineseTokenizer(Tokenizer):
    def  __init__(self):
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", 
                       "-Djava.class.path=%s:%s"%(os.path.abspath('./Segmenter/bin'),
                                                  os.path.abspath('./Segmenter/lib/IKAnalyzer2012_u6.jar')
                                                  ))
        segmenter = jpype.JClass("Segmenter")
        self.tokenizer = segmenter()
        logger.info('Chinese Tokenizer Initialised')

    def __call__(self,text):
        words=self.tokenizer.segment(jpype.JString(text))
        token=Token()
        for word in words:
            token.text=word
            yield token
    
    def __getstate__ ( self ):
        state = {}
        return state