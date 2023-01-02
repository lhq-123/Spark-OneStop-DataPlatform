# docker服务安装

## 配置CentOS7阿里云yum源

```shell
cd /etc/yum.repos.d/
mv CentOS-Base.repo CentOS-Base.repo.bak
wget -O CentOs-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
```

## yum源更新

```shell
yum clean all
yum makecache
```

## 安装Docker所需依赖包

```shell
yum install -y yum-utils device-mapper-persistent-data lvm2
```

## 配置阿里云Docker yum源

```shell
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```

## 查看Docker版本

`yum list docker-ce --showduplicates`

## 安装Docker 18.03.0版本

`yum install docker-ce-18.03.0.ce`

## 启动Docker服务

```shell
systemctl enable docker
systemctl start docker
systemctl status docker
```

