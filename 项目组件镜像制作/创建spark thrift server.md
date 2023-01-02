# 创建spark thrift server

## 关闭spark独立集群

`stop-all.sh`

## 拷贝hive的hive-site.xml文件，修改参数

```shell
cd /opt/spark-2.4.7-bin-hadoop2.7/conf
cp /opt/apache-hive-2.1.0-bin/conf/hive-site.xml .
```

```shell
vim hive-site.xml
# 修改第36行，thrift server地址和端口
<property>
   <name>hive.server2.thrift.port</name>
   <value>10001</value>
</property>
<property>
    <name>hive.server2.thrift.bind.host</name>
    <value>spark.bigdata.cn</value>
</property>
```

## 设置默认spark参数

- 修改spark-defaults文件，设置默认参数

  ```shell
  vim spark-defaults.conf
  # 添加以下两行
  spark.sql.warehouse.dir         hdfs://hadoop.bigdata.cn:9000/user/hive/warehouse
  spark.sql.shuffle.partitions    2
  ```

## 给spark添加mysql驱动

```shell
cd /opt/spark-2.4.7-bin-hadoop2.7/jars
cp /opt/apache-hive-2.1.0-bin/lib/mysql-connector-java-5.1.38.jar .
```

## 启动spark thrift server

- 因为我们使用的是YARN模式，所以我们得需要按照YARN的方式来配置资源申请

  ```shell
  YARN-only:
  --queue QUEUE_NAME        The YARN queue to submit to (Default: "default").
  --num-executors NUM       Number of executors to launch (Default: 2).
                            If dynamic allocation is enabled, the initial number of
                            executors will be at least NUM.
  --archives ARCHIVES       Comma separated list of archives to be extracted into the
                            working directory of each executor.
  --principal PRINCIPAL     Principal to be used to login to KDC, while running on
                            secure HDFS.
  --keytab KEYTAB           The full path to the file that contains the keytab for the
                            principal specified above. This keytab will be copied to
                            the node running the Application Master via the Secure
                            Distributed Cache, for renewing the login tickets and the
                            delegation tokens periodically.
  ```

- 启动thrift server

  ```shell
  start-thriftserver.sh \
  --name sparksql-thrift-server \
  --master yarn \
  --deploy-mode client \
  --driver-memory 1g \
  --hiveconf hive.server2.thrift.http.port=10001 \
  --num-executors 3 \
  --executor-memory 1g \
  --conf spark.sql.shuffle.partitions=2
  ```

- yarn资源页面查看（进入ThriftServer进程的AppMaster）

  - http://node1:8088/

    ![image-20210205160746423](images/image-20210205160746423.png)

  - 进入hadoop容器，查看服务进程

    ```shell
    root@cb338fa74260 hadoop]# jps -vm | grep 6017   
    6017 ExecutorLauncher --arg spark.bigdata.cn:37890 --properties-file /tmp/hadoop-root/nm-local-dir/usercache/root/appcache/application_1608087619253_0001/container_1608087619253_0001_01_000001/__spark_conf__/__spark_conf__.properties -Xmx512m -Djava.io.tmpdir=/tmp/hadoop-root/nm-local-dir/usercache/root/appcache/application_1608087619253_0001/container_1608087619253_0001_01_000001/tmp -Dspark.yarn.app.container.log.dir=/opt/hadoop-2.7.0/logs/userlogs/application_1608087619253_0001/container_1608087619253_0001_01_000001
    [root@cb338fa74260 hadoop]# jps -vm | grep CoarseGrainedExecutorBackend
    6054 CoarseGrainedExecutorBackend --driver-url spark://CoarseGrainedScheduler@spark.bigdata.cn:37890 --executor-id 1 --hostname hadoop.bigdata.cn --cores 1 --app-id application_1608087619253_0001 --user-class-path file:/tmp/hadoop-root/nm-local-dir/usercache/root/appcache/application_1608087619253_0001/container_1608087619253_0001_01_000002/__app__.jar -Xmx1024m -Djava.io.tmpdir=/tmp/hadoop-root/nm-local-dir/usercache/root/appcache/application_1608087619253_0001/container_1608087619253_0001_01_000002/tmp -Dspark.driver.port=37890 -Dspark.yarn.app.container.log.dir=/opt/hadoop-2.7.0/logs/userlogs/application_1608087619253_0001/container_1608087619253_0001_01_000002 -XX:OnOutOfMemoryError=kill %p
    6102 CoarseGrainedExecutorBackend --driver-url spark://CoarseGrainedScheduler@spark.bigdata.cn:37890 --executor-id 3 --hostname hadoop.bigdata.cn --cores 1 --app-id application_1608087619253_0001 --user-class-path file:/tmp/hadoop-root/nm-local-dir/usercache/root/appcache/application_1608087619253_0001/container_1608087619253_0001_01_000004/__app__.jar -Xmx1024m -Djava.io.tmpdir=/tmp/hadoop-root/nm-local-dir/usercache/root/appcache/application_1608087619253_0001/container_1608087619253_0001_01_000004/tmp -Dspark.driver.port=37890 -Dspark.yarn.app.container.log.dir=/opt/hadoop-2.7.0/logs/userlogs/application_1608087619253_0001/container_1608087619253_0001_01_000004 -XX:OnOutOfMemoryError=kill %p
    6079 CoarseGrainedExecutorBackend --driver-url spark://CoarseGrainedScheduler@spark.bigdata.cn:37890 --executor-id 2 --hostname hadoop.bigdata.cn --cores 1 --app-id application_1608087619253_0001 --user-class-path file:/tmp/hadoop-root/nm-local-dir/usercache/root/appcache/application_1608087619253_0001/container_1608087619253_0001_01_000003/__app__.jar -Xmx1024m -Djava.io.tmpdir=/tmp/hadoop-root/nm-local-dir/usercache/root/appcache/application_1608087619253_0001/container_1608087619253_0001_01_000003/tmp -Dspark.driver.port=37890 -Dspark.yarn.app.container.log.dir=/opt/hadoop-2.7.0/logs/userlogs/application_1608087619253_0001/container_1608087619253_0001_01_000003 -XX:OnOutOfMemoryError=kill %p
    ```

  - 查看服务的spark监控页面

    - 可以看到YARN上一共创建了4个container，一个是AM所运行的container，还有3个是我们提交thrift server所指定的executor数量。

    ![image-20210205161347514](images/image-20210205161347514.png)

## 使用beeline连接ThriftServer2

- beeline连接thriftserver2

  ```shell
  beeline
  !connect jdbc:hive2://spark.bigdata.cn:10001
  
  [root@c5836fa7593c conf]# beeline
  Beeline version 1.2.1.spark2 by Apache Hive
  beeline> !connect jdbc:hive2://spark.bigdata.cn:10001
  Connecting to jdbc:hive2://spark.bigdata.cn:10001
  Enter username for jdbc:hive2://spark.bigdata.cn:10001: root
  Enter password for jdbc:hive2://spark.bigdata.cn:10001: 
  20/12/11 07:20:04 INFO jdbc.Utils: Supplied authorities: spark.bigdata.cn:10001
  20/12/11 07:20:04 INFO jdbc.Utils: Resolved authority: spark.bigdata.cn:10001
  20/12/11 07:20:04 INFO jdbc.HiveConnection: Will try to open client transport with JDBC Uri: jdbc:hive2://spark.bigdata.cn:10001
  Connected to: Spark SQL (version 2.4.7)
  Driver: Hive JDBC (version 1.2.1.spark2)
  Transaction isolation: TRANSACTION_REPEATABLE_READ
  0: jdbc:hive2://spark.bigdata.cn:10001> show databases;
  +---------------+--+
  | databaseName  |
  +---------------+--+
  | default       |
  | test          |
  +---------------+--+
  2 rows selected (0.719 seconds)
  ```

  

- 在web ui上查看运行运行的sql语句

  ![image-20210205161538129](images/image-20210205161538129.png)

## 配置spark thrift server自动启动

### 创建启动脚本

- 创建/etc/bootstrap.sh文件

  ```shell
  # !/bin/sh
  source /etc/profile
  # 启动history server
  start-history-server.sh 
  
  # 启动thrift server
  start-thriftserver.sh --name sparksql-thrift-server \
  --master yarn \
  --deploy-mode client \
  --driver-memory 1g \
  --hiveconf hive.server2.thrift.http.port=10001 \
  --num-executors 3 \
  --executor-memory 1g \
  --conf spark.sql.shuffle.partitions=2
  ```

  > --num-executors参数的值最好改为1个，减少内存资源占用

### 设置脚本执行权限

`chmod a+x /etc/bootstrap.sh`

### 加入自动启动服务

```shell
vim /etc/rc.d/rc.local 
/etc/bootstrap.sh

chmod 755 /etc/rc.d/rc.local 
```

### 启动spark容器(包含thriftserver)

`docker restart spark`

