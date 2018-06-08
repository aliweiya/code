# Introduction

该代码使用**中间人攻击**（Man in the middle attack）爬取微信公众号。

# Requirments

- 中间代理使用[anyproxy](http://anyproxy.io/cn/)。
- 需要一步手机发起微信公众号访问请求，确保手机能使用anyproxy作为代理。

# Usage

## 安装Node.js
### Centos
```
yum install nodejs
```
### windows
去官网下载安装
## npm安装下列包
```
npm install -g anyproxy
npm install -g cheerio
npm install -g mongodb
```
## anyproxy生成证书
```
./node_modules/anyproxy/bin/anyproxy-ca
```
## 安装证书
### Centos
```
cp .anyproxy/certificates/rootCA.crt /etc/pki/ca-trust/source/anchors/rootCA.crt
update-ca-trust extract
```
### Windows
访问`http://ip:8002/fetchCrtFile`安装证书（访问不到的话关闭防火墙）

http://anyproxy.io/cn/#windows%E7%B3%BB%E7%BB%9F%E4%BF%A1%E4%BB%BBca%E8%AF%81%E4%B9%A6

手机也需要安装证书，方法同windows。

## 设置手机代理为anyproxy

各手机设置方法不同，请上网查找。

## 启动anyproxy
```
anyproxy --intercept -r rule_wechat.js -s
```