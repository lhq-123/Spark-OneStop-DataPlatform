#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Author: Alex_Liu
# Program function: 读取表清单文件，每行一个表名，全量表和增量表用@隔开

def readFileContent(fileName):
    # 加载数据
    tableNameList = []
    # 读取文件
    file = open(fileName)
    for line in file.readlines():
        # 替换读取每一行文件的默认字符：'\n'
        curLine = line.rstrip('\n')
        tableNameList.append(curLine)
    return tableNameList

