#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Author: Alex_liu
# Program function: 添加日志功能（日志功能在接口层使用）

import logging.config

from Auto_Create_SparkTable.config import settings


# log_type:传入的日志类型(admin,company,user等)
def get_logger(log_type):
    # 1.加载日志配置信息
    logging.config.dictConfig(settings.logging_dic)
    # 2.获取日志对象
    logger = logging.getLogger(log_type)
    # 返回日志对象给调用的地方
    return logger
