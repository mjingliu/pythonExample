#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from builtins import object, len

import TSASkills as tss
import infrastructure as infra
import const_stat as cs
import numpy as np

class ARModel(object):
    def __init__(self, data):
        '''
        输入的数据应该是通过平稳性检测过的数据
        '''
        self.basicStat = tss.StatisticsModel(data)
        self.constructData = tss.DataConstruct(data)
        self.order = {}
        self.iY = {}
        self.iX = {}
        self.iCoef = {}

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

        ACF/PACF ->AIC/SIC -> LB/LM ->coef confirmation -> in-band prediction -> out-band prediction
        如果LB/LM检测还有自相关性，说明模型不合理而不是系数不对，需要重新假定模型。
        '''
        # 计算出 大致的阶数
        for key in cs.order_type:
            iOrder, iOrderList = self.__getPOrder__(type=cs.order_type[key])
            iY, iX = self.Estimation(iOrder, LSE=False)
            iCoef, iSSR = self.Estimation(iOrder)
            self.order[key] = iOrder
            self.iY[key] = iY
            self.iX[key] = iX
            self.iCoef[key] = iCoef

        # 对阶数对应的回归方程进行检验，
        
        '''
        # ACF/PACF，AIC,SIC三种不同的方法计算得到三种系数，如果方法具有一致性，则三种方法得到的系数个数应该是一致的。
        # 如果不一致的话，需要确定哪个方法最合适。
        # 在不一致的情况下，进行LB/LM检测，如果有残差还存在自相关性，则该系数不合适。
          如果残差不存在自相关性，则系数少者为最终选项
        '''

        return

    def __minOrder__(self):

        iLen = len(self.order)

        pass

    def __maxOrder__(self):
        pass

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
        # AR检测，具体检测什么东西呢？暂时未知
        pass

    def ErrorTest(self, iY, iX, iCoef):
        '''
        残差检测，1.残差的自相似性检测，LB检测；2. 残差的正态性检测，JB检测
        若LB检测中，没有自相关性，则说明模型是正确的，
        若LB检测中，残差有自相关性，说明模型还需要进一步分析，也就是说，当前的模型不能描述所有的信息
        当前模型的残差中还有自相关信息没有被描述，需要重新选择分析选择模型
        '''

        iError = self.Errors(iY, iX, iCoef) # 该函数的适用错误，理由如下：在self.Errors函数中，使用了iY和iX，但是iY和iX是二维数组
                                # 故，调用该函数之前，应该输入对应的X和Y，用以计算对应的误差

        tValue, pValue = tss.StatisticsTSTest.getLBTestResult(iError, numofpara=self.order)
        return tValue, pValue

    def Errors(self,iY, iX, iCoef):
        # 计算误差矩阵
        iY = np.asarray(iY)
        iX = np.asarray(iX)
        iCoef = np.asarray(iCoef)
        iError = iY - iX.dot(iCoef)
        return iError

    def Estimation(self, order, LSE=True):
        iY, iX = self.constructData.ConstructPOrderArray(order)
        # 估计，获取到对应的参数以及参数对应的方差
        if LSE is True:
            iLSE = infra.LSEstimation(iX, iY, 0)
            return iLSE.getEstimator(), iLSE.getSSR()
        # 返回计算LSE的构造数据
        return iY, iX

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
