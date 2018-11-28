# Standard imports 
import os
import ROOT

# RootTools
from RootTools.core.standard import *

# Logging
import logging
logger = logging.getLogger(__name__)

def singleton(class_):
  instances = {}
  def getinstance(*args, **kwargs):
    if class_ not in instances:
        instances[class_] = class_(*args, **kwargs)
    return instances[class_]
  return getinstance

def reduceFiles_DeepLepton( self, factor = 1, to = None ):
    ''' Reduce number of files in the sample
    '''
    len_before = len(self.files)
    norm_before = self.normalization

    if factor!=1:
        self.files = self.files[0::factor]
        if len(self.files)==0:
            raise helpers.EmptySampleError( "No ROOT files for sample %s after reducing by factor %f" % (self.name, factor) )
    elif to is not None:
        if to>=len(self.files):
            return
        self.files = self.files[:to] 
    else:
        return
