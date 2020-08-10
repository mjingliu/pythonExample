#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
whole process:
1. 选择数据，用以确定样本内数据，样本外数据
   样本内数据用来确定使用什么样子的模型
   样本为数据用来检验 “通过样本内数据得到的模型” 的精度
2. 选择基础模型，这里使用GARCH(1,1)为基础
3. 根据模型，估计参数
4. 检验当前模型是否合适，也就是说估计误差最小，以及对应的分布假设合理性，
    如果不合理，则根据检测指标，重新调整模型
5. 对获取到的模型，进行样本外数据预测，并且对该数据进行精度分析，用以确定模型的准确度
6. 使用该模型进行实际预测
'''