#!/usr/bin/env python
# @desc : todo 实现读取表名文件
__coding__ = "utf-8"
__author__ = "alex"


# 加载表名所在的文件
def readFileContent(fileName):
    tableNameList = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.rstrip('\n')
        tableNameList.append(curLine)
    return tableNameList
