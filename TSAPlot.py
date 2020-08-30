#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from builtins import object

import matplotlib.pyplot as plt


class TPlot(object):
    def __init__(self, xdata, ydata, *args, **kwargs) :
        '''
        *args: stock code,
        '''
        self.xdata = xdata
        self.ydata = ydata
        self.args = args
        self.kwargs = kwargs

    def __basicSetting__(self) :
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
        argsLen = len(self.args)
        if argsLen >= 1 :
            str = []
            for i in range(argsLen) :
                str.append(self.args[i])
            plt.title("{}".format(str))
        else :
            print("no args input")

    def plotBar(self) :
        self.__basicSetting__()
        plt.bar(self.xdata, self.ydata)
        plt.show()

    def plotLine(self) :
        self.__basicSetting__()
        plt.plot(self.xdata, self.ydata)
        plt.show()

    def plotScatter(self) :
        self.__basicSetting__()
        plt.scatter(self.xdata,self.ydata)
        plt.show()
