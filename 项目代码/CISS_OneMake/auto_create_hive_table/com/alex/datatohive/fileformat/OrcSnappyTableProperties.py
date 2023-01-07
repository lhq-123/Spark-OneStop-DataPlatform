#!/usr/bin/env python
# @desc : hdfs存储数据为orc格式并设置snappy压缩
__coding__ = "utf-8"
__author__ = "alex"

from auto_create_hive_table.com.alex.datatohive.fileformat.OrcTableProperties import OrcTableProperties


class OrcSnappyTableProperties(OrcTableProperties):
    def getStoreFmtAndProperties(self, tableName):
        return super(OrcSnappyTableProperties, self).getStoreFmtAndProperties(
            tableName) + "tblproperties (\"orc.compress\"=\"SNAPPY\")\n"
