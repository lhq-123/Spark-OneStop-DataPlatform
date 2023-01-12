#!/usr/bin/env python
# @desc : todo 实现构建Oracle、Hive、SparkSQL的连接
__coding__ = "utf-8"
__author__ = "alex"

# 导包
from auto_create_spark_table.cn.alex.utils import ConfigUtil  # 导入配置文件解析包
import cx_Oracle  # 导入Python连接Oracle依赖库包
from pyhive import hive  # 导入Python连接Hive依赖包
import os  # 导入系统包

# 配置Oracle的客户端驱动文件路径
LOCATION = r"D:\\instantclient_12_2"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]


# 用户获取Oracle的连接对象：cx_Oracle.connect(host='', port='', username='', password='', param='')
def getOracleConn():
    oracleConn = None  # 构建Oracle连接对象
    try:
        ORACLE_HOST = ConfigUtil.getOracleConfig('oracleHost')
        ORACLE_PORT = ConfigUtil.getOracleConfig('oraclePort')
        ORACLE_SID = ConfigUtil.getOracleConfig('oracleSID')
        ORACLE_USER = ConfigUtil.getOracleConfig('oracleUName')
        ORACLE_PASSWORD = ConfigUtil.getOracleConfig('oraclePassWord')
        dsn = cx_Oracle.makedsn(ORACLE_HOST, ORACLE_PORT, ORACLE_SID)
        oracleConn = cx_Oracle.connect(ORACLE_USER, ORACLE_PASSWORD, dsn)
    # 异常处理
    except cx_Oracle.Error as error:
        print(error)
    return oracleConn


#  用户获取SparkSQL的连接对象
def getSparkHiveConn():
    sparkHiveConn = None
    try:
        SPARK_HIVE_HOST = ConfigUtil.getSparkConnHiveConfig('sparkHiveHost')
        SPARK_HIVE_PORT = ConfigUtil.getSparkConnHiveConfig('sparkHivePort')
        SPARK_HIVE_UNAME = ConfigUtil.getSparkConnHiveConfig('sparkHiveUName')
        SPARK_HIVE_PASSWORD = ConfigUtil.getSparkConnHiveConfig('sparkHivePassWord')
        sparkHiveConn = hive.Connection(host=SPARK_HIVE_HOST, port=SPARK_HIVE_PORT, username=SPARK_HIVE_UNAME,
                                        auth='CUSTOM', password=SPARK_HIVE_PASSWORD)
    # 异常处理
    except Exception as error:
        print(error)
    return sparkHiveConn
