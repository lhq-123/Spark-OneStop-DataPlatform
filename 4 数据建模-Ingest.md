[TOC]



# Ingest

## **1.数据平台机构**

![Snipaste_2023-01-02_12-35-47](assets/Snipaste_2023-01-02_12-35-47.png)

**Ingest：**

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
create external table one_make_ods_test.ciss_base_areas
comment '行政地理区域表'
PARTITIONED BY (dt string)
stored as avro
location '/data/dw/ods/one_make/full_imp/ciss4.ciss_base_areas'
TBLPROPERTIES
('avro.schema.url'='/data/dw/ods/one_make/avsc/CISS4_CISS_BASE_A
REAS.avsc');
```

2.指定解析类和加载Schema文件

```sql
create external table one_make_ods_test.ciss_base_areas
comment '行政地理区域表'
PARTITIONED BY (dt string)
ROW FORMAT SERDE
'org.apache.hadoop.hive.serde2.avro.AvroSerDe'
STORED AS INPUTFORMAT
'org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat'
OUTPUTFORMAT
'org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat'
location '/data/dw/ods/one_make/full_imp/ciss4.ciss_base_areas'
TBLPROPERTIES
('avro.schema.url'='/data/dw/ods/one_make/avsc/CISS4_CISS_BASE_
AREAS.avsc');
```

## **3.自动装载**

在数据集成时将已经采集同步成功的101张表的数据加载到SparkSQL中，现开发一个程序实现自动拼接建表并获取每张表的字段信息，然后将语句提交给Spark执行，通过这种方式将数据装载进SparkSQL中
