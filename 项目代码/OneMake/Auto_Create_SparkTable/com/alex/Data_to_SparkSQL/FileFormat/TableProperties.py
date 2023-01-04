#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Author: Alex_Liu
# Program function: 创建表的属性,python中，定义抽象类的语法，需要引入abc包，导入两个abstractmethod、ABCMeta对象
from abc import ABCMeta, abstractmethod


class TableProperties(object):
    __metaclass__ = ABCMeta

    # 获取建表格式与表配置属性
    @abstractmethod
    def getStoreFmtAndProperties(self, tableName):
        pass
