#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import Any

import pymysql
import os,sys
import numpy as np
import matplotlib.pyplot as plt
import util
from fractal import Fractal
import math
import StockDB as db
import const
#import pywt as wvlt

'''
1. 假设每一个行业都是以一年为周期，也就是说一年为通用周期
2. 某些行业可能是以季节为周期
3. 某些行业是以假期为周期
4. 从周期的维度看，在时域上，以某个固定的windows，获取距离最小的部分，
5. 需要在所有的stock数据中，进行分析，看一下是否有周期类型的数据，如果有的话，可以做后续指导
6. 高频部分代表的是波动和细节，低频部分代表的是整体趋势，如何界定高频和低频，是需要判断的一个问题，需要有判断准则。
7，如果去除低频数据，
8. 需要按照行业来划分类别，有可能是每一个行业有属于行业自己的周期
9. 按照地域划分，看一下地域的影响
'''

'''
1. 把到目前为止所有的fft/ifft变化的代码内容都清理掉
2. 把小波变化的内容增加进来，看一下小波域中的数据是什么样子的，看看能有什么发现
3. 小波逆变换能否恢复完整恢复数据？
4. 正确调整小波参数，用以模拟stock line
'''
'''
使用分形对数据进行分析
具体步骤如下：
1. 使用R/S方法，找到该股票对应的Hust指数是多少
    此处的n可以选用很多个数值，使用不同的n可能有不同的Hust，看看是否有对应关系
2. 使用R/S方法，是否对股票的不同阶段，有不同的Hust指数
3. 根据Hust指数，使用公式lg(R/S)n = lgC + H*lgn，测试一下当n增加“1”时，对应的Xn+1的值是多少？
具体计算步骤如下：
a. 在需要分析的采样样本(S)中，把采样划分为M个包含n个采样的数据块，也就是说 S = M*n
b. 对每一个n个采样序列Xi计算对应的均值，X = (X1 + X2 + ...+Xn)/n
c. 对每一个n个采样序列Xi计算对应的误差，detXi = Xi-X
d. 对每一个n个采样序列Xi，计算每一个Xi对应的累计误差，Xierror = detX0 + detX1 +...+detXi
e. 计算n个采样序列的R值，R = max(Xierror) - min(Xierror), i = 0,1,2...n-1
f. 计算n个采样序列的S值，S = sqrt((detX0 * detX0 + detX1*detX1 + detX2*detX2+...+detXn-1*detXn-1)/(n*n))

'''

coeffiency: float = 0.85

myDB = db.stockDB(user="mingjliu", password="qwe`1234")
tblName = const.tblName
dbName = const.dbName
stockCode = "601155.SH"

try:
    tmpList = list(myDB.selectData(tblName, dbName, stockCode))
    print("all the Select data is :%d " % len(tmpList))
    aList = []
    aListClose = []
    aListDate = []
    aListCloseIndex = []

    for i in range(len(tmpList)):
        aList.append(tmpList[i][0])
        aListDate.append(tmpList[i][1])
        aListClose.append(tmpList[i][2])

    aList.reverse()
    aListDate.reverse()
    aListClose.reverse()
    # 找到对应数据的跳跃点位置索引，用以区分对应的区段来获取H值
    # 例如：002415股票：从上市到2020年6月20号，一共有5次阶跃跳变，分别为：第211天，第487天，第745天，第1398天，第1639天
    # 每一次价格的阶跃跳变都是以大于10%的价格跳变，是股票增发价格分摊导致，故应该在每一个对应区间内来分析数据
    for i in range(len(aListClose)):
        if i > 0 and aListClose[i] < coeffiency * aListClose[i-1]:
            aListCloseIndex.append(i)
    print(aListCloseIndex)

    aListLen = len(aListCloseIndex)

    if aListLen > 0:
        iArr = np.array(aListClose[aListCloseIndex[aListLen-1]:])
    else:
        iArr = np.array(aListClose)

    iArrOri = np.log10(iArr)
    iArr1 = iArrOri[:-1]
    iArr2 = iArrOri[1:]
    iArr = iArr2-iArr1

    fra = Fractal(iArr[-20:])
    print(len(iArr))
    sample = [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    #sample = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    #sample = [3, 4, 5]

    #sample = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 17, 19, 21, 23, 28, 36, 50, 70, 90]
    #sample = [3,20]
    #iHArrX = math.log10(sample)
    initCtr = True
    iAxisLen = 0

    #dimArrayX = np.array((len(sample),2))
    #dimArrayY = np.array((len(sample),1))
    dimArrayX = []
    dimArrayY = []
    fraArrSize = fra.getArrSize()

    for itmp in range(len(sample)):
        iHArrX = math.sqrt(sample[itmp])
        #iHArrX = math.log10(sample[itmp])
        if fraArrSize < sample[itmp]:
            print("len of iArr:%s" % len(iArr))
            print("sample: %s" % sample[itmp])
            continue
        dimArrayX.append(iHArrX)

        #fra.Sample(sample[itmp])
        fra.SampleSinglePoint(sample[itmp], const.FORWORD)
        iHArr = np.array(fra.getVnValue())
        iHArrRS = np.array(fra.getRSValue())
        #dimArrayY.append(iHArrRS.mean())
        dimArrayY.append(iHArr)
        '''
        iHArrtmp = iHArr / iHArrX

        if True == initCtr:
            iHArrFinal = np.array(iHArrtmp)
            iHXFinal = np.linspace(iHArrX, iHArrX, num=len(iHArr))
            iAxisLen = len(iHArrFinal)
            #iHXFinal = np.linspace(1, iAxisLen, num=iAxisLen)
            #print(iHXFinal)
            iHXtmp = iHXFinal
            initCtr = False
        else:

            iHArrFinal = np.append(iHArrFinal,iHArrtmp)
            #iHXExtend = util.extendAxis(iHXtmp,len(iHArrtmp))
            iHXExtend = np.linspace(iHArrX, iHArrX, num=len(iHArr))
            iHXFinal = np.append(iHXFinal,np.array(iHXExtend))
        '''
    np.set_printoptions(suppress=True, precision=4)

    dimArrayXtmp = np.array(dimArrayX)
    dimArrayYtmp = np.array(dimArrayY)

    para = util.LSMethod(dimArrayXtmp, dimArrayYtmp)
    print(para)
    '''
    fra.getFraPeriod()
    ArrayX = fra.getFraPeriodWindow()
    ArrayY = fra.getFraPeriodValueofWin()
    plt.scatter(ArrayX, ArrayY)
    plt.plot(ArrayX, ArrayY)
    '''
    #plt.scatter(iHXFinal, iHArrFinal)
    plt.scatter(dimArrayX, dimArrayY)
    dimArrayYtmp = para[0] + np.float(para[1]) * dimArrayXtmp
    plt.plot(dimArrayXtmp,dimArrayYtmp)

    #plt.plot(aListDate,aListClose)
    plt.rcParams['font.sans-serif'] = ['SimHei'] #设置中文字体
    plt.title("采样：{}".format("8"))
    plt.show()

except Exception as e:
    print("Exception: %s" % e)
finally:
    myDB.exitDB()