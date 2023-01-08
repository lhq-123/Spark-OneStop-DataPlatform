[TOC]



# Ingest

## **1.CISS数据平台机构**

![Snipaste_2023-01-07_18-07-17](assets/Snipaste_2023-01-07_18-07-17.png)

**ODS：**

- 数据源：摄取Oracle数据，原封不动的存在HDFS上
- 数据内容：所有的增量数据，全量数据还有其他的一些数据
- 存储格式：AVRO
- 存储形式：在HDFS上以日期分区的形式存储，在Spark SQL中建表时申明分区
- 数据集成已完成，通过Sqoop将所有的增量、全量、及每张表的Schema文件上传到HDFS对应的路径上

## **2.建表语法**

Spark on Hive的常用建表语法

```sql
CREATE [TEMPORARY] [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.]table_name
(
col1Name col1Type [COMMENT col_comment],
co21Name col2Type [COMMENT col_comment],
co31Name col3Type [COMMENT col_comment],
co41Name col4Type [COMMENT col_comment],
co51Name col5Type [COMMENT col_comment],
……
coN1Name colNType [COMMENT col_comment]
)
[PARTITIONED BY (col_name data_type ...)]
[CLUSTERED BY (col_name...) [SORTED BY (col_name ...)] INTO N BUCKETS]
[ROW FORMAT row_format]
row format delimited fields terminated by
lines terminated by
[STORED AS file_format]
[LOCATION hdfs_path]
TBLPROPERTIES


EXTERNAL：外部表类型
内部表、外部表、临时表
PARTITIONED BY：分区表结构
普通表、分区表、分桶表
CLUSTERED BY：分桶表结构
ROW FORMAT：指定分隔符
列的分隔符：\001
行的分隔符：\n
STORED AS：指定文件存储类型
ODS：avro
DWD：orc
LOCATION：指定表对应的HDFS上的地址
默认：/user/hive/warehouse/dbdir/tbdir
TBLPROPERTIES：指定一些表的额外的一些特殊配置属性
```

AVRO建表语法

1.指定类型和加载Schema文件

```sql
create external table one_make_ods_ingest.ciss_base_areas
comment '行政地理区域表'
PARTITIONED BY (dt string)
stored as avro
location 'hdfs://hadoop.bigdata.cn:9000//data/dw/ods/one_make/full_imp/ciss4.ciss_base_areas'
TBLPROPERTIES
('avro.schema.url'='hdfs://hadoop.bigdata.cn:9000//data/dw/ods/one_make/avsc/CISS4_CISS_BASE_A
REAS.avsc');
```

2.指定解析类和加载Schema文件

```sql
create external table one_make_ingest.ciss_base_areas
comment '行政地理区域表'
PARTITIONED BY (dt string)
ROW FORMAT SERDE
'org.apache.hadoop.hive.serde2.avro.AvroSerDe'
STORED AS INPUTFORMAT
'org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat'
OUTPUTFORMAT
'org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat'
location 'hdfs://hadoop.bigdata.cn:9000/data/dw/ods/one_make/full_imp/ciss4.ciss_base_areas'
TBLPROPERTIES
('avro.schema.url'='hdfs://hadoop.bigdata.cn:9000/data/dw/ods/one_make/avsc/CISS4_CISS_BASE_AREAS.avsc');
```

## **3.自动装载**

在数据集成时将已经采集同步成功的101张表的数据加载到SparkSQL中，现开发一个程序实现自动拼接建表并获取每张表的字段信息，然后将语句提交给Spark执行，通过这种方式将数据装载进SparkSQL中

### **开发环境**

先安装开发时所依赖的第三方库：

```shell
# 安装sasl包(在whl文件所在目录下执行安装)，whl文件在OneMake同级的Pip目录下，不是python3.7就自行去网上下载对应版本
pip install sasl-0.2.1-cp37-cp37m-win_amd64.whl
# 安装thrift包
pip install thrift
# 安装thrift sasl包
pip install thrift-sasl
# 安装python操作oracle包
pip install cx-Oracle
# 安装python操作hive包，也可以操作sparksql
pip install pyhive
```

**sasl包注意跟python版本对应**

检测是否安装成功：

![Snipaste_2023-01-05_19-10-53](assets/Snipaste_2023-01-05_19-10-53.png)

代码：

Spark-OneStop-DataPlatform\项目代码\OneMake\Auto_Create_SparkTable包下的代码

代码模块功能：

```mathematica
  ├─Auto_Create_SparkTable                        
      ├─com
      │  ├─alex
      │     │  MainApplication.py                  # 程序运行入口，核心调度运行的程序
      │     ├─bean
      │     │  │  ColumnMeta.py                    # Oracle列的信息对象：用于将列的名称、类型、注释进行封装
      │     │  │  TableMeta.py                     # Oracle表的信息对象：用于将表的名称、列的信息、表的注释进行封装
      │     ├─Data_to_SparkSQL                     # 模块名
      │     │  │  CreateMetaCommon.py              # 定义了建表时固定的一些字符串数据，数据库名称、分层名称、文件类型属性等
      │     │  │  CreateSparkTableFromOracle.py    # 自动创建SparkSQL数据库、以及获取Oracle表的信息创建SparkSQL表等
      │     │  │  CreateSparkTablePartition.py     # 定义了建表时固定的一些字符串数据，数据库名称、分层名称、文件类型属性等
      │     │  │  LoadIngDataToSeg.py              # 用于实现将Ingest的数据insert到Segmentation表中
      │     │  ├─FileFormat                        # 处理各种文件格式的脚本的包名
      │     │     │  AvroTableProperties.py        # Avro文件格式对象，用于封装Avro建表时的字符串
      │     │     │  OrcSnappyTableProperties.py   # Orc文件格式对象，用于封装Orc建表时的字符串
      │     │     │  OrcTableProperties.py         # Orc文件格式加Snappy压缩的对象
      │     │     │  TableProperties.py            # 用于获取表的属性的类
      │     ├─utils                                # 程序中使用到的工具类的包名
      │        │  ConfigUtil.py                    # 用于加载配置文件，获取配置文件信息
      │        │  ConnectUtil.py                   # 用于获取Oracle连接、SparkSQL连接
      │        │  OracleMetaUtil.py                # 用于获取Oracle中表的信息：表名、字段名、类型、注释等
      │        │  ReadFileUtil.py                  # 用于读写文件，获取所有Oracle表的名称
      │        │  TableNameUtil.py                 # 用于将全量表和增量表的名称放入不同的列表中
      ├─config                                     # 配置日志的脚本的包名
      │  │  common.py                              # 用于获取日志的类
      │  │  settings.py                            # 用于配置日志记录方式的类
      ├─logs                                       # 日志存放位置
      │      one_make.log                          # 日志文件
      ├─resource                                   # 配置文件
      │      config.txt                            # Oracle、SparkSQL的地址、端口、用户名、密码等配置信息
```

### **测试**

#### **ODS测试**

测试读取所有表清单：

代码不用全部运行，后面一部分注释掉，一部分一部分运行测试

![Snipaste_2023-01-07_21-31-05](assets/Snipaste_2023-01-07_21-31-05.png)

测试创建ODS库：

![Snipaste_2023-01-07_21-46-42](assets/Snipaste_2023-01-07_21-46-42.png)

在spark容器里通过beeline进入spaarksql查看(保证SparkthriftServer正常启动着)

![Snipaste_2023-01-07_21-50-31](assets/Snipaste_2023-01-07_21-50-31.png)

如果没有这个sparksubmit的话就开启开启STS：

```shell
# 在spark/sbin目录下执行
./start-thriftserver.sh \
--name sparksql-thrift-server \
--master yarn \
--deploy-mode client \
--driver-memory 1g \
--hiveconf hive.server2.thrift.http.port=10001 \
--num-executors 3 \
--executor-memory 1g \
--conf spark.sql.shuffle.partitions=2
```

通过Beeline连接SparkThriftServer：

```shell
# beeline !connect jdbc:hive2://spark.bigdata.cn:10001
[root@c5836fa7593c conf] beeline
Beeline version 1.2.1.spark2 by Apache Hive
beeline> !connect jdbc:hive2://spark.bigdata.cn:10001
Connecting to jdbc:hive2://spark.bigdata.cn:10001
Enter username for jdbc:hive2://spark.bigdata.cn:10001: root
Enter password for jdbc:hive2://spark.bigdata.cn:10001: 123456
20/12/11 07:20:04 INFO jdbc.Utils: Supplied authorities: spark.bigdata.cn:10001
20/12/11 07:20:04 INFO jdbc.Utils: Resolved authority: spark.bigdata.cn:10001
20/12/11 07:20:04 INFO jdbc.HiveConnection: Will try to open client transport with JDBC Uri: jdbc:hive2://spark.bigdata.cn:10001
Connected to: Spark SQL (version 2.4.7)
Driver: Hive JDBC (version 1.2.1.spark2)
Transaction isolation: TRANSACTION_REPEATABLE_READ
0: jdbc:hive2://spark.bigdata.cn:10001> show databases;
```

ODS建库成功：

![Snipaste_2023-01-07_21-46-27](assets/Snipaste_2023-01-07_21-46-27.png)

测试ODS建表(增量加全量一共101张)：

![Snipaste_2023-01-07_22-04-13](assets/Snipaste_2023-01-07_22-04-13.png)

ODS层建表完成后可以在beeline中随便查看一张表看是否有数据：

![Snipaste_2023-01-07_22-23-34](assets/Snipaste_2023-01-07_22-23-34.png)

如果没有数据的话，可以去看一下日志：

使用了异常，如果有错误的话，会把白色的日志打印到控制台：

![Snipaste_2023-01-08_01-23-59](assets/Snipaste_2023-01-08_01-23-59.png)

```shell
org.apache.spark.sql.AnalysisException: org.apache.hadoop.hive.ql.metadata.HiveException: Unable to move source hdfs:// to destination hdfs://
```

这是我在重跑的时候出现的，因为我配置的是Spark on hive ，所以使用的是hive的catalog，一开始没配置，后面我在spark容器的spark/conf/hive-site.xml里加上下面的配置然后重启spark容器再重跑就没问题了

```xml
<property>
      <name>metastore.catalog.default</name>
      <value>hive</value>
</property>
```

