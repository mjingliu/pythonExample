#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from builtins import object

import TSASkills as tss
import infrastructure as infra

class ARModel(object):
    '''
    input: time series
    output:
    '''
    def __init__(self, data):
        '''
        输入的数据应该是通过平稳性检测过的数据
        '''
        self.basicStat = tss.StatisticsModel(data)

    def Regression(self):
        # 回归
        '''
        1. 阶数估计，ACF计算/PACF计算
        2. 根据准则，确认阶数
        3. 构造数据，进行最小二乘估计，获取系数以及对应的系数方差
        notes:
        AR(P), 主要是看PACF的结尾
        MA(Q), 主要是看ACF的结尾
        '''
        iOrderLimit = self.basicStat.getOrder()
        iACF = self.basicStat.getACF(iOrderLimit)
        iPACF = self.basicStat.getPACF(iOrderLimit)

        iThreshold = self.basicStat.getACFPACFCoefTest()

        iACFIndex = self.__getOrderIdx__(iACF, iThreshold)
        iPACFIndex = self.__getOrderIdx__(iPACF, iThreshold)

        

    def __getOrderIdx__(self, data, threshold):
        iArr = []
        for i in range(len(data)):
            if abs(data[i]) > abs(threshold[0]):
                iArr.append(i)
        return iArr

    def ARTest(self):
        # AR检测
        pass

    def Estimation(self):
        # 估计，获取到对应的参数以及参数对应的方差
        pass

    def Prediction(self):
        # 预测
        pass

class MAModel(object):
    def __init__(self):
        pass

class ARMAModel(object):
    def __init__(self):
        pass

class GARCHModel(object):
    def __init__(self):
        pass
