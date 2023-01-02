#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Author: Liu
# Program function:  创建数据平台的ODS层，即从oracle中获得表结构，在SparkSQL中创建对应表。

from pyhive import hive                                                         # 导入Hive操作包
from auto_create_hive_table.cn.itcast.datatohive import CreateMetaCommon        # 导入常量数据包
from auto_create_hive_table.cn.itcast.utils import OracleMetaUtil               # 导入Oracle表信息的工具类
import logging