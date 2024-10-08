<div align=center>
   <img src="logo.png" width=50% alt="DDNS Server">
</div>

# Overview

DDNSS 是一个开源的 DNS 服务器(DNS Server),用于简化多台主机的 DNS 服务,客户端无需进行额外安装,通过 http 请求快速完成 ip 地址的更新,服务端在接收请求时直接获取请求的源 ip.

- 支持 IPV4/IPV6 协议.
- 支持 Docker 镜像快速部署.
- 基于 Python 语言使用 Flask 框架开发.
- 通过 CloudFlare API 完成 IP 地址更新.

## Quickstart

### Server deploy

```shell
# build image
docker build https://github.com/DaiCae/ddnss.git -t ddnss:latest
# from source code
git clone https://github.com/DaiCae/ddnss
cd ddnss && docker compose up -d
```

### Client usage

- Basic
  ```shell
  curl -4 -L http://127.0.0.1:5533/dns/update/www
  curl -6 -L http://[::1]:5533/dns/update/www
  ```
- Wtih auth

  ```shell
  curl -4 -L http://<username>:<password>@<127.0.0.1>:5533/dns/update/www
  curl -6 -L http://<username>:<password>@[::1]:5533/dns/update/www
  ```

- With crontab

  ```shell
  */1 * * * * curl -4 -L http://127.0.0.1:5533/dns/update/www
  */1 * * * * curl -6 -L http://[::1]:5533/dns/update/www

  ```

- With crontab & log

  ```shell
  */1 * * * * curl -4 -L http://127.0.0.1:5533/dns/update/www >> /var/log/dns.log
  */1 * * * * curl -6 -L http://[::1]:5533/dns/update/www >> /var/log/dns.log

  # tail /var/log/dns.log -n 100
  # tail /var/log/dns.log -n 100 | grep <host>
  ```
