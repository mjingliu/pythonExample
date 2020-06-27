#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import numpy as np
import math

def Hust (iArr, sample):
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
    if len(iArr) < (int(sample)*2):
        return False
    iArr = np.array(iArr)
    blockLen = iArr.size / sample
    iArrR = []
    iArrS = []
    iArrRSValue = []
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
        iArrRSValue.append(math.log10(tmpR/tmpS))

    return iArrRSValue
