﻿# ADS-IDAC-SimPy

基于Python开发的Maritime ADS-IDAC系统。
Maritime ADS-IDAC system is developed by Python.


# 系统开发架构

![系统架构](https://gitee.com/Eternal-Br/pic-bed/blob/master/ads-idac/Framework - 副本.png)

## 如何使用本系统
1. 您的计算机系统需要安装Python 3 (3.6或者更高的版本，默认安装带有相应版本的pip)，并配置好Python 和 pip的环境变量。

2. 在工程目录下使用 pip install -r requirements.txt 命令安装依赖，如果安装失败，或者在安装及使用过程中提示缺少某个依赖项，则需要您使用 python -m pip install [packagename] 手动安装。

3. 如果您有可以使用的远程数据库MySQL，请先以root身份登录到远程数据库，然后转到5，否则请转到4。

4. 如果您没有可供使用的远程数据库软件，那么需要在您的计算机系统上安装MySQL数据库软件，之后您需要做好相关的配置工作。您可以参考[这个链接](https://www.runoob.com/mysql/mysql-install.html)来安装和配置MySQL。这里默认您已经做好了相关操作，并以root身份登录到了数据库。

5. 您以root身份：

   （1）创建新的数据库 idac 

   （2）创建新用户 用户名：user1 密码：\*\*\*\*\*

   （3）为用户 user1 分配 idac 数据库权限

6. 在 src/server/opt_db.py中调用init_mysql() 函数初始化对应的数据表，注意这里的连接数据库密码应当与您在上一步中设置的一致。

7. 设置仿真参数，运行仿真程序。

8. 启动服务器，在浏览器中查看。





