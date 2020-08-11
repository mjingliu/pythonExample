#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import math
import const
from fractal import Fractal as frc

class StockAnalysis(object):
    '''
    this class is mainly for time domain analysis of stock data
    '''
    def __init__(self, data, date):
        '''
        1. pass the para "data" which is the real stock price,
            date is the corresponding series of data
        '''
        self.aArrData = data
        self.aDate = date

    def calDividendTimes(self):
        aTimes = []
        for i in range(len(self.aArrData)):
            if i > 0 and self.aArrData[i] < const.coeffiency * self.aArrData[i-1]:
                aTimes.append(i)
        return aTimes

    def getDividendDate(self):
        if len(self.aArrData) != len(self.aDate):
            print("please make sure of inputing the same length of data/date!")
        aDates = []
        aTimes = self.calDividendTimes()
        for i in aTimes:
            aDates.append(self.aDate[i])
        return aDates

    def getEffectiveData(self):
        '''
        basic logic: when the dividend take place, use the latest data to take analysis
        1. get the data those are to be analyzed
        '''
        aTimes = self.calDividendTimes()

        if len(aTimes) > 0:
            return self.aArrData[aTimes[len(aTimes) - 1]:]
        else:
            return self.aArrData

    def getLgYieldsArr(self):
        '''
        1. get the ln ratio
        2. formula is :log[Pt/P(t-1)]
        '''
        aArrData = self.getEffectiveData()

        aArr = np.array(aArrData)
        aArrTmp = np.log(aArr)
        aArrLog = aArrTmp[1:] - aArrTmp[:-1]
        return aArrLog

class StockAnalysisFractal(object):
    '''
    this class is mainly for fractal domain stock data analysis
    '''
    def __init__(self, iArr):
        if isinstance(iArr,list):
            self.ifrac = frc(iArr)
        else:
            print("please make sure of the input data is list type")
    def inputWindows(self, win):
        self.sample = win