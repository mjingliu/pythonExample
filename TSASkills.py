#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from builtins import object, len, range, print, int
import numpy as np
from scipy.linalg import toeplitz
import const_stat
import infrastructure as inf

class StatisticsTSTest(object):
    def __init__(self):
        self.iLBGamma = None
        self.iLBCtr = False

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

    def __LBTestTValue__(self, data, order):
        '''
        1. get the T value
        2. get the p value
        '''
        if self.iLBCtr is False:
            self.__calcGamma__(data)

        iData = np.asarray(data)
        iSize = iData.size
        iArr = self.iLBGamma[:order]
        iTmp = []
        for i in range(0, order):
            iTmp.append(iArr[i]*iSize*(iSize+2)/(iSize-i-1))
        iTmp = np.asarray(iTmp)
        iTValue = np.dot(iTmp[:],iTmp[:])

        return iTValue

    def __LBTestPValue__(self, freedom, significance):
        iSigList = np.asarray(const_stat.X2ROW)
        iLen = iSigList.size
        iloc = 9 # location 9 is 0.05 significance

        if iSigList[0]<= significance:
            iloc = 0
        elif iSigList[iLen-1] >= significance:
            iloc = iLen -1
        else:
            for i in range(0, iLen-1):
                if iSigList[i] >significance and iSigList[i+1] <= significance:
                    iloc = i+1
                    break

        return const_stat.X2Value[iloc][freedom]

    def __calcGamma__(self, data):
        iData = np.asarray(data)

        iSize = iData.size
        '''
        calculate the Gamma_k
        '''
        iGamma = []
        iGamma.append(np.dot(iData[:], iData[:]))
        for i in range(1, iSize):
            iGamma.append(np.dot(iData[:-i],iData[i:]))
        self.iLBGamma = np.array(iGamma[1:]/iGamma[0])

    def getLBTestResult(self, data, order=0, numofpara=0, significance=0.05):
        '''
        condition:
        if the model is ARMA(p,q), then the degree(N) of X2 should be m-(p+q)
        order: the input N
        significance: the probability of X2 should be met
        fitPara: number of p+q
        default value of alg of order is 12.*np.power(len(data)/100., 1/4.)
        or, order = ln(T), T = length of array
        in current implementation, use the first one.
        '''

        if self.iLBCtr is False:
            self.__calcGamma__(data)
            self.iLBCtr = True
        if order <= 0:
            order = np.ceil(12.*np.power(len(data)/100., 1/4.))
        if order <= numofpara:
            print("please check the order and num of para passed!")
            return None,None,None

        return self.__LBTestTValue__(data, order), self.__LBTestPValue__(order-numofpara, significance), order

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

    def __checkSignificance__(self, confidence):
        if confidence >= 1 and confidence < 0:
            print("enter the wrong confidence value!")
            return None

        iSigTmp = 1 - confidence
        iSignificance = [0.25,0.1,0.05,0.025,0.01,0.005]
        iSize = len(iSignificance)
        iLoc = iSize
        if iSigTmp >= iSignificance[0]:
            iLoc = 0
        elif iSigTmp < iSignificance[iSize-1]:
            iLoc = iSize -1
        else:
            for i in range(0, iSize-1):
                if iSigTmp < iSignificance[i] and iSigTmp >= iSignificance[i+1]:
                    iLoc = i+1
                    break

        return iSignificance[iLoc]

    def getConfidence(self, confidence):
        return 1. - self.__checkSignificance__(confidence)

    def getSignifance(self, confidence):
        return self.__checkSignificance__(confidence)

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

        self.iRouk = iRouk

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
        confidence = self.getConfidence(confidence)
        return self.__ACFPACFCoefTest__(confidence)

    def __meanZeroTest__(self, significance):
        '''
        input:
            Test the duration when mean is zero within the provided confidence
        output:
        the confidence area
        Xbar/(sigma/sqrt(n)) ~ t(n-1) distribution

        when the actual Xbar calulated from the sample is between the duration calculated by t distribution,
        then, the H0: mean is zero is right, otherwise, H1: mean is not zero is right
        '''

        sampleLen = self.getSize()
        iVar = self.getVar()

        if sampleLen >= len(const_stat.TN):
            iLen = len(const_stat.TN) - 2
        else:
            iLen = sampleLen - 1

        iTau = 0

        for i in range(0, const_stat.TROW):
            if const_stat.TValue[i][0] == significance:
                iTau = const_stat.TValue[i][iLen]
                break

        iTValue = (iVar/sampleLen)**0.5*iTau

        return -iTValue, iTValue

    def getMeanZeroTest(self, confidence=0.95):
        iSig = self.getSignifance(confidence)
        return self.__meanZeroTest__(iSig), self.getMean()

class DataConstruct(object):
    '''
    construct all kinds of array
    return the assembled array
    '''
    def __init__(self):
        pass


