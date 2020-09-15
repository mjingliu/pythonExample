#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from builtins import object
import infrastructure as inf

class StatisticsTest(object):
    def __init__(self):
        pass

    def __DFTest__(self, data, kind):
        '''
        input:
        data: the data which need to be tested
        kind: string type, which kind of type should be used to test, currently the following three kinds: nc, c, ct
        return:
        tvalue:
        pvalue:
        '''
        return

    def getDFTestResult(self, data, kind):

        return self.__DFTest__(data, kind)

    def __ADFTest__(self, data, kind):

        return

    def getADFTestResult(self, data, kind):

        return self.__ADFTest__(data, kind)

    def __PPTest__(self, data, kind):

        return

    def getPPTestResult(self, data, kind):

        return self.__PPTest__(data, kind)

    def __LBTest__(self):
        pass

    def getLBTestResult(self):

        return self.__LBTest__()

    def __LMTest__(self):
        pass

    def getLMTestResult(self):

        return self.__LMTest__()

    def __JBTest__(self, data, confidence):

        return

    def getJBTestResult(self, data, confidence=0.95):

        return self.__JBTest__(data, confidence)

class StatisticsBasic(object):
    def __init__(self, data):
        pass

    def __Mean__(self):
        pass

    def getMean(self):
        return self.__Mean__()

    def __Var__(self):
        pass

    def getVar(self):
        return self.__Var__()

    def __Skews__(self):
        pass

    def getSkews(self):
        return self.__Skews__()

    def __Kurt__(self):
        pass

    def getKurt(self):
        return self.__Kurt__()


class StatisticsModel(StatisticsBasic):
    '''
    consider GARCH/ARCH model
    functinality:
    1. confirm the coefficiency
    2. fit
    3. prediction
    '''
    def __init__(self):
        pass

class DataConstruct(object):
    '''
    construct all kinds of array
    return the assembled array
    '''
    def __init__(self):
        pass


