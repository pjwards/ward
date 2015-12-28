[![Stories in Ready](https://badge.waffle.io/egaoneko/ward.png?label=ready&title=Ready)](https://waffle.io/egaoneko/ward)

# [Ward](http://pjwards.com)

## Requirements

#### Back-End

* python >= 3.5 (tested with version 3.5)
* django >= 1.8.5 (tested with version 1.8.5)
* celery (tested with version 3.1.18)
* django-celery (tested with version 3.1.17)
* facebook-sdk (tested with version 1.0.0a0)
* mezzanine (tested with version 4.0.1)
* django-rest-framework (tested with version 3.3.0)
* markdown (tested with version 2.6.3)
* django-filter (tested with version 0.11.0)
* beautifulsoup4 (tested with version 4.4.1)
* lxml (tested with version 3.5.0)
* django-registration (tested with version 2.0.2)
* JPype1-py3 (tested with version 0.5.5.2)
* konlpy (tested with version 0.4.4)
* django-allauth (tested with version 0.24.1)
* redis (tested with version 2.10.3)
* uwsgi (tested with version 2.0.11.2)
* pylibmc (tested with version 1.5.0)
* psycopg2 (tested with version 2.6.1)
* MeCab


#### Front-End

* Bootstrap
* Bootstrap Social
* jQuery
* jQuery UI
* Font Awesome
* JUI
* Start Bootstrap Creative ([Start Bootstrap](http://www.startbootstrap.com))
* Start Bootstrap SB Admin 2 ([Start Bootstrap](http://www.startbootstrap.com))
* Bootstrap Login Form ([AZMIND](http://azmind.com/2015/04/19/bootstrap-login-forms/))
* html2canvas


## Installation

#### How to install?

##### Docker

Ward uses Docker, so you can easy to install by using Docker.
If you learn more about Docker, [this site](https://docs.docker.com) helps you.

```bash
docker build -t=ward .
docker run --name ward -it -p 80:80 -v /var/log/ward:/var/log ward:latest
```


##### Mac

```bash
pip install -r requirements.txt
brew install redis
brew install node
npm install bower

cd product_forder
bower install
cd product_folder/www
mkdir logs
python manage.py migrate
python manage.py createsuperuser

sudo redis-server
. run_celery.sh
```


##### Ubuntu

```bash
# JPype1-py3
sudo apt-get install default-jdk
sudo apt-get install g++ python3-dev

# lxml
sudo apt-get install python3-lxml
sudo apt-get install libxml2-dev libxslt-dev python-dev
sudo apt-get build-dep python3-lxml

# Pillow
sudo apt-get build-dep python-imaging
sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev

# psycopg2
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev python-dev

# npm
sudo apt-get install -y python-software-properties python g++ make
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install nodejs
sudo apt-get install npm
sudo npm install -g bower

# redis
sudo apt-get install redis-server

cd workspace
sudo chown www-data:www-data -R *

cd product_forder
bower install
cd product_folder/www
mkdir logs
python manage.py migrate
python manage.py createsuperuser

```


#### setting.py

You must set your own `local_settings.py` in `ward/wwww/fb_archive`.


#### OAuth Setting

Go to admin sites and add social application.
You need app id, app secret for facebook oauth.
If you learn more, [this site](https://godjango.com/65-starting-with-django-allauth/) helps you.


#### MeCab

##### Ubuntu

```bash
sudo yum install curl
bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
```

##### Mac

```bash
bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
```

## Tip

### Pycharm

If you face unresolved reference issue in pycharm, you should make 'www' Source root. And you set 'add source roots to PYTHONPATH' in pycharm preference.

[This site](http://stackoverflow.com/questions/21236824/unresolved-reference-issue-in-pycharm) helps you to set.

And set 'Django Support' in pycharm preference, such as 'Django project root', 'Settings' and 'manage.py'.



