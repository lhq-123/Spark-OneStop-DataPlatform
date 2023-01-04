#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Author: Alex_Liu
# Program function: 获取全量表和增量表

def getTableNameList(fileNameList):
    # 初始化全量表集合
    fullTableList = []
    # 初始化增量表集合
    incrTableList = []
    resultList = []
    # 初始化布尔变量
    isFull = True
    for line in fileNameList:
        if isFull:
            if "@".__eq__(line):
                isFull = False
                continue
            fullTableList.append(line)
        else:
            incrTableList.append(line)
    resultList.append(fullTableList)
    resultList.append(incrTableList)
    # 返回二维数组，包含全量和增量表名
    return resultList