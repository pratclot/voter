#!/bin/sh

wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
chmod +x cloud_sql_proxy

export YOUR_INSTANCE_CONNECTION_NAME=$(gcloud sql instances describe "${YOUR_INSTANCE_NAME}" | awk '/connectionName/ {print $NF}')
./cloud_sql_proxy -instances=\"${YOUR_INSTANCE_CONNECTION_NAME}\"=tcp:"${MYSQL_PORT}" &

echo 'Working on configs...'
envsubst < my.cnf.tpl > my.cnf
envsubst < voter/auth.py.tpl > voter/auth.py
echo 'Done with the configs'

echo 'Creating venv and installing requirements...'
virtualenv env
source env/bin/activate
pip install -r requirements.txt
echo 'Environment is prepared'

echo 'Running Django tools...'
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

echo 'Stopping SQL proxy...'
pkill -9 -f cloud_sql_proxy
echo 'Stopped the proxy'

echo 'Generating my.cnf for GAE...'
envsubst < my.cnf.tpl.socket > my.cnf
echo 'Done with the config'

echo 'Deploying to GAE...'
gcloud app deploy

