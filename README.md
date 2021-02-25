# kpp
`课评评` —— A site gives course reviews!

## Introduction

- You can review on the course you take with any words!
- You can check the course you want to pick!
- You can see brief description without reading the whole review! **JUST USE WORDCLOUD**

## 介绍

- 课评评——一个面向学生的评课网站
- 你可以在上面评价任何你上过的课程；
- 你也可以查看你想选择的课程的评价；
- 你可以不用阅读所有评论就了解这门课程的重要信息！

## Installation

The project is built by `Django`, which is easy to migrate, just take these following steps:

```shell
git clone https://github.com/Wu-Ming-Ke-Qu/kpp
cd kpp
```

Then, fill some basic settings:

```python
SECRET_KEY = '&v=$55c3h$1@2gw*@js2=a%+^!(e)8!3ycyq*%%1zg(ydk66t=' # change it if used in production environment

DEBUG = True # change it to 'False'

EMAIL_HOST_USER = 'yourname' # fill in with your SMTP username
EMAIL_HOST_PASSWORD = 'password' # fill in with your SMTP password

## SECURE SSL settings, change these if needs https://
CORS_REPLACE_HTTPS_REFERER      = False
HOST_SCHEME                     = "http://"
SECURE_PROXY_SSL_HEADER         = None
SECURE_SSL_REDIRECT             = False
SESSION_COOKIE_SECURE           = False
CSRF_COOKIE_SECURE              = False
SECURE_HSTS_SECONDS             = None
SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
SECURE_FRAME_DENY               = False
```

At last, you can run development deploy with:

```shell
python manage.py runserver
```

## Features

- Automatically generate wordcloud images if the review change, add, delete and so on
- User register and sign in system

## License

本项目采用知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议进行许可。
This repository is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.


## Contributing

fork and raise a pull request
