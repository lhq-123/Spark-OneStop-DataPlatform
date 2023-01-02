# 查看容器ip

- 使用docker命令查看容器网络配置

  `docker inspect 容器id`

  ```shell
          "NetworkSettings": {
              "Bridge": "",
              "SandboxID": "3969ea59031932009f864375fa7fb73a23e1249a8f53ca2a1169965b1f81505b",
              "HairpinMode": false,
              "LinkLocalIPv6Address": "",
              "LinkLocalIPv6PrefixLen": 0,
              "Ports": {
                  "1521/tcp": [
                      {
                          "HostIp": "0.0.0.0",
                          "HostPort": "1521"
                      }
                  ]
              },
              "SandboxKey": "/var/run/docker/netns/3969ea590319",
              "SecondaryIPAddresses": null,
              "SecondaryIPv6Addresses": null,
              "EndpointID": "c8238864e72cb47505bfce2d88dd2608cd54b1a94c96e447e1e73fea303f0af1",
              "Gateway": "172.17.0.1",
              "GlobalIPv6Address": "",
              "GlobalIPv6PrefixLen": 0,
              "IPAddress": "172.17.0.2",
              "IPPrefixLen": 16,
              "IPv6Gateway": "",
              "MacAddress": "02:42:ac:11:00:02",
              "Networks": {
                  "bridge": {
                      "IPAMConfig": null,
                      "Links": null,
                      "Aliases": null,
                      "NetworkID": "90b73e4fb1b9a26c217eda549a2e77563ad58451b9e1c19df1e3f72cc649a0af",
                      "EndpointID": "c8238864e72cb47505bfce2d88dd2608cd54b1a94c96e447e1e73fea303f0af1",
                      "Gateway": "172.17.0.1",
                      "IPAddress": "172.17.0.2",
                      "IPPrefixLen": 16,
                      "IPv6Gateway": "",
                      "GlobalIPv6Address": "",
                      "GlobalIPv6PrefixLen": 0,
                      "MacAddress": "02:42:ac:11:00:02",
                      "DriverOpts": null
                  }
              }
          }
          ## 查看到容器的ip为172.17.0.2，网关为172.17.0.1。
  ```

  