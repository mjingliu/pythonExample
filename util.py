#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from scipy.linalg import toeplitz
import const_stat

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

def LSMethod(xArray, yArray):
    '''
    xArray: this is the X array to be calculated
    yArray: this is the Y array to be calculated
    :return: parameter of least sqare method(最小二乘法估计参数)
    note: support X*Y
    '''
    if type(xArray) is not np.ndarray or type(yArray) is not np.ndarray:
        print("please input the right parameter!")
        return False
    yArray = np.array(yArray)
    xArray = np.array(xArray)

    xDim = np.shape(xArray)
    yDim = np.shape(yArray)

    if xDim[0] != yDim[0]: # make sue column == row
        print("please make sure of the column of X is equal to row of Y")
        return False

    row = xArray.size
    xArray = np.reshape(xArray,(row, 1))

    xArray = np.insert(xArray, 0, 1, axis=1)

    xArrayTranspose = xArray.transpose()
    xArrayTmp = xArrayTranspose.dot(xArray)
    xArrayTmpInv = np.linalg.inv(xArrayTmp)
    xTmp = np.array(xArrayTmpInv.dot(xArrayTranspose))
    print("xTmp shape: {}".format(np.shape(xTmp)))
    print("yArray shape: {}".format(np.shape(yArray)))
    #paraList = xTmp.dot(yArray)
    paraList = np.dot(xTmp,yArray)
    print("paraList shape: {}".format(np.shape(paraList)))
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

    def getMean(self):
        return self.mean

    def getVar(self):
        return self.var

    def getSkewness(self):
        iMean = self.mean
        iVar = self.var
        self.skewness = np.mean((self.data - iMean)**3)/(iVar ** 1.5)
        return self.skewness

    def getKurt(self):
        iMean = self.mean
        iVar = self.var
        self.kurt = np.mean((self.data - iMean)**4)/(iVar**2)
        return self.kurt

    def __calcRk__(self, data, order):
        if order >= len(data):
            print("please input the right order!")
            return

        iRk = []

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
        return self.__calcACF__(self.dataRemoveMean, order, bias)

    def getAbsACF(self, order, bias=True):
        return self.__calcACF__(np.abs(self.dataRemoveMean), order, bias)

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
        for i in range(1, order+1):
            iArr = self.__YuleWalker__(self.dataRemoveMean, i, bias)
            iPACF.append(iArr[-1])
        return iPACF

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

        tmpT = np.sqrt(len(self.data))
        iDiagnostic = np.abs(diagArr*tmpT)

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

        dataLen = len(self.dataRemoveMean)
        iRk = self.__calcRk__(self.dataRemoveMean, order+1)

        iRouk = np.array(iRk[1:]/iRk[0])
        iRoukAdj = []
        N = order - fitPara

        for i in range(N):
            iRoukAdj.append(iRouk[i]*dataLen*(dataLen+2)/(dataLen - i))
        iRoukAdj = np.array(iRoukAdj)

        tmpValue = iRoukAdj.dot(iRouk[:N])
        X2Vale = const_stat.X2Value[iloc][N]

        return tmpValue,X2Vale

