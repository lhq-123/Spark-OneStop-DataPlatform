#!/usr/bin/env python
# @desc : hdfs存储数据为orc格式
__coding__ = "utf-8"
__author__ = "alex"

from auto_create_hive_table.com.alex.datatohive.fileformat.TableProperties import TableProperties


class OrcTableProperties(TableProperties):
    def getStoreFmtAndProperties(self, tableName):
        return "stored as orc\n"
