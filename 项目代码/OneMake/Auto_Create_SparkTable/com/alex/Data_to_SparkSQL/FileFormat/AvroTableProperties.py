#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Author: Alex_Liu
# Program function: 从Oracle抽取到HDFS的数据为Avro格式的，包括Avro格式数据的
#                   Schema信息也抽取到了HDFS，如果想在SparkSQL中实现自动创表，
#                   得先获取Avro数据的Schema信息，先获取Schema文件的信息
from Auto_Create_SparkTable.com.alex.Data_to_SparkSQL.FileFormat.TableProperties import TableProperties
from Auto_Create_SparkTable.com.alex.utils import ConfigUtil

class AvroTableProperties(TableProperties):
    #  Avro schema Folder存放位置
    # AVSC_FOLDER = "hdfs:///data/dw/ods/one_make/avsc/"
    AVSC_FOLDER = ConfigUtil.getAvroConfig('folder')

    #  AVSC schema文件前缀
    # AVSC_FILE_PREFIX = "CISS4_"
    AVSC_FILE_PREFIX = ConfigUtil.getAvroConfig('file_prefix')

    # 拼接AVRO建表语法的拓展部分
    def getStoreFmtAndProperties(self, tableName):
        return "ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.avro.AvroSerDe'\n" + \
               "STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat'\n" + \
               " OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat'\n" + \
               "tblproperties ('avro.schema.url'='" + \
               self.AVSC_FOLDER + self.AVSC_FILE_PREFIX + tableName.upper() + ".avsc')\n"
