#!/usr/bin/env python 
# -*- coding:utf-8 -*-
'''
There is the foundation of the whole alg in the statistic.
In this file, there exist two algebra estimation alg.
one is least square related, including OLS, WLS.
when change weight in WLS, get many different LS variants.
the other is distance estimation alg.

Actually, there exist three alg. LS, Distance estimation, Maxim Likelihood estimation
In this file, do not implement MLE alg since when using MLE, must know the distribution density function in first.
unfortunately, do not know the DDF in advance.
'''
from builtins import object, isinstance
import numpy as np

class LSEstimation(object):
    '''
    This class is for least square estimation operation,
    Y = A*X
    input:
    X:
    Y:
    output:
    A: Y/X
    SSE: sum of (Yi - Yi(estimator))
    SST: SSE + SSR = sum of (Yi - Yi(Mean))
    SSR: sum of (Yi(estimator) -Yi(Mean)）
    coefVar: var of each of A's coefficiency
    '''
    def __init__(self, X, Y):
        if not isinstance(X, np.ndarray) or not isinstance(Y, np.ndarray):
            self.X = np.asarray(X)
            self.Y = np.asarray(Y)
        else:
            self.X = X
            self.Y = Y

        self.A = [Y.shape[0]]
        self.AVar = [Y.shape[0]]
        self.SSE = None
        self.SST = None
        self.SSR = None

    def __calEstimationA__(self):
        pass

    def __calEstimationAVar__(self):
        pass

    def getEstimator(self):
        pass

    def getEstimatorVar(self):
        pass

    def getXYValue(self):
        pass

    def getSSE(self):
        pass

    def getSSR(self):
        pass

    def getSSt(self):
        pass

class DEstimation(object):
    '''
    This class is for distance estimation operation,
    Y = A*X
    input:
    X:
    Y:
    output:
    A: Y/X
    SSE: sum of (Yi - Yi(estimator))
    SST: SSE + SSR = sum of (Yi - Yi(Mean))
    SSR: sum of (Yi(estimator) -Yi(Mean)）
    coefVar: var of each of A's coefficiency
    '''

    def __init__(self, X, Y) :
        if not isinstance(X, np.ndarray) or not isinstance(Y, np.ndarray) :
            self.X = np.asarray(X)
            self.Y = np.asarray(Y)
        else :
            self.X = X
            self.Y = Y

        self.A = [Y.shape[0]]
        self.AVar = [Y.shape[0]]
        self.SSE = None
        self.SST = None
        self.SSR = None

    def __calEstimationA__(self) :
        pass

    def __calEstimationAVar__(self) :
        pass

    def getEstimator(self) :
        pass

    def getEstimatorVar(self) :
        pass

    def getXYValue(self) :
        pass

    def getSSE(self) :
        pass

    def getSSR(self) :
        pass

    def getSSt(self) :
        pass
