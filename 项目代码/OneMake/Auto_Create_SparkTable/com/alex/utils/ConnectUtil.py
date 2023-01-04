#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Author: Alex_Liu
# Program function: 创建Oracle和SparkSQL连接工具类
import os

import cx_Oracle
from pyhive import hive
from Auto_Create_SparkTable.com.alex.utils import ConfigUtil

LOCATION = r"D:\pythonOracle\instantclient_12_2"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]

def getOracleConn():
    oracleConn = None
    try:
        ORACLE_HOST = ConfigLoader.getOracleConfig('oracleHost')
        ORACLE_PORT = ConfigLoader.getOracleConfig('oraclePort')
        ORACLE_SID = ConfigLoader.getOracleConfig('oracleSID')
        ORACLE_USER = ConfigLoader.getOracleConfig('oracleUName')
        ORACLE_PASSWORD = ConfigLoader.getOracleConfig('oraclePassWord')
        # 获得oracle连接 用户名/密码@IP:端口号/SERVICE_NAME
        # oracleConn = cx_Oracle.connect(f'{ORACLE_USER}/{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SID}')
        # dsn:data source name
        dsn = cx_Oracle.makedsn(ORACLE_HOST, ORACLE_PORT, ORACLE_SID)
        oracleConn = cx_Oracle.connect(ORACLE_USER, ORACLE_PASSWORD, dsn)
        print(cursor.fetchall())
    except cx_Oracle.Error as error:
        print(error)
    return oracleConn

def getSparkHiveConn():
    sparkHiveConn = None
    try:
        SPARK_HIVE_HOST = ConfigLoader.getSparkConnHiveConfig('sparkHiveHost')
        SPARK_HIVE_PORT = ConfigLoader.getSparkConnHiveConfig('sparkHivePort')
        SPARK_HIVE_UNAME = ConfigLoader.getSparkConnHiveConfig('sparkHiveUName')
        SPARK_HIVE_PASSWORD = ConfigLoader.getSparkConnHiveConfig('sparkHivePassWord')
        sparkHiveConn = hive.Connection(host=SPARK_HIVE_HOST, port=SPARK_HIVE_PORT, username=SPARK_HIVE_UNAME, auth='CUSTOM', password=SPARK_HIVE_PASSWORD)
    except Exception as error:
        print(error)
    # finally:
    #     if sparkHiveConn:
    #         sparkHiveConn.close()
    return sparkHiveConn
