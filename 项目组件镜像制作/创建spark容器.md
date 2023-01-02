#创建spark容器

## 上传并解压spark压缩包

- 上传压缩包

  - spark-2.4.7-bin-hadoop2.7.tgz

- 解压压缩包

  `tar -xvzf spark-2.4.7-bin-hadoop2.7.tgz -C /opt/`

## 配置Spark HistoryServer

```shell
cd /opt/spark-2.4.7-bin-hadoop2.7/conf
cp spark-defaults.conf.template spark-defaults.conf
```

```shell
# spark-defaults.conf
vim spark-defaults.conf
spark.eventLog.enabled     true
spark.eventLog.dir     hdfs://hadoop.bigdata.cn:9000/tmp/spark-history
```

## 设置默认读取HDFS

```shell
cd /opt/spark-2.4.7-bin-hadoop2.7/conf
cp spark-env.sh.template spark-env.sh
```

```shell
# vim spark-env.sh
export JAVA_HOME=/opt/jdk1.8.0_141/
export SPARK_HOME=/opt/spark-2.4.7-bin-hadoop2.7
export SPARK_MASTER_IP=spark.bigdata.cn
export SPARK_EXECUTOR_MEMORY=2G
export HADOOP_CONF_DIR=/opt/hadoop-2.7.0/etc/hadoop
export SPARK_HISTORY_OPTS="-Dspark.history.ui.port=18080 -Dspark.history.retainedApplications=200 -Dspark.history.fs.logDirectory=hdfs://hadoop.bigdata.cn:9000/tmp/spark-history"
```

## 配置集群节点

```shell
cp slaves.template slaves
vim slaves
spark.bigdata.cn
```

## 创建Spark容器

- 创建spark容器，指定IP

  ```shell
  docker run \
  --privileged=true \
  --net docker-bd0 \
  --ip 172.33.0.133 \
  -v /mnt/docker_share:/mnt/docker_share \
  -v /etc/hosts:/etc/hosts \
  -v /opt/hadoop-2.7.0:/opt/hadoop-2.7.0 \
  -v /opt/jdk1.8.0_141:/opt/jdk1.8.0_141 \
  -v /opt/apache-hive-2.1.0-bin:/opt/apache-hive-2.1.0-bin \
  -v /opt/spark-2.4.7-bin-hadoop2.7:/opt/spark-2.4.7-bin-hadoop2.7 \
  -p 18080:18080 -p 8080:8080 -p 7077:7077 -p 4040:4040 -p 10001:10001 \
  --name spark -d hadoop:2.7.0
  ```

## 容器配置环境变量

- 进入容器中

  `docker exec -it spark bash`

- 配置环境变量

  ```shell
  vim /etc/profile
  
  export HIVE_HOME=/opt/apache-hive-2.1.0-bin
  export PATH=$HIVE_HOME/bin:$PATH
  
  export SPARK_HOME=/opt/spark-2.4.7-bin-hadoop2.7
  export PATH=${SPARK_HOME}/bin:${SPARK_HOME}/sbin:$PATH
  
  source /etc/profile
  ```

## 启动spark

- 创建spark history目录

  ```shell
  
  hadoop fs -mkdir -p /tmp/spark-history
  start-all.sh
  start-history-server.sh
  ```

## 查看spark web ui 

- Spark Web UI：
  - http://192.168.10.100:8080/
- Spark HistoryServer：
  - http://192.168.10.100:18080/