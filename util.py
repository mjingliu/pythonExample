#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np

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
    paraList = xArrayTmpInv.dot(xArrayTranspose).dot(yArray)

    return paraList

class StatFunction(object):
    def __init__(self, data):
        if not isinstance(data, np.ndarray):
            print("please make sure of the type of input is numpy datatype")
            return
        self.data = data
        self.mean = np.mean(self.data)
        self.var = np.var(self.data)

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

