# 创建hadoop容器

## 宿主机环境准备

### 拉取镜像

`docker pull centos:7`

### 进入存放安装包目录

`cd /mnt/docker_share`

### 上传jdk和hadoop

- 前提：安装上传软件工具(yum install lrzsz)

`rz jdk*.tar.gz;rz hadoop*.tar.gz`

### 解压软件包

- 解压到opt目录，后续我们将映射该目录下的软件包到docker容器

  ```shell
  tar -xvzf jdk-8u141-linux-x64.tar.gz -C /opt
  tar -xvzf hadoop-2.7.0.tar.gz -C /opt
  ```

### 创建用于保存数据的文件夹

```shell
mkdir -p /data/dfs/nn
mkdir -p /data/dfs/dn
```

## 容器环境准备

### 启动hadoop容器

- 注意一定要添加 --privileged=true，否则无法使用系统服务

```SHELL
docker run \
--net docker-bd0 --ip 172.33.0.121 \
-p 50070:50070 -p 8088:8088 -p 19888:19888 \
-v /mnt/docker_share:/mnt/docker_share \
-v /etc/hosts:/etc/hosts \
-v /opt/hadoop-2.7.0:/opt/hadoop-2.7.0 \
-v /opt/jdk1.8.0_141:/opt/jdk1.8.0_141 \
-v /data/dfs:/data/dfs \
--privileged=true \
-d  -it --name hadoop centos:7 \
/usr/sbin/init
```

> 注意：确保在主机上禁用SELinux

### 进入hadoop容器

```shell
docker exec -it hadoop bash
```

### 安装vim

- 为了后续方便编辑配置文件，安装一个vim

  `yum install -y vim`

### 安装ssh

- 因为启动Hadoop集群需要进行免密登录，Centos7容器需要安装ssh

```shell
yum install -y openssl openssh-server
yum install -y openssh-client*
```

- 修改ssh配置文件

  ```shell
  vim /etc/ssh/sshd_config
  # 在文件最后添加
  PermitRootLogin yes
  RSAAuthentication yes
  PubkeyAuthentication yes
  ```

- 启动ssh服务

  ```shell
  systemctl start sshd.service
  # 设置开机自动启动ssh服务
  systemctl enable sshd.service
  # 查看服务状态
  systemctl status sshd.service
  ```

## 配置免密登录

### 生成秘钥

`ssh-keygen`

### 设置密码

- 设置root用户的密码为123456

  `passwd`

### 拷贝公钥

`ssh-copy-id hadoop.bigdata.cn`

### 测试免密登录

ssh hadoop.bigdata.cn

## 配置JDK

```shell
vim /etc/profile
# 配置jdk的环境变量
export JAVA_HOME=/opt/jdk1.8.0_141
export CLASSPATH=${JAVA_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
# 让上一步配置生效
source /etc/profile
```

## 配置Hadoop

- core-site.xml

  ```xml
    <property>
      <name>fs.defaultFS</name>
      <value>hdfs://hadoop.bigdata.cn:9000</value>
    </property>
    <property>
      <name>hadoop.proxyuser.root.hosts</name>
      <value>*</value>
    </property>
    <property>
      <name>hadoop.proxyuser.root.groups</name>
      <value>*</value>
    </property>
    <property>
      <name>hadoop.http.staticuser.user</name>
      <value>root</value>
    </property>
  ```

- hdfs-site.xml

  ```xml
    <property>
      <name>dfs.namenode.http-address</name>
      <value>hadoop.bigdata.cn:50070</value>
    </property>
    <property>
      <name>dfs.namenode.secondary.http-address</name>
      <value>hadoop.bigdata.cn:50090</value>
    </property>
    <property>
      <name>dfs.replication</name>
      <value>1</value>
    </property>
    <property>
      <name>dfs.namenode.name.dir</name>
      <value>file:///data/dfs/nn</value>
    </property>
    <property>
      <name>dfs.datanode.data.dir</name>
      <value>file:///data/dfs/dn</value>
    </property>
    <property>
      <name>dfs.permissions</name>
      <value>false</value>
    </property>
  ```

- yarn-site.xml

  ```xml
    <property>
      <name>yarn.resourcemanager.hostname</name>
      <value>hadoop-yarn</value>
    </property>
    <property>
      <name>yarn.nodemanager.aux-services</name>
      <value>mapreduce_shuffle</value>
    </property>
    <property>
      <name>yarn.resourcemanager.hostname</name>
      <value>hadoop.bigdata.cn</value>
    </property>
    <property>
      <name>yarn.log-aggregation-enable</name>
      <value>true</value>
    </property>
    <property>
      <name>yarn.nodemanager.remote-app-log-dir</name>
      <value>/user/container/logs</value>
    </property>
  ```

- mapred-site.xml

  ```xml
    <property>
      <name>mapreduce.framework.name</name>
      <value>yarn</value>
    </property>
    <property>
      <name>mapreduce.jobhistory.address</name>
      <value>hadoop.bigdata.cn:10020</value>
    </property>
    <property>
      <name>mapreduce.jobhistory.webapp.address</name>
      <value>hadoop.bigdata.cn:19888</value>
    </property>
    <property>
      <name>mapreduce.jobhistory.intermediate-done-dir</name>
      <value>/tmp/mr-history</value>
    </property>
    <property>
      <name>mapreduce.jobhistory.done-dir</name>
      <value>/tmp/mr-done</value>
    </property>
  ```

- hadoop-env.sh

  ```shell
  export JAVA_HOME=/opt/jdk1.8.0_141
  ```

- slaves

  ```
  hadoop.bigdata.cn
  ```

- 配置环境变量

  - vim /etc/profile
  - source /etc/profile

  ```shell
  export HADOOP_HOME=/opt/hadoop-2.7.0
  export PATH=${HADOOP_HOME}/sbin:${HADOOP_HOME}/bin:$PATH
  ```

  

## 初始化并启动Hadoop

### 格式化hdfs

`hdfs namenode -format`

### 启动hadoop

```shell
start-all.sh 
# 启动history server
mr-jobhistory-daemon.sh start historyserver
```

### 测试hadoop

```shell
cd $HADOOP_HOME
bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.0.jar pi 2 1
```

### 查看进程

```shell
bash-4.1# jps
561 ResourceManager
659 NodeManager
2019 Jps
1559 NameNode
1752 SecondaryNameNode
249 DataNode
```

### 查看web ui

- HDFS
  - http://192.168.10.100:50070
- YARN
  - http://192.168.10.100:8088
- Job History Server
  - http://192.168.10.100:19888

## 配置开启容器启动Hadoop

### 创建启动脚本

- 创建新文件存放启动脚本

  ```shell
  touch /etc/bootstrap.sh
  chmod a+x /etc/bootstrap.sh
  vim /etc/bootstrap.sh
  ```

- 文件内容

  ```shell
  #!/bin/bash
  source /etc/profile
  cd /opt/hadoop-2.7.0
  start-dfs.sh
  start-yarn.sh
  mr-jobhistory-daemon.sh start historyserver
  ```

### 加入自动启动服务

```shell
vim /etc/rc.d/rc.local 
/etc/bootstrap.sh
# 开启执行权限
chmod 755 /etc/rc.d/rc.local
```

### 为宿主机配置域名映射

- 为了方便将来访问，在window上配置宿主机域名映射，C:\Windows\System32\drivers\etc目录下的hosts文件

- 添加以下映射（此处可以把规划好的域名映射都加进来）

  ```
  192.168.10.100 hadoop.bigdata.cn
  192.168.10.100 hive.bigdata.cn
  192.168.10.100 mysql.bigdata.cn
  192.168.10.100 oracle.bigdata.cn
  ```

  