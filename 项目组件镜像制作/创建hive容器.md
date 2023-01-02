# 创建Hive容器

## 宿主机上传hive安装包并解压

- 进入/mnt/docker_share目录，上传apache-hive-2.1.0-bin.tar.gz到此目录下

- 解压到opt目录下

  `tar -xvzf apache-hive-2.1.0-bin.tar.gz -C /opt/`

## 修改hive配置文件

```shell
cd /opt/apache-hive-2.1.0-bin/conf
touch hive-site.xml
vim hive-site.xml
```

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>hive.metastore.warehouse.dir</name>
        <value>/user/hive/warehouse</value>
    </property>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://hadoop.bigdata.cn:9000</value>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionUserName</name>
        <value>root</value>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionPassword</name>
        <value>123456</value>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionURL</name>
        <value>jdbc:mysql://mysql.bigdata.cn:3306/hive?createDatabaseIfNotExist=true&amp;useSSL=false&amp;characterEncoding=UTF-8</value>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionDriverName</name>
        <value>com.mysql.jdbc.Driver</value>
    </property>
    <property>
        <name>hive.metastore.schema.verification</name>
        <value>false</value>
    </property>
    <property>
        <name>datanucleus.schema.autoCreateAll</name>
        <value>true</value>
    </property>
    <property>
        <name>hive.server2.thrift.bind.host</name>
        <value>hive.bigdata.cn</value>
    </property>
    <property>
        <name>hive.metastore.uris</name>
        <value>thrift://hive.bigdata.cn:9083</value>
    </property>
</configuration>
```

## 上传配置mysql驱动

- 上传mysql jdbc驱动到宿主机/mnt/docker_share

  - mysql-connector-java-5.1.38-bin.jar

- 复制mysql的驱动程序到hive/lib下面

  ```shell
  cp /mnt/docker_share/mysql-connector-java-5.1.38-bin.jar /opt/apache-hive-2.1.0-bin/lib
  ll /opt/apache-hive-2.1.0-bin/lib | grep mysql
  ```

## 启动mysql和hadoop容器

- 启动mysql容器

  `docker start mysql`

- 启动hadoop容器

  `docker start hadoop`

## 创建hive容器

- 创建hive容器，指定IP（注意一定要添加 --privileged=true否则无法使用系统服务）

  ```shell
  docker run \
  --privileged=true \
  --net docker-bd0 \
  --ip 172.33.0.131 \
  -v /mnt/docker_share:/mnt/docker_share \
  -v /etc/hosts:/etc/hosts \
  -v /opt/hadoop-2.7.0:/opt/hadoop-2.7.0 \
  -v /opt/jdk1.8.0_141:/opt/jdk1.8.0_141 \
  -v /opt/apache-hive-2.1.0-bin:/opt/apache-hive-2.1.0-bin \
  -p 10000:10000 \
  --name hive -d hadoop:2.7.0
  ```

## 进入hive容器

`docker exec -it hive bash`

## 配置hive环境变量

```shell
vim /etc/profile

export HIVE_HOME=/opt/apache-hive-2.1.0-bin
export PATH=$HIVE_HOME/bin:$PATH

source /etc/profile
```

## 初始化mysql元数据

- 初始化mysql元数据命令

  `schematool -initSchema -dbType mysql`

- 进入到mysql容器中，设置hive相关表的编码格式

  `docker exec -it mysql bash`

- 进入到mysql中，执行以下几条语句，修改Hive的默认编码方式

  `mysql -u root -p`

  ```sql
  use hive;
  -- 修改表字段注解和表注解
  alter table COLUMNS_V2 modify column COMMENT varchar(256) character set utf8;
  alter table TABLE_PARAMS modify column PARAM_VALUE varchar(4000) character set utf8;
  -- 修改分区字段注解：
  alter table PARTITION_PARAMS modify column PARAM_VALUE varchar(4000) character set utf8;
  alter table PARTITION_KEYS modify column PKEY_COMMENT varchar(4000) character set utf8;
  -- 修改索引注解：
  alter table INDEX_PARAMS modify column PARAM_VALUE varchar(4000) character set utf8;
  -- 查看编码格式
  show variables like "%char%";
  ```

## 启动hive和使用beeline连接hive

- 启动hive

  ```shell
  nohup hive --service metastore &
  nohup hive --service hiveserver2 &
  ```

- 使用beeline连接hive

  ```shell
  beeline
  !connect jdbc:hive2://hive.bigdata.cn:10000
  ```

## 配置hive自动启动

### 创建日志保存目录

`mkdir -p /opt/apache-hive-2.1.0-bin/logs`

### 创建启动脚本

```shell
vim /etc/bootstrap.sh

# !/bin/sh
source /etc/profile

DATE_STR=`/bin/date  "+%Y%m%d%H%M%S"`

HIVE_METASTORE_LOG=${HIVE_HOME}/logs/hiveserver2-metasvr-${DATE_STR}.log
HIVE_THRIFTSVR_LOG=${HIVE_HOME}/logs/hiveserver2-thriftsvr-${DATE_STR}.log

nohup ${HIVE_HOME}/bin/hive --service metastore >> ${HIVE_METASTORE_LOG} 2>&1 &
nohup ${HIVE_HOME}/bin/hive --service hiveserver2 >> ${HIVE_THRIFTSVR_LOG} 2>&1 &
```

### 设置脚本执行权限

`chmod a+x /etc/bootstrap.sh`

### 加入自动启动服务

```shell
vim /etc/rc.d/rc.local
/etc/bootstrap.sh
chmod 755 /etc/rc.d/rc.local 
```

### 重启容器

```shell
docker restart hive
docker exec -it hive bash
```

