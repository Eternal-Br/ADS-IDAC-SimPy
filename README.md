﻿
# ADS-IDAC-SimPy

基于Python开发的Maritime ADS-IDAC系统。
A Maritime ADS-IDAC system which is developed by Python.

ADS: The Accident Dynamics Simulator.
IDAC: The Information, Decision, and Action in a Crew context cognitive model.

# 系统开发架构

![系统架构](https://s1.ax1x.com/2020/05/13/YwJzLQ.png)

## 如何使用本系统
1. 您的计算机系统需要安装Python 3 (3.6或者更高的版本，默认安装带有相应版本的pip)，并配置好Python 和 pip的环境变量。

2. 在工程目录下使用 *pip install -r requirements.txt* 命令安装依赖，如果安装失败，或者在安装及使用过程中提示缺少某个依赖项，则需要您使用 *python -m pip install [packagename]* 手动安装。

3. 如果您有可以使用的远程数据库MySQL，请先以root身份登录到远程数据库，然后转到5，否则请转到4。

4. 如果您没有可供使用的远程数据库软件，那么需要在您的计算机系统上安装MySQL数据库软件，之后您需要做好相关的配置工作。您可以参考[这个链接](https://www.runoob.com/mysql/mysql-install.html)来安装和配置MySQL。再安装过程中选择认证方式的时候，建议选择 *Use legacy Authentacion Method* 这种方式。这里默认您已经做好了相关操作，并以root身份登录到了数据库。

5. 您以root身份：

   （1）创建新的数据库 *idac* 

   （2）创建新用户 用户名：*user1* 密码：\*\*\*\*\*

   （3）为用户 user1 分配 idac 数据库权限

6. 在 src/server/opt_db.py 中调用init_mysql() 函数初始化对应的数据表，注意这里的连接数据库密码应当与您在上一步中设置的一致。

7. 设置仿真参数，运行仿真程序。

8. 启动服务器，在浏览器中查看。

 ## How to use this system
 1. You need to install Python 3 (version 3.6 or higher, with the corresponding version of pip installed by default)  on your computer, and configure the environment variables of Python and pip.

2. Use this command *pip install -r requirements.txt* in the project directory to install the dependencies. If the installation fails, or a certain dependency is missing during installation and use, you need to use *python -m pip install [packagename]* to install it manually.

3. If you have a remote database MySQL that you can use, please log in to the remote database as root first, then go to 5, otherwise go to 4.

4. If you do not have the remote database software available, you need to install the MySQL database software on your computer system, and then you need to do the related configuration work. You can refer to [this link](https://phoenixnap.com/kb/install-mysql-on-windows) to install and configure MySQL. But I recommand you selecting *Use legacy Authentacion Method* when chosing Authentacion Methods. By default here, you have already done the relevant operations and logged in to the database as root user.

5. You operate as root:

​   （1）Create a new database named *idac*

​   （2）Create a new user User name: *user1* , and whos Password is : \*\*\*\*\*

​   （3）Assign idac database permissions foruser1

6. Call the init_mysql () function in src/server/opt_db.py to initialize the corresponding data table. Note that the password for connecting to the database here should be the same as the one you set in the previous step.

7. Set the simulation parameters and run the simulation program.

8. Start the server and view it in the browser. You'd better switch to */en_version* route or just click on the button that named *Switch to English* to browse the older version of the page.



