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
from builtins import object, isinstance, len
import numpy as np

class LSEstimation(object):
    '''
    This class is for least square estimation operation,
    Y = A*W*X
    input:
    X:
    Y:
    W: weight for A
    output:
    A: Y/X
    SSE: sum of (Yi - Yi(estimator))
    SST: SSE + SSR = sum of (Yi - Yi(Mean))
    SSR: sum of (Yi(estimator) -Yi(Mean)）
    coefVar: var of each of A's coefficiency
    '''
    def __init__(self, X, Y, W):
        if not isinstance(X, np.ndarray) or not isinstance(Y, np.ndarray) or not isinstance(W,np.ndarray):
            self.X = np.asarray(X)
            self.Y = np.asarray(Y)
            self.W = np.asarray(W)
        else:
            self.X = X
            self.Y = Y
            self.W = W
        iLen = Y.shape[0]
        self.A = np.ndarray((iLen,1))
        self.AVar = np.ndarray((iLen,1))
        self.AStd = np.ndarray((iLen,1))
        self.SSE = None
        self.SST = None
        self.SSR = None

        self.__calEstimationVariable__()

    def __calEstimationVariable__(self):
        xDim = self.X.shape
        yDim = self.Y.shape
        if xDim[0] != yDim[0]:
            print("please make use of the dimension of X and Y is same!")
            return False

        iX = self.X
        iY = self.Y
        iXT = iX.transpose()
        iXTmp = iXT.dot(iX)
        iYTmp = iXT.dot(iY)

        if len(iX) == len(iY): # when this thing take place, that's to say, only one parameter need to be estimated.
            self.A = iYTmp/iXTmp
            yReg = iX*self.A
        else:
            iXInv = np.linalg.inv(iXTmp)
            self.A = np.array(iXInv.dot(iYTmp))
            yReg = iX.dot(self.A)

        iErrTmp = iY - np.mean(iY)
        self.SST = iErrTmp.T.dot(iErrTmp)
        iErrTmp = yReg - np.mean(iY)
        self.SSE = iErrTmp.T.dot(iErrTmp)
        iErrTmp = iY - yReg
        self.SSR = iErrTmp.T.dot(iErrTmp)

        iVar = iErrTmp.T.dot(iErrTmp)/yDim[0]
        if len(iX) == len(iY):
            self.AVar = np.array(iVar/iXTmp)
        else:
            iEye = np.eye(yDim[0], k=0)
            iXInv = np.linalg.inv(iXTmp)
            self.AVar = iVar*np.diagonal(iEye.dot(iXInv).dot(iEye.T))

        self.AStd = np.sqrt(self.AVar)

    def getEstimatorVar(self):

        return self.AVar

    def getEstimatorSTD(self):

        return self.AStd

    def getEstimator(self):

        return self.A

    def getEstimatorVar(self):

        return self.AVar

    def getXYValue(self):

        return self.X, self.Y, self.W

    def getSSE(self):

        return self.SSE

    def getSSR(self):

        return self.SSR

    def getSST(self):

        return self.SST

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
        return self.A

    def getEstimatorVar(self) :
        return self.AVar

    def getXYValue(self) :
        return self.X, self.Y

    def getSSE(self) :
        return self.SSE

    def getSSR(self) :
        return self.SSR

    def getSST(self) :
        return self.SST

class MLEstimation(object):

    def __init__(self):
        pass

    def __calEstimationA__(self) :
        pass

    def __calEstimationAVar__(self) :
        pass

    def getEstimator(self) :
        return self.A

    def getEstimatorVar(self) :
        return self.AVar

    def getXYValue(self) :
        return self.X, self.Y

    def getSSE(self) :
        return self.SSE

    def getSSR(self) :
        return self.SSR

    def getSST(self) :
        return self.SST