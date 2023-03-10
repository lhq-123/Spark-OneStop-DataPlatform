#!/usr/bin/env python
# @desc : todo 加载并读取数据库连接信息工具类
__coding__ = "utf-8"
__author__ = "alex"

import configparser

# load and read config.ini
config = configparser.ConfigParser()
config.read('C:\\Users\\admin\\Desktop\\Spark一站式历史数据平台\\Spark-OneStop-DataPlatform\\项目代码\\CISS_OneMake\\auto_create_spark_table\\resources\\config.txt')


# 根据key获得value
def getProperty(section, key):
    return config.get(section, key)


# 根据key获得oracle数据库连接的配置信息
def getOracleConfig(key):
    return config.get('OracleConn', key)


# 根据key获得spark连接hive数据库的配置信息
def getSparkConnHiveConfig(key):
    return config.get('SparkConnHive', key)
