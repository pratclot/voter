# voter

## Installation steps (later to be used in a pipeline)

- create my.cnf and voter/auth.py files:
```bash
[xxxx@xxxx.net voter]$ cat my.cnf
[client]
host = localhost
port = 3306
database = voter
user = voter
password = xxxx
default-character-set = utf8
protocol = tcp
[xxxx@xxxx.net voter]$ cat voter/auth.py
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ='xxxx.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'xxxx'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xxxx'

ALLOWED_HOSTS = ['xxxx.com']
[xxxx@xxxx.net voter]$
```
- start up the container:
```bash
docker-compose up -d
```
- create tables in the database:
```bash
docker-compose exec voter python manage.py migrate
```
- restart the container:
```bash
docker-compose restart
```
- in case something goes wrong you can always start the server manually. For 
this, change the entrypoint to /bin/sleep and then run:
```bash
docker-compose exec voter python manage.py runserver
```
- there is a debug.log file also present but it is not working at the moment!

## Hints

On Windows 'host' directive in my.cnf is being ignored for some reason, 
please specify the 'HOST' key in DATABASES['default'] manually. This dict is 
set up in mycnf.py file.