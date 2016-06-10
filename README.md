# codingpy.com
A site about Python, built with Python3.5, Flask, MySQL, and Semantic-UI.

## Create database 
Change the origin database to MySQL

```sql
create database codingpy DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'codingpy'@'%' IDENTIFIED BY 'codingpy2016';
GRANT ALL PRIVILEGES ON codingpy.* TO 'codingpy'@'%';
FLUSH PRIVILEGES;
```

## Initial
First time to run, initial:

#### 1. Create virtualenv

Change to the virtualenv using Python3.5. 

Some classes do not support Python2.7.

```
source venv/bin/activate
```

#### 2. Initial Database

At the first time, migrate the database

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
初始化Role数据
```
python manage.py db shell
```

```
>>> from codingpy.models import Role
>>> Role.insert_roles()

```
生成的数据为：

```sql
INSERT INTO `roles` (`id`, `name`, `default`, `permissions`)
VALUES
	(1, 'Moderator', 0, 15),
	(2, 'Administrator', 0, 255),
	(3, 'User', 1, 3);

```

初始化admin用户, admin@example.com, 密码admin

```
INSERT INTO `users` (`id`, `email`, `username`, `name`, `about_me`, `role_id`, `password_hash`, `confirmed`, `member_since`, `last_seen`, `avatar_hash`, `avatar`)
VALUES
	(1, 'admin@example.com', 'admin', NULL, NULL, 2, '$2a$12$V0fn/bEjy22DBnSuzk2Eu./ScOfidBaVhosBIFvrPQn8ERRzjA4wG', 1, '2016-06-06 00:39:24', '2016-06-06 00:42:35', 'e64c7d89f26bd1972efa854d13d7dd61', NULL);

```


## Run 

#### 1. Start redis server
```
redis-server
```

#### 2. Start the web server

Start the server at [http://127.0.0.1:5000]()

```
python manage.py runserver
```

#### 3. Visit the site at [http://127.0.0.1:5000]()



# Deploy on Ubuntu Server

## Prepare

#### create User
```bash

# useradd -m -d /home/flask -s /bin/bask flask
# passwd flask
# sudo adduser flask sudo


```

#### Create virtualenv

```bash
# pip install --upgrade virtualenv
# pip install --upgrade pip
# apt-get upgrade python3

# virtualenv -p python3 flaskenv
# source flaskenv/bin/activate

# mkdir source
# cd source
# git clone https://github.com/yongli82/codingpy.git
# cd codingpy
# pip install -r requirements.txt
```

#### test running

```
# python manage.py runserver
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
At another terminal

```
# curl http://127.0.0.1:5000
<!DOCTYPE html>
<html lang="zh-CN">

<head>

    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>
 编程派 | Coding Python
 ......
 ......
```

#### Link to Gunicore and Nginx 

Gunicore and Nginx already installed and running for other django projects


```
gunicorn --bind 0.0.0.0:8000 wsgi
```


```
$ sudo supervisorctl reload  
$ sudo supervisorctl start codingpy
```












