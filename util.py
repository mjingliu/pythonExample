#!/usr/bin/env python
# -*- coding:utf-8 -*-
from builtins import isinstance, print

import numpy as np
from scipy.linalg import toeplitz
import const_stat
import const


def extendAxis(origin, length):
    '''
    :param origin: the targeted X-axis
    :param length: input the real length which to be used for extending to the len(origin)
    :return: the extended Axis
    '''
    if len(origin) < length:
        print("Please make sure of the length of origin is more than len")
        return False
    step = len(origin) / length
    targetX = []
    for each in range(length):
        pos = int(each*step)
        targetX.append(origin[pos])

    return targetX

def LSMethodConstructArray(rawArray, pOrder=0, type=0):
    '''
    input the original array,
    output the constructed XArray and YArray
    '''
    if not isinstance(rawArray, np.ndarray):
        iArray = np.array(rawArray)
    else:
        iArray = rawArray

    p = pOrder

    if type is const_stat.NOCONST_NOTREND_DFTEST:
        iXArraytmp = iArray[:-1].T
        iYArray = iArray[1:].T
        iXArray = iXArraytmp

    elif type is const_stat.CONST_NOTREND_DFTEST:
        iXArraytmp = iArray[:-1].T
        iYArray = iArray[1:].T
        iOne = np.ones((iYArray.size,1)).T
        iXArray = np.hstack((iOne,iXArraytmp))

    elif type is const_stat.CONST_TREND_DFTEST:
        iXArraytmp = iArray[:-1].T
        iYArray = iArray[1:].T
        iOne = np.ones((iYArray.size, 1)).T

        iTime = []
        for i in range(iArray.size-1):
            iTime.append(i+2)
        iTrendTime = np.array(iTime)
        iTmpArr = np.hstack((iOne,iTrendTime))
        iXArray = np.hstack((iTmpArr,iXArraytmp))

    elif type is const_stat.NOCONST_NOTREND_ADFTEST:
        iXArraytmp = iArray[:-1]
        iYArray = iArray[p:].T
        iArr = iXArraytmp[1:] - iXArraytmp[:-1]
        iTmpArr = iXArraytmp[p-1:].T
        iCtr = True
        for i in range(np.size(iYArray)):
            if iCtr is True:
                iTmpX = iArr[i:p-1+i]
                iCtr = False
            else:
                iTmpX = np.vstack((iTmpX,iArr[i:p-1+i]))
        iXArray = np.hstack((iTmpX,iTmpArr))

    elif type is const_stat.CONST_NOTREND_ADFTEST:
        iXArraytmp = iArray[:-1]
        iYArray = iArray[p:].T
        iArr = iXArraytmp[1:] - iXArraytmp[:-1]
        iTmpArr = iXArraytmp[p-1:].T
        iCtr = True
        for i in range(np.size(iYArray)):
            if iCtr is True:
                iTmpX = iArr[i:p-1+i]
                iCtr = False
            else:
                iTmpX = np.vstack((iTmpX,iArr[i:p-1+i]))
        iOnes = np.ones((iYArray.size,1))
        iTmpX = np.hstack((iTmpX,iOnes))
        iXArray = np.hstack((iTmpX,iTmpArr))

    elif type is const_stat.CONST_TREND_ADFTEST:
        iXArraytmp = iArray[:-1]
        iYArray = iArray[p:].T
        iArr = iXArraytmp[1:] - iXArraytmp[:-1]
        iTmpArr = iXArraytmp[p-1:].T
        iCtr = True
        for i in range(np.size(iYArray)):
            if iCtr is True:
                iTmpX = iArr[i:p-1+i]
                iCtr = False
            else:
                iTmpX = np.vstack((iTmpX,iArr[i:p-1+i]))
        iTime = []
        for j in range(np.size(iYArray)):
            iTime.append(p+1+j)
        iTrend = np.array(iTime)
        iOnes = np.ones((iYArray.size,1))
        iTmpX = np.hstack((iTmpX,iOnes))
        iTmpX = np.hstack((iTmpX, iTrend.T))
        iXArray = np.hstack((iTmpX,iTmpArr))
    else:
        print("please input the right type")
        iXArray = []
        iYArray = []

    return iXArray,iYArray

def GetCoeffSTD(xArray, yArray,coeffiency, p=1, type=0):
    '''
    input: xArray, yArray and the coeffiency array
    output: coefficiency standard deviation array
    '''

    if not isinstance(xArray, np.ndarray) or not isinstance(yArray, np.ndarray) or not isinstance(coeffiency,np.ndarray):
        xArr = np.array(xArray)
        yArr = np.array(yArray)
        coeArr = np.array(coeffiency)

    else:
        xArr = xArray
        yArr = yArray
        coeArr = coeffiency

    xShape = np.shape(xArray)

    if type is const_stat.NOCONST_NOTREND_DFTEST or type is const_stat.NOCONST_NOTREND_ADFTEST:
        rank = xShape[0]-p
    elif type is const_stat.CONST_NOTREND_DFTEST or type is const_stat.CONST_NOTREND_ADFTEST:
        rank = xShape[0]-p-1
    elif type is const_stat.CONST_TREND_DFTEST or type is const_stat.CONST_TREND_ADFTEST:
        rank = xShape[0] - p - 2

    yArrEsm = xArr.dot(coeArr)
    yEpsilon = yArr-yArrEsm
    std = (yEpsilon.T.dot(yEpsilon))/rank

    iOnes = np.ones((1,len(coeArr)))
    itmp = xArr.transpose().dot(xArr)
    itmpInv = np.linalg.inv(itmp)
    iCoefficiencySTD = std*(iOnes.dot(itmpInv).dot(iOnes.T))

    return np.sqrt(iCoefficiencySTD)

def PPTesttau(xArray, yArray, coefficency, t, sigma, q=1, type=0):
    '''
    xArray: input the estimator
    '''
    if not isinstance(xArray, np.ndarray) or not isinstance(yArray, np.ndarray) or not isinstance(coefficency, np.ndarray):
        xArray = np.array(xArray)
        yArray = np.array(yArray)
        coefficency = np.array(coefficency)

    iResidual = np.array(yArray - xArray.dot(coefficency))
    iGamma = []
    iQ = []
    iGamma.append(np.dot(iResidual.T, iResidual))
    for i in range(1, q + 1):
        iGamma.append(np.dot(iResidual[:-q].T, iResidual[q:]))
        iQ.append(i)

    iGamma = np.array(iGamma)
    iLength = np.shape(iResidual)[0]
    iGamma0 = iGamma[0]/iLength

    if type is const_stat.NOCONST_NOTREND_DFTEST:
        iVar = iLength - 1
    elif type is const_stat.CONST_NOTREND_DFTEST:
        iVar = iLength - 2
    elif type is const_stat.CONST_TREND_DFTEST:
        iVar = iLength -3
    else:
        iVar = iLength - 1
        print("please make sure that input the right type to be used!")

    iMSE = iGamma[0]/iVar

    if q == 0:
        tau = t
    elif q>0:
        jQ = np.array(iQ)
        jQ = 1 - jQ/(q+1)
        itmp = jQ.dot(iGamma[1:])
        ilamda2 = iGamma0 + itmp*2
        ilamda = np.sqrt(ilamda2)
        iGamma0SQRT = np.sqrt(iGamma0)
        tau = t*iGamma0SQRT/ilamda + (itmp*iLength*sigma)/(ilamda*iMSE)
    else:
        print("wrong parameter of q:{}".format(q))
        tau = 0xFFFF

    return tau

def LSMethod(xArray, yArray):
    '''
    xArray: this is the X array to be calculated
    yArray: this is the Y array to be calculated
    :return: parameter of least sqare method(最小二乘法估计参数)
    note: support X*Y
    '''
    if not isinstance(xArray, np.ndarray) and not isinstance(yArray, np.ndarray):
        print("please input the right parameter!")
        return False

    xDim = np.shape(xArray)
    yDim = np.shape(yArray)

    if xDim[0] != yDim[0]: # make sure x-row == y-column
        print("please make sure of the column of X is equal to row of Y")
        return False
    '''
    the following three line of code should be removed from this function in order to decouple.
    should bring this three line into the outer function
    
    row = xArray.size
    xArray = np.reshape(xArray,(row, 1))
    xArray = np.insert(xArray, 0, 1, axis=1)
    '''

    xArrayTranspose = xArray.transpose()
    xArrayTmp = xArrayTranspose.dot(xArray)
    xArrayTmpInv = np.linalg.inv(xArrayTmp)
    xTmp = np.array(xArrayTmpInv.dot(xArrayTranspose))

    paraList = xTmp.dot(yArray)
    
    return paraList

class StatFunction(object):
    def __init__(self, data):
        if not isinstance(data, np.ndarray):
            print("please make sure of the type of input is numpy datatype")
            return
        self.data = data
        self.mean = np.mean(self.data)
        self.var = np.var(self.data)
        self.dataRemoveMean = self.data - self.mean
        self.std = np.std(self.data)

    def setDataType(self, dataType = 0):
        if dataType == const.DATATYPE['RD'] :
            iData = self.data
        elif dataType == const.DATATYPE['RDA'] :
            iData = np.abs(self.data)
        elif dataType == const.DATATYPE['RDS'] :
            iData = self.data ** 2
        elif dataType == const.DATATYPE['RDMM'] :
            iData = self.dataRemoveMean
        elif dataType == const.DATATYPE['RDMMA'] :
            iData = np.abs(self.dataRemoveMean)
        elif dataType == const.DATATYPE['RDMMS'] :
            iData = self.dataRemoveMean ** 2
        else :
            print("please input the right dataType:%s" % dataType)
            iData = 0
        self.currData = iData
        self.currType = dataType

    def getCurData(self):
        return self.currData

    def getMean(self):
        iData = self.getCurData()
        mean = np.mean(iData)
        return mean

    def getMeanDiagnostic(self, confidence=0.95):
        student = [0.25,0.1,0.05,0.025,0.01,0.005]

        dataLen = len(self.getCurData())
        std = np.std(self.getCurData())
        alpha = 0.05
        if dataLen >= len(const_stat.TN):
            index = len(const_stat.TN)-1
        else:
            index = dataLen

        iTalpha = 0

        for i in range(len(student)):
            if const_stat.TValue[i][0] == alpha:
                iTalpha = const_stat.TValue[i][index]
                break
        iTvalue = (std/dataLen)**0.5*iTalpha

        return iTvalue

    def getVar(self):
        iData = self.getCurData()
        std = np.std(iData)
        return std

    def getSkewness(self):
        iData = self.getCurData()
        iMean = np.mean(iData)
        iVar = np.var(iData)

        iSkewness = np.mean((iData - iMean) ** 3) / (iVar ** 1.5)
        return iSkewness

    def getKurt(self):
        iData = self.getCurData()
        iMean = np.mean(iData)
        iVar = np.var(iData)

        iKurt = np.mean((iData - iMean)**4)/(iVar**2)
        return iKurt

    def __calcRk__(self, data, order):
        if order >= len(data):
            print("please input the right order!")
            return

        iRk = []
        data = data - np.mean(data)

        iRk.append(np.dot(data[:], data[:]))

        for i in range(1, order+1):
            iRk.append(np.dot(data[:-i], data[i:]))
        return iRk

    def __calcACF__(self, data, order, bias=True):

        if not isinstance(data, np.ndarray):
            print("please make sure of the input type is numpy.ndarray!")
            return
        iRk = self.__calcRk__(data, order)

        dataLen = len(data)
        iRk = np.array(iRk)

        if bias is not True: # unbias estimation
            for i in range(0, len(iRk)):
                iRk[i] = iRk[i]*dataLen/(dataLen-i)

        return iRk[1:]/iRk[0]

    def getACF(self, order, bias=True):
        dataArr = self.getCurData()
        return self.__calcACF__(dataArr, order, bias)

    def __YuleWalker__(self, data, order, bias):

        iRk = self.__calcRk__(data, order)
        dataLen = len(data)

        if bias is not True:
            for i in range(0,len(iRk)):
                iRk[i] = iRk[i]*dataLen/(dataLen-i)

        iRArray = toeplitz(iRk[:-1]) # construct the toeplitz array

        return np.linalg.solve(np.array(iRArray), np.array(iRk)[1:])

    def getPACF(self, order, bias=True):
        iPACF = []
        dataArr = self.getCurData()
        for i in range(1, order+1):
            iArr = self.__YuleWalker__(dataArr, i, bias)
            iPACF.append(iArr[-1])
        return iPACF

    def getDiagACF(self, confidence=0.95):
        '''
        if the confidence is 0.95, then the coefficiency should be 2, that is 2*sigma,
        currently, sqrt is the sigma
        '''
        isqrt = np.sqrt(len(self.getCurData()))
        print("length of current data:%s" % len(self.getCurData()))
        coef = 2
        if confidence == 0.95:
            coef = 2
        elif confidence == 0.99:
            coef = 3

        return coef/isqrt,-coef/isqrt

    def getDiagnosticWhiteNoise(self, diagArr):
        '''
        basic assumption:
        when {Xt} ~ white noise distribution, ROUk ~norm(0,1/T)
        H0: white noise
        H1: refuse white noise
        1. when abs(ROU1) > 2/sqrt(T), refuse H0
        2. when many abs(ROUk) > 2/sqrt(T), refuse H0
        3. t = sqrt(T) * Rouk, when abs(t) > 3, refuse H0
        '''
        if not isinstance(diagArr, np.ndarray):
            diagArr = np.array(diagArr)
            print("please make sure of the array type is numpy.ndarray!")

        tmpT = np.sqrt(len(self.getCurData()))
        iDiagnostic = diagArr*tmpT

        return iDiagnostic

    def getDiagnosticLjungBox(self, order, confidence=0.05, fitPara = 0):
        '''
        condition:
        if the model is ARMA(p,q), then the "N" of X2 should be m-(p+q)
        order: the input N
        confidence: the probability of X2 should be met
        fitPara: number of p+q
        general, order = ln(T), T = length of array
        '''
        tmpConf = [0.995,0.99,0.975,0.95,0.9,0.75,0.5,0.25,0.1,0.05,0.025,0.01,0.005]
        iloc = 0
        iControl = True

        for iconf in range(len(tmpConf)):
            if confidence == tmpConf[iconf]:
                iControl = False
                break
            else:
                iloc = iloc +1
        if iControl is True:
            print("please make sure of the value of confidenc is valid!")
            return

        dataLen = len(self.getCurData())
        dataArr = self.getCurData()
        iRk = self.__calcRk__(dataArr, order + 1)

        iRouk = np.array(iRk[1:]/iRk[0])
        iRoukAdj = []
        N = order - fitPara

        for i in range(N):
            iRoukAdj.append(iRouk[i]*dataLen*(dataLen+2)/(dataLen - i))
        iRoukAdj = np.array(iRoukAdj)

        tmpValue = iRoukAdj.dot(iRouk[:N])
        X2Vale = const_stat.X2Value[iloc][N]

        return tmpValue,X2Vale

    def getDFTest(self, data):
        '''
        get the DT Test result
        Test the following three model respectively
        suppose:
        y = alpha + beta * x + gamma * t+ epsilon, epsilon ~ normal(0,1)

        a) test the following model only
        y = beta * x + epsilon
        b) test the model:
        y = alpha + beta * x + epsilon
        c) test the model:
        y = alpha + beta * x + gamma * t + epsilon
        '''
        if not isinstance(data, np.ndarray):
            iData = np.array(data)
            print("please input the numpy data type first!")
        else:
            iData = data
        con
        pass

    def getADFTest(self, data):
        '''
        get the result of ADF Test
        '''
        pass

    def getPPTest(self, data):
        '''
        get the result of PP Test
        '''
        pass
