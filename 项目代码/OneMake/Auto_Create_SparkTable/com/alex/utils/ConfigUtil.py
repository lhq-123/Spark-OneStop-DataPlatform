#!\\usr\\bin\\env python
# _*_ coding: utf-8 _*_
# Author: Alex_liu
# Program function: 创建配置文件读取工具类，读取Oracle、SparkSQL连接配置信息等
import configparser

# 加载配置文件
config = configparser.ConfigParser()
config.read('C:\\Users\\admin\\Desktop\\Spark工业一站式项目\\Spark-OneStop-DataPlatform\\项目代码\\OneMake\\Auto_Create_SparkTable'
            '\\resource\\config.txt')


# 根据Key获得value
def getProperty(section, key):
    return config.get(section, key)


# 根据Key获得Oracle的参数
def getOracleConfig(key):
    return config.get('OracleConn', key)


# 根据Key获得SparkSQL的参数
def getSparkConfig(key):
    return config.get('SparkConnHive', key)


def getHiveConfig(key):
    return config.get('HiveConn', key)


def getAvroConfig(key):
    return config.get('AvroProp', key)
