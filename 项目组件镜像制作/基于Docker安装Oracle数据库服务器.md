# 基于Docker安装Oracle数据库服务器

## 拉取docker11镜像

`docker pull registry.cn-hangzhou.aliyuncs.com/helowin/oracle_11g`

- 查看已经下载的镜像

  ```shell
  [root@node1 yum.repos.d]# docker images
  REPOSITORY                                             TAG                 IMAGE ID            CREATED             SIZE
  registry.cn-hangzhou.aliyuncs.com/helowin/oracle_11g   latest              3fa112fd3642        4 years ago         6.85GB
  ```

## 创建oracle容器

- 创建容器，并将1521端口映射到Linux宿主机端口

  `docker run --net docker-bd0 --ip 172.33.0.100 -d -p 1521:1521 --name oracle 3fa112fd3642`

## 查看Oracle容器

```shell
[root@node1 yum.repos.d]# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS                    NAMES
32ee7713da98        3fa112fd3642        "/bin/sh -c '/home/o…"   About a minute ago   Up About a minute   0.0.0.0:1521->1521/tcp   oracle
```

## 配置容器Oracle环境变量

```shell
# 进入到docker容器的bash中
docker exec -it oracle bash

# 切换到root用户
su root
密码为:helowin

# 添加Oracle环境变量配置
vi /etc/profile
export ORACLE_HOME=/home/oracle/app/oracle/product/11.2.0/dbhome_2
export ORACLE_SID=helowin
export PATH=$ORACLE_HOME/bin:$PATH

# 加载环境变量
source /etc/profile
```

## oracle命令连接数据库

```shell
# 切换到oracle用户
su oracle
source /etc/profile
# 连接数据库
sqlplus /nolog
conn / as sysdba
```

## 配置oracle字符集	

- 查看oracle字符集

  ```sql
  select * from nls_database_parameters where parameter = 'NLS_CHARACTERSET';
  PARAMETER
  ------------------------------
  VALUE
  --------------------------------------------------------------------------------
  NLS_CHARACTERSET
  AL32UTF8
  ```

- 修改Oracle字符集为ZHS16GBK

  - 1.关闭数据库

    `shutdown immediate;`

  - 2.mount方式打开数据库

    `startup mount`

  - 3.配置session

    ```sql
    ALTER SYSTEM ENABLE RESTRICTED SESSION;
    ALTER SYSTEM SET JOB_QUEUE_PROCESSES=0;
    ALTER SYSTEM SET AQ_TM_PROCESSES=0;
    ```

  - 4.启动数据库

    `alter database open;`

  - 5.修改字符集

    `ALTER DATABASE character set INTERNAL_USE ZHS16GBK;`

  - 6.关闭，重新启动

    `shutdown immediate;`

    `startup`

  - 7.再次查看编码格式

    ```sql
    SQL> select * from nls_database_parameters where parameter = 'NLS_CHARACTERSET';
    NLS_CHARACTERSET
    ZHS16GBK
    ```

## 创建CISS用户并授权

```sql
create user ciss identified by 123456;
grant dba to ciss;
grant imp_full_database to ciss;
exit
```

> 如果出现问题，可以使用以下方式删除用户以及用户下所有的表`drop user ciss cascade;`

## 导入数据到oracle中

### 上传CISS库备份文件

- 将资料中的CISS_2021.dmp文件上传到Linux系统中

  ```shell
  [root@node1 ~]# rz
  rz waiting to receive.
  ?a? zmodem ′??.  °′ Ctrl+C ??.
  Transferring CISS_2021.DMP...
    100%  236892 KB 13934 KB/s 00:00:17       0 ′?
  ```

### 上传到docker容器中

```shell
# docker cp ./CISS_2021.dmp 容器ID:/home/
docker cp ./CISS_2021.dmp b5da7f6e34d0:/home/
```

### 进入到Docker容器并执行导入

```shell
-- 再进入到容器中
docker exec -it oracle bash

-- 查看DUMP目录是否存在
select * from dba_directories where DIRECTORY_NAME='DB_DUMP';
no rows selected

-- 在SQLPLUS中创建DUMP目录
create directory DB_DUMP as '/home/db_dump';

# 在Docker容器中创建DUMP目录文件夹
su root
mkdir -p /home/db_dump
chown oracle /home/db_dump
# 导入数据到DUMP目录
cd /home/db_dump

# 将DMP文件移动到DUMP目录
mv /home/CISS_2021.dmp /home/db_dump/
exit
# 使用oracle用户执行导入
source /etc/profile
impdp ciss/123456@localhost/helowin DIRECTORY=DB_DUMP DUMPFILE=CISS_2021.dmp

# 导入完成后删除dmp文件
rm -rf /home/db_dump/CISS_2021.dmp
```

## 查询数据测试

```sql
select TABLE_NAME from all_tables where TABLE_NAME LIKE 'CISS_%';
```

