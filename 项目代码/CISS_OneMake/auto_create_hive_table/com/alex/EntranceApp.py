#!/usr/bin/env python
# @desc : TODO ODS&DWD建库、建表、装载数据主类
__coding__ = "utf-8"
__author__ = "alex"

# 导入读Oracle表、建Hive表的包
import logging
from auto_create_hive_table.com.alex.datatohive import CHiveTableFromOracleTable, CreateMetaCommon, CreateHiveTablePartition, LoadData2DWD
# 导入工具类：连接Oracle工具类、文件工具类、表名构建工具类
from auto_create_hive_table.com.alex.utils import OracleHiveUtil, FileUtil, TableNameUtil
# 导入日志工具包
from auto_create_hive_table.com.config import common
# 根据不同功能接口记录不同的日志
admin_logger = common.get_logger('alex')


def recordLog(modelName):
    """
    记录普通级别日志
    :param modelName: 模块名称
    :return: 日志信息
    """
    msg = f'{modelName}'
    admin_logger.info(msg)
    return msg


def recordWarnLog(msg):
    """
    记录警告级别日志
    :param msg: 日志信息
    :return: 日志信息
    """
    admin_logger.warning(msg)
    return msg


if __name__ == '__main__':

    # 输出信息
    recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>开始构建一站式历史数据平台的ODS层跟DWD层<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    partitionVal = '20210101'
    oracleConn = OracleHiveUtil.getOracleConn()
    sparkSQLConn = OracleHiveUtil.getSparkHiveConn()
    # 根据自己电脑的位置改
    tableList = FileUtil.readFileContent("C:\\Users\\admin\\Desktop\\Spark工业一站式项目\\Spark-OneStop-DataPlatform\\项目代码\\CISS_OneMake\\auto_create_hive_table\\com\\resources\\tablenames.txt")
    tableNameList = TableNameUtil.getODSTableNameList(tableList)
    # 测试：输出获取到的连接以及所有表名
    # print(oracleConn)
    # print(sparkSQLConn)
    # for tables in tableNameList:
    #     print("---------------------")
    #     for name in tables:
    #         print(name)
    cHiveTableFromOracleTable = CHiveTableFromOracleTable(oracleConn, sparkSQLConn)
    recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>创建ODS层对应的库<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    try:
        cHiveTableFromOracleTable.executeCreateDbHQL(CreateMetaCommon.ODS_NAME)
        recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>创建ODS层对应的全量表<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    except Exception as error:
        logging.error(error)
    fullTableList = tableNameList[0]
    for tblName in fullTableList:
        try:
            cHiveTableFromOracleTable.executeCreateTableHQL(CreateMetaCommon.ODS_NAME, tblName, CreateMetaCommon.FULL_IMP)
        except Exception as error:
            logging.error(error)
    recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>创建ODS层对应的增量表<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    incrTableList = tableNameList[1]
    for tblName in incrTableList:
        # SparkSQL中创建这张增量表：数据库名称、表名、表的类型
        try:
            cHiveTableFromOracleTable.executeCreateTableHQL(CreateMetaCommon.ODS_NAME, tblName, CreateMetaCommon.INCR_IMP)
        except Exception as error:
            logging.error(error)
    recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>声明ODS层对应的增量表的分区<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    createHiveTablePartition = CreateHiveTablePartition(sparkSQLConn)
    # 全量表执行44次创建分区操作
    for tblName in fullTableList:
        try:
            createHiveTablePartition.executeCPartition(CreateMetaCommon.ODS_NAME, tblName, CreateMetaCommon.FULL_IMP, partitionVal)
        except Exception as error:
            logging.error(error)
    recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>声明ODS层对应的全量表的分区<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    # 增量表执行57次创建分区操作
    for tblName in incrTableList:
        try:
            createHiveTablePartition.executeCPartition(CreateMetaCommon.ODS_NAME, tblName, CreateMetaCommon.INCR_IMP, partitionVal)
        except Exception as error:
            logging.error(error)
    recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>创建DWD层对应的库<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    cHiveTableFromOracleTable.executeCreateDbHQL(CreateMetaCommon.DWD_NAME)
    recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>创建DWD层对应的表<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    allTableName = [i for j in tableNameList for i in j]
    for tblName in allTableName:
        try:
            cHiveTableFromOracleTable.executeCreateTableHQL(CreateMetaCommon.DWD_NAME, tblName, None)
        except Exception as error:
            logging.error(error)
    recordWarnLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>DWD层加载数据，此操作将启动Spark JOB执行，请稍后<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    for tblName in allTableName:
        recordLog(f'>>>>>>>>>>>>>>>>>>>>>>>>>>加载ODS层数据到DWD层对应的{tblName}表<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        try:
            LoadData2DWD.loadTable(oracleConn, sparkSQLConn, tblName, partitionVal)
        except Exception as error:
            logging.error(error)
        recordLog(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>DWD层的{tblName}表数据加载完成<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>一站式历史数据平台的ODS跟DWD层构建完成！！！！！！<<<<<<<<<<<<<<<<<<<<<<<<<')
    # 关闭连接，释放资源
    oracleConn.close()
    sparkSQLConn.close()
