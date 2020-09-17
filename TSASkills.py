#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from builtins import object, len, range, print, int
import numpy as np
from scipy.linalg import toeplitz
import infrastructure as inf

class StatisticsTSTest(object):
    def __init__(self):
        pass

    def __DFTest__(self, data, kind):
        '''
        input:
        data: the data which need to be tested
        kind: string type, which kind of type should be used to test, currently the following three kinds: nc, c, ct
        return:
        tvalue:
        pvalue:
        '''
        return

    def getDFTestResult(self, data, kind):

        return self.__DFTest__(data, kind)

    def __ADFTest__(self, data, kind):

        return

    def getADFTestResult(self, data, kind):

        return self.__ADFTest__(data, kind)

    def __PPTest__(self, data, kind):

        return

    def getPPTestResult(self, data, kind):

        return self.__PPTest__(data, kind)

    def __LBTest__(self):
        pass

    def getLBTestResult(self):

        return self.__LBTest__()

    def __LMTest__(self):
        pass

    def getLMTestResult(self):

        return self.__LMTest__()

    def __JBTest__(self, data, confidence):

        return

    def getJBTestResult(self, data, confidence=0.95):

        return self.__JBTest__(data, confidence)

class StatisticsBasic(object):
    def __init__(self, data):
        self.iData = np.asarray(data)

    def getData(self):
        return self.iData

    def getSize(self):
        return len(self.iData)

    def __Mean__(self):
        return np.mean(self.iData)

    def getMean(self):
        return self.__Mean__()

    def __Var__(self):
        return np.var(self.iData)

    def getVar(self):
        return self.__Var__()

    def __Std__(self):
        return np.std(self.iData)

    def getStd(self):
        return self.__Std__()

    def __Skews__(self):
        iMean = self.__Mean__()
        iVar = self.__Var__()

        return np.mean((self.iData - iMean)**3)/(iVar**1.5)

    def getSkews(self):
        return self.__Skews__()

    def __Kurt__(self):
        iMean = self.__Mean__()
        iVar = self.__Var__()

        return np.mean((self.iData - iMean)**4)/(iVar**2)

    def getKurt(self):
        return self.__Kurt__()


class StatisticsModel(StatisticsBasic):
    '''
    consider GARCH/ARCH model
    functinality:
    1. confirm the coefficiency
    2. fit
    3. prediction
    '''
    def __init__(self, data):
        StatisticsBasic.__init__(self, data)
        self.iRouk = []
        self.__calcRouk__()

    def __calcDefaultOrder__(self):
        iData = self.getData()
        return np.ceil(12.*np.power(len(iData)/100., 1/4.))

    def getOrder(self):
        return self.__calcDefaultOrder__()

    def __calcRouk__(self):
        iData = np.asarray(self.getData())
        iData = iData - self.getMean()

        iRouk = self.iRouk
        iRouk.append(np.dot(iData, iData))

        for i in range(1, len(iData)):
            iRouk.append(np.dot(iData[:-i], iData[i:]))

    def getRouk(self, order):
        return self.iRouk[:order+1]

    def __calcACF__(self, order, bias):

        iRouk = np.asarray(self.getRouk(order))
        iSize = self.getSize()
        if iSize <= len(iRouk):
            print("please enter the right order")
            return None

        if bias is not True:
            for i in range(0, len(iRouk)):
                iRouk[i] = iRouk[i] * iSize/(iSize-i)

        return iRouk[1:]/iRouk[0]

    def getACF(self, order=None, bias=True):
        if order is None:
            order = self.getOrder()

        order = int(order)

        return self.__calcACF__(order, bias)

    def __YuleWalker__(self, order, bias):
        iRouk = np.asarray(self.iRouk[:order])
        iSize = self.getSize()

        if bias is not True:
            for i in range(0, len(iRouk)):
                iRouk[i] = iRouk[i] * iSize/(iSize-i)

        iGammaP = np.asarray(toeplitz(iRouk[:-1]))

        return np.linalg.solve(iGammaP, iRouk[1:])

    def getPACF(self, order=None, bias=True):
        if order is None:
            order = self.getOrder()

        order = int(order)

        iPACF = []

        for i in range(1, order+1):
            iAlpha = self.__YuleWalker__(i, bias)
            iPACF.append(iAlpha[-1])

        return iPACF

    def __ACFPACFCoefTest__(self, confidence):
        '''
        this functionality is used for ACF/PACF coefficiency Test
        if the confidence is 0.95, then the coefficiency should be 2, that is 2*sigma,
        currently, sqrt is the sigma
        when abs(coef) < 2/sqrt(T), then accept the ACF/PACF coefficiency, otherwise refuse it.
        abs(Ak)<2/Sqrt(T), T is the oberservation number.
        '''

        iSqrt = np.sqrt(self.getSize())

        if confidence == 0.99:
            coef = 3
        else:
            coef = 2

        return coef/iSqrt, -coef/iSqrt

    def getACFPACFCoefTest(self, confidence = 0.95):
        return self.__ACFPACFCoefTest__(confidence)

class DataConstruct(object):
    '''
    construct all kinds of array
    return the assembled array
    '''
    def __init__(self):
        pass


