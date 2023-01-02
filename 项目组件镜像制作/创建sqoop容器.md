# 创建sqoop容器

## 上传并解压sqoop安装包

- 上传sqoop安装包到/mnt/docker_share

  - sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz

- 解压安装包并重命名

  ```shell
  tar -xvzf sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz -C /opt
  mv /opt/sqoop-1.4.7.bin__hadoop-2.6.0/ /opt/sqoop
  ```

## 配置oracle驱动

- 后续需要将Oracle中的数据导入到HDFS，所需需要将Oracle的JDBC驱动放入到SQOOP中

### 上传oracle驱动

- 拷贝oracle驱动包到sqoop的lib目录中,把oracle驱动上传到宿主机的/mnt/docker_share文件夹中
  - ojdbc-full.tar.gz

### 解压驱动

```shell
tar -xvzf ojdbc-full.tar.gz -C /opt/sqoop/lib/
mv /opt/sqoop/lib/OJDBC-Full/* /opt/sqoop/lib
```

## 配置sqoop环境变量

- 修改sqoop配置文件,配置sqoop环境变量

  ```shell
  cd /opt/sqoop/conf
  cp sqoop-env-template.sh sqoop-env.sh
  vim sqoop-env.sh
  
  export HADOOP_COMMON_HOME=/opt/hadoop-2.7.0
  export HADOOP_MAPRED_HOME=/opt/hadoop-2.7.0
  export HIVE_HOME=/opt/apache-hive-2.1.0-bin
  ```

## 创建sqoop容器

- 创建docker容器，用于部署sqoop

  ```shell
  docker run \
  --privileged=true \
  --net docker-bd0 \
  --ip 172.33.0.110 \
  -v /mnt/docker_share:/mnt/docker_share \
  -v /etc/hosts:/etc/hosts \
  -v /opt/hadoop-2.7.0:/opt/hadoop-2.7.0 \
  -v /opt/jdk1.8.0_141:/opt/jdk1.8.0_141 \
  -v /opt/apache-hive-2.1.0-bin:/opt/apache-hive-2.1.0-bin \
  -v /opt/sqoop:/opt/sqoop \
  --name sqoop -d hadoop:2.7.0
  ```

## 配置环境变量

- 进入容器

  `docker exec -it sqoop bash`

- 配置环境变量

  ```shell
  vim /etc/profile
  
  export HIVE_HOME=/opt/apache-hive-2.1.0-bin
  export SQOOP_HOME=/opt/sqoop
  export PATH=${SQOOP_HOME}/bin:$PATH
  
  source /etc/profile
  ```

## 测试sqoop

- 启动oracle、sqoop、hadoop服务

  `docker start oracle sqoop hadoop`

- 进入容器，加载环境变量

  `source /etc/profile`

- 执行以下sqoop导出脚本

  -  测试Oracle连接

    ```shell
    sqoop list-databases \
    --connect jdbc:oracle:thin:@oracle.bigdata.cn:1521:helowin \
    --username ciss \
    --password 123456
    ```

  - 测试sqoop导入oracle表到HDFS

    ```shell
    hdfs dfs -mkdir -p /data/test
    
    # 导出一个表测试
    sqoop import \
    --connect jdbc:oracle:thin:@oracle.bigdata.cn:1521:helowin \
    --username ciss \
    --password 123456 \
    --warehouse-dir /data/test/CISS_BASE_AREAS \
    --table CISS4.CISS_BASE_AREAS -m 1
    
    hdfs dfs -rm -r /data/test/CISS_BASE_AREAS
    ```

    