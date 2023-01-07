#!/usr/bin/env python
# @desc : todo 将ODS层表的数据导入到DWD层
__coding__ = "utf-8"
__author__ = "alex"

import logging
from auto_create_hive_table.com.alex.datatohive import CreateMetaCommon
from auto_create_hive_table.com.alex.utils import OracleMetaUtil



def loadTable(orclConn, hiveConn, tableName, partitionValue):
    """
    加载ODS层表的数据到DWD层
    :param orclConn: Oracle连接对象
    :param hiveConn: Hive连接对象
    :param tableName: 表名
    :param partitionValue: 分区值
    :return: None
    """
    tableMeta = OracleMetaUtil.getTableMeta(orclConn, tableName.upper())
    buffer = [
        "insert overwrite table " + CreateMetaCommon.DWD_NAME + "." + tableMeta.tableName + " partition(dt=" + partitionValue + ")\n",
        "select\n"]
    # 拼接所有列名
    allColumns = ', '.join(comame for comame in tableMeta.getColumnNameList())
    buffer.append(allColumns + "\n")
    buffer.append("from " + CreateMetaCommon.ODS_NAME + "." + tableMeta.tableName + "\n")
    buffer.append("where dt='" + partitionValue + "'")
    logging.warning(f'SparkSql插入数据，sql\n{"".join(buffer).lower()}')
    # 将整个SQL语句转换为小写
    loadSQL = ''.join(buffer).lower()
    # 获取Hive连接的一个游标
    cursor = hiveConn.cursor()
    # 执行SQL语句，加载数据
    cursor.execute(loadSQL)
