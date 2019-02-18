# voter

## Installation steps (later to be used in a pipeline)

- create my.cnf and voter/auth.py files:
```bash
[xxxx@xxxx.net voter]$ cat my.cnf
[client]
host = localhost
# socket = /cloudsql/xxxx:europe-west3:xxxx
port = 3306
database = voter
user = voter
password = xxxx
default-character-set = utf8
protocol = tcp
[xxxx@xxxx.net voter]$ cat voter/auth.py
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ='xxxx.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'xxxx'
SOCIAL_AUTH_GITHUB_KEY = 'xxxx'
SOCIAL_AUTH_GITHUB_SECRET = 'xxxx'

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
- collect all static files and put them into STATIC_ROOT:
```bash
docker-compose exec voter python manage.py collectstatic
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

## Hints

On Windows 'host' directive in my.cnf is being ignored for some reason, 
please specify the 'HOST' key in DATABASES['default'] manually. This dict is 
set up in mycnf.py file.

To get this to work in Google App Engine a few tweaks need to be done:

- comment out LOGGING var in voter/settings.py (or create a debug.log file, did not test it)
- use 'socket' directive in my.cnf instead of 'host', 'port' probably also needs to go
- add a handy bash function:
```bash
(.venv36) [xxxx@xxxx.net voter_gae]$ type glogs
glogs ()
{
    if [ $# -ne 0 ]; then
        gcloud app logs tail -s $@;
    else
        gcloud app logs tail -s default;
    fi
}
```

