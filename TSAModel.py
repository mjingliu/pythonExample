#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from builtins import object, len

import TSASkills as tss
import infrastructure as infra
import const_stat as cs

class ARModel(object):
    def __init__(self, data):
        '''
        输入的数据应该是通过平稳性检测过的数据
        '''
        self.basicStat = tss.StatisticsModel(data)
        self.constructData = tss.DataConstruct(data)

    def Regression(self):
        # 回归
        '''
        1. 阶数估计，ACF计算/PACF计算
        2. 根据准则，确认阶数
        3. 构造数据，进行最小二乘估计，获取系数以及对应的系数方差
        notes:
        AR(P), 主要是看PACF的截尾
        MA(Q), 主要是看ACF的截尾

        如果通过ACF确认AR阶数的话，由于是拖尾，所以，需要从高到底来选择对应的系数，知道剩余系数占据比例大于68.3%(1 sigma)或者95%(2 sigma)
        如果通过PACF确认MA阶数的话，方法类似于ACF的拖尾方法
        通常选择的是68.3%为门限
        '''
        iOrder = self.__getPOrder__()
        iCoef, iSSR = self.Estimation(iOrder)

        return

    def __getOrderIdx__(self, data, threshold):
        iArr = []
        for i in range(len(data)):
            if abs(data[i]) > abs(threshold[0]):
                iArr.append(i)
        return iArr

    def __getPOrder__(self, type=cs.ORDER_TYPE_ACF_PACF):
        iOrderLimit = self.basicStat.getOrder()

        if type is cs.ORDER_TYPE_ACF_PACF:
            #iACF = self.basicStat.getACF(iOrderLimit)
            iPACF = self.basicStat.getPACF(iOrderLimit)

            iThreshold = self.basicStat.getACFPACFCoefTest()

            #iACFIndex = self.__getOrderIdx__(iACF, iThreshold)
            iPACFIndex = self.__getOrderIdx__(iPACF, iThreshold)

            iLen = len(iPACFIndex)
            return iPACFIndex[iLen - 1], iPACFIndex

        elif type is cs.ORDER_TYPE_AIC or type is cs.ORDER_TYPE_SIC:
            iAIC = []
            iSIC = []
            iSel = tss.StatModelSelection()
            for i in range(iOrderLimit):
                iCoef, iSSR = self.Estimation(i+1)
                iAIC.append(iSel.getAIC(iSSR, i+1))
                iSIC.append(iSel.getSIC(iSSR, i+1))

        else:
            return False, False

        if type is cs.ORDER_TYPE_AIC:
            iMin = min(iAIC)
            iIdx = iAIC.index(iMin)
            return iIdx+1, iAIC

        if type is cs.ORDER_TYPE_SIC:
            iMin = min(iSIC)
            iIdx = iSIC(iMin)
            return iIdx+1, iSIC

    def ARTest(self):
        # AR检测
        pass

    def Errors(self):
        # 误差
        pass

    def Estimation(self, order):
        # 估计，获取到对应的参数以及参数对应的方差
        iY, iX = self.constructData.ConstructPOrderArray(order)
        iLSE = infra.LSEstimation(iX, iY, 0)
        return iLSE.getEstimator(), iLSE.getSSR()

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
