#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from builtins import object

import TSASkills as tss
import infrastructure as infra

class ARModel(object):
    def __init__(self, data):
        self.statBasic = tss.StatisticsModel(data)
        
    def Regression(self):
        # 回归
        pass

    def ARTest(self):
        # AR检测
        pass

    def Errors(self):
        # 误差
        pass

    def Estimation(self):
        # 估计
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
