FROM python:3.6

RUN apt -qqy update

RUN apt -qqy install nginx

RUN git clone https://github.com/orgsea/supervisor-py3k.git

ADD ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN cd ../supervisor-py3k && python setup.py install 

RUN rm -rf /etc/nginx/sites-enabled/default

ENTRYPOINT ["python", "manage.py", "runserver"]

