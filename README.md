## 介绍（INTRODUCTION）

你是否还在被文件传输所困扰？微信、QQ需要登陆，不但有安全问题，大小限制也比较严格；邮箱也需要登陆，且上传下载速度得不到保证；scp命令固然好用，但是不太亲民。。

本项目可以快速地在你的服务器上部署一个下载页面，任何人都可以上传文件，上传成功后会生成一次性的URL，任何访问这个URL的用户会下载该文件。上传者可以设定有效次数和有效时间，从而可以达到”阅后即焚“的效果。

（更新中。。）

## 运行

1. clone项目

2. 安装MYSQL（已安装则跳过）

3. 建库
```SQL
CREATE DATABASE click_download DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```
4. 编写配置文件

参考：
```
[database]
username=root
password=your_password
db_name=click_download
port=3306

[flask_app]
host=http://127.0.0.1
port=11111
```

5. 建表

```
python click_orm.py
```

6. 运行

```
python flask_app.py
```