#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import math
import const
from fractal import Fractal

class StockAnalysis(object):
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
