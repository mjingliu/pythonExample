#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import numpy as np
import math
import const

class Fractal(object):

    def __init__(self, iArr):
        self.iArrRSValue = []
        self.iArrVnValue = []
        self.iRList = []
        self.iSList = []
        self.iPeriodPos = []
        self.iPeriodWindow = []
        self.iPeriodValueofWin = []
        self.iArr = iArr

    def __Hust__ (self, iArr, sample):
        '''
        iArr: 该参数为传入Hust函数的矩阵
        sample: 该参数为按照该sample值划分iArr矩阵为len(iArr)%sample个小的采样序列
        return：为该iArr对应的Hust值

        具体计算步骤如下：
        a. 在需要分析的采样样本(S)中，把采样划分为M个包含n个采样的数据块，也就是说 S = M*n
        b. 对每一个n个采样序列Xi计算对应的均值，X = (X1 + X2 + ...+Xn)/n
        c. 对每一个n个采样序列Xi计算对应的误差，detXi = Xi-X
        d. 对每一个n个采样序列Xi，计算每一个Xi对应的累计误差，Xierror = detX0 + detX1 +...+detXi
        e. 计算n个采样序列的R值，R = max(Xierror) - min(Xierror), i = 0,1,2...n-1
        f. 计算n个采样序列的S值，S = sqrt((detX0 * detX0 + detX1*detX1 + detX2*detX2+...+detXn-1*detXn-1)/(n*n))

        采用最小二乘法获取到对应的参数，
        若输入的参数len(iArr) < (sample *2),则说明传入的参数个数太少，不做任何处理，只反馈输入参数个数太少的告警
        '''
        if len(iArr) < int(sample):
            return False
        iArr = np.array(iArr)

        samModular = iArr.size % sample
        iArr = iArr[samModular:]

        blockLen = iArr.size / sample

        #print("sample: %s, samModular: %s, blockLen:%s" % sample,samModular,blockLen)

        iArrR = []
        iArrS = []
        iArrRSValue = []
        iArrVnValue = []

        for each in range(int(blockLen)):
            tmpArr = np.array(iArr[each * sample: (each+1)*sample])
            tmpMean = tmpArr.mean() # mean
            tmpError = np.array(tmpArr-tmpMean) # error
            for i in range(len(tmpError)):
                if i != 0:
                    tmpError[i] += tmpError[i-1]
            tmpMax = tmpError.max()
            tmpMin = tmpError.min()
            tmpR = tmpMax-tmpMin # R
            iArrR.append(tmpR)
            tmpS = tmpArr.std() # S
            iArrS.append(tmpS)
            if tmpS == 0.0:
                print("\n this is tmpS==0.0")
                print(tmpArr)
                print("tmpR = %f" % tmpR)
                continue
            iArrRSValue.append(math.log10(tmpR / tmpS))
            iArrVnValue.append(tmpR/tmpS)

        self.iRList = iArrR
        self.iSList = iArrS
        self.iArrRSValue = iArrRSValue
        self.iArrVnValue = iArrVnValue
        #print("log10RS:%s" % iArrRSValue)
        print("VnValue:%s" % iArrVnValue)

    def Sample(self,sample):
        self.__Hust__(self.iArr,sample)

    def SampleSinglePoint(self, sample, direction):

        if type(self.iArr) is not np.ndarray:
            print("please confirm the inpur is ndArray type!")

        if direction == const.BACKWORD:
            iArrtmp = self.iArr[::-1]
        else:
            iArrtmp = self.iArr
        self.__Hust__(iArrtmp[:int(sample)], sample)

    def getArrSize(self):
        return len(self.iArr)

    def getVnValue(self):
        return self.iArrVnValue

    def getRSValue(self):
        return self.iArrRSValue

    def getRList(self):
        return self.iRList

    def getSList(self):
        return self.iSList

    def getFraPeriod(self):
        sample = [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
        for itmp in range(len(sample)):
            iArr = self.iArr[:sample[itmp]]
            self.__Hust__(iArr, sample[itmp])
            self.iPeriodValueofWin.append(self.iArrVnValue)
            self.iPeriodWindow.append(math.sqrt(sample[itmp]))

    def getFraPeriodWindow(self):
        return self.iPeriodWindow

    def getFraPeriodValueofWin(self):
        return self.iPeriodValueofWin
