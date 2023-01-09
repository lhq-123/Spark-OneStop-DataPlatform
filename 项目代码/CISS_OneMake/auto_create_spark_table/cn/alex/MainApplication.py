#!/usr/bin/env python
# @desc : todo ODS&DWD建库、建表、装载数据主类
__coding__ = "utf-8"
__author__ = "alex"

# 导入读Oracle表、建Hive表的包
from auto_create_spark_table.cn.alex.datatospark import CreateSparkTableFromOracle, CreateMetaCommon, CreateSparkTablePartition, LoadDataToDWD
# 导入工具类：连接Oracle工具类、文件工具类、表名构建工具类
from auto_create_spark_table.cn.alex.utils import ConnectUtil, ReadFileUtil, TableNameUtil
# 导入日志工具包
from auto_create_spark_table.config import common

# 根据不同功能接口记录不同的日志
admin_logger = common.get_logger('alex')


def recordLog(modelName):
    msg = f'{modelName}'
    admin_logger.info(msg)
    return msg


def recordErrorLog(msg):
    admin_logger.warning(msg)
    return msg


if __name__ == '__main__':

    recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>构建历史数据平台的ODS层和DWD层并加载数据<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    partitionVal = '20210101'
    oracleConn = ConnectUtil.getOracleConn()
    hiveConn = ConnectUtil.getSparkHiveConn()
    tableList = ReadFileUtil.readFileContent("C:\\Users\\admin\\Desktop\\Spark一站式历史数据平台\\Spark-OneStop-DataPlatform\\项目代码\\CISS_OneMake\\auto_create_spark_table\\resources\\tablenames.txt")
    tableNameList = TableNameUtil.getODSTableNameList(tableList)
    # ------------------测试：输出获取到的连接以及所有表名
    print(oracleConn)
    print(hiveConn)
    for tables in tableNameList:
        print("---------------------")
        for name in tables:
            print(name)
    try:
        createSparkTableFromOracle = CreateSparkTableFromOracle(oracleConn, hiveConn)
        recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>ODS层创建数据库<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        createSparkTableFromOracle.executeCreateDbHQL(CreateMetaCommon.ODS_NAME)
        recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>ODS层全量表入库<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        fullTableList = tableNameList[0]
        for tblName in fullTableList:
            createSparkTableFromOracle.executeCreateTableHQL(CreateMetaCommon.ODS_NAME, tblName, CreateMetaCommon.FULL_IMP)
        recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>ODS层增量表入库<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        incrTableList = tableNameList[1]
        for tblName in incrTableList:
            # Hive中创建这张增量表：数据库名称、表名、表的类型
            createSparkTableFromOracle.executeCreateTableHQL(CreateMetaCommon.ODS_NAME, tblName, CreateMetaCommon.INCR_IMP)
        recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>声明ODS层全量表分区<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        createHiveTablePartition = CreateSparkTablePartition(hiveConn)
        # 全量表执行44次创建分区操作
        for tblName in fullTableList:
            createHiveTablePartition.executeCPartition(CreateMetaCommon.ODS_NAME, tblName, CreateMetaCommon.FULL_IMP, partitionVal)
        recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>声明ODS层增量表分区<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        # 增量表执行57次创建分区操作
        for tblName in incrTableList:
            createHiveTablePartition.executeCPartition(CreateMetaCommon.ODS_NAME, tblName, CreateMetaCommon.INCR_IMP, partitionVal)
        recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>DWD层创建数据库<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        createSparkTableFromOracle.executeCreateDbHQL(CreateMetaCommon.DWD_NAME)
        recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>DWD层表入库<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        allTableName = [i for j in tableNameList for i in j]
        for tblName in allTableName:
            createSparkTableFromOracle.executeCreateTableHQL(CreateMetaCommon.DWD_NAME, tblName, None)
        recordLog('>>>>>>>>>>>>>>>>>>>>>>>>DWD层数据入库，此操作将启动Spark JOB执行，请稍后<<<<<<<<<<<<<<<<<<<<<<<<<<')
        for tblName in allTableName:
            recordLog(f'>>>>>>>>>>>>>>>>>>>>ODS层数据已经加载到DWD层的{tblName}表<<<<<<<<<<<<<<<<<<<<<')
            LoadDataToDWD.loadTable(oracleConn, hiveConn, tblName, partitionVal)
    except Exception as e:
        recordErrorLog(f'构建发生了异常>>>>>>>>>{e}')
        exit(1)
    recordLog('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>完成ODS层跟DWD层的构建<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    oracleConn.close()
    hiveConn.close()
