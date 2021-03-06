# 加密文件重复性检测系统

## 具体要求

在网络存储应用中，为了节省存储空间，通常会对重复数据进行消除操作。本题目致力于设计和实现一个加密文件的重复性检测系统，其中用户文件采用AES对称密码加密后上传至服务器的同时，利用SHA-1算法生成校验符一并上传。当上传重复数据时，服务器提示不上传；用户可以将数据下载解密。通过本课题使学生深入了解密码学在机密性、重复性检测等领域的实现原理，提升编程能力。
题目的具体要求如下：

(1)	查阅相关资料，掌握密文去重算法的原理和实现细节；熟悉AES算法、Hash算法等基本的密码算法的实现；

(2)	选择一种编程语言和开发工具，设计和实现密文去重系统，对不同类型、不同大小的文件进行重复性验证，分析比较检测的准确率、执行效率等指标；

(3)	程序具有图形化用户界面，输出美观；

(4)	可根据自己能力，在完成以上基本要求后，对程序功能进行适当扩充；

(5)	撰写报告，对所采用的算法、程序结构和主要函数过程以及关键变量进行详细的说明；对程序的调试过程所遇到的问题进行回顾和分析，对测试和运行结果进行分析；总结软件设计和实习的经验和体会，进一步改进的设想；

(6)	提供关键程序的清单、源程序及可执行文件和相关的软件说明。

## 架构设计

### 客户端-服务端模型

服务端提供相应的api，以http服务的形式呈现给客户端。

客户端通过访问这些api来与服务器交互，完成文件的上传、下载、获取和删除操作。

为了防止未授权用户访问，服务端会对api请求进行身份认证，只有携带正确token的请求才能被正常处理。

![image-20210616134918768](https://soreatu-1300077947.cos.ap-nanjing.myqcloud.com/uPic/image-20210616134918768.png)

#### 文件上传

客户端需要自己对需要上传的文件进行加密，并计算SHA1摘要值，通过upload将密文和摘要值一并发送给服务端。

服务器首先会对摘要值进行判断，是否存在重复上传的情况。若在已上传文件中有摘要值与当前摘要值一样，则说明重复上传，返回给客户端"file exists"响应；否则，读取上传文件并保存在server/upload目录中。

#### 文件下载

客户端可以通过download来下载上传到云存储服务器上的密文文件，下载到本地后，需要自行进行解密，解密后的文件保存在client/download目录中

### 客户端架构

客户端采用Python语言编写

- 用户界面：PyQt5

- 客户端服务端交互：requests

- 密码算法：AES、SHA-1

### 服务端架构

客户端采用golang语言编写

- http服务框架：gin
- 数据库：sqlite3

## 使用

```
$ git clone https://github.com/soreatu/baby-ciphertext-deduplicate-system.git
```

编译服务端，或者从[Releases](https://github.com/soreatu/baby-ciphertext-deduplicate-system/releases)中下载mac版已经编译好的armory

```
$ cd server
$ go build -o armory .
```

配置客户端环境

```
$ python3 -m pip install PyQt5
```

启动服务端

```
$ cd server
$ ./armory
```

启动客户端

```
$ cd client
$ python3 main.py
```

## Authors

[soreatu](https://github.com/soreatu)

[jylsec](https://github.com/swfangzhang)

[oops]()

