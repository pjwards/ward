[![Stories in Ready](https://badge.waffle.io/egaoneko/fb_archive.png?label=ready&title=Ready)](https://waffle.io/egaoneko/fb_archive)

# Facebook Archive

## Requirements

#### Back-End

* python >= 3.5 (tested with version 3.5)
* django >= 1.8.5 (tested with version 1.8.5)
* celery (tested with version 3.1.18)
* django-celery (tested with version 3.1.17)
* facebook-sdk (tested with version 1.0.0a0)
* mezzanine (tested with version 4.0.1)
* django-bower (tested with version 5.0.4)
* django-rest-framework (tested with version 3.3.0)
* markdown (tested with version 2.6.3)
* django-filter (tested with version 0.11.0)

#### Front-End

* jQuery
* jQuery UI
* Font Awesome
* JUI

#### Optional dependencies:

* redis (tested with version 2.10.3)
* rabbitmq-server
* redis-server


## Installation

### Celery

#### rabbitmq-server

##### Ubuntu

```bash
sudo apt-get install rabbitmq-server
```
##### Mac

```bash
brew install rabbitmq-server
```

The RabbitMQ server scripts are installed into /usr/local/sbin. This is not automatically added to your path, so you may wish to add
PATH=$PATH:/usr/local/sbin to your .bash_profile or .profile.

```bash
sudo rabbitmq-server
sudo rabbitmqctl add_user user password
sudo rabbitmqctl add_vhost vir_host
sudo rabbitmqctl set_permissions -p vir_host user ".*" ".*" ".*"
```


#### redis-server

##### Ubuntu

```bash
sudo apt-get install redis-server
```

##### Mac

```bash
brew install redis
```


#### django-celery

[django-celery install](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-the-django-orm-cache-as-a-result-backend)


#### django-bower

[django-bower install](https://django-bower.readthedocs.org/en/latest/installation.html)

```bash
brew install nodejs
npm install bower
```

## Tip

### Pycharm

If you face unresolved reference issue in pycharm, you should make 'www' Source root. And you set 'add source roots to PYTHONPATH' in pycharm preference.

[This site](http://stackoverflow.com/questions/21236824/unresolved-reference-issue-in-pycharm) help you to set.

And set 'Django Support' in pycharm preference, such as 'Django project root', 'Settings' and 'manage.py'.


### DB

```bash
python manage.py migrate
python manage.py createsuperuser
```


## How to install?

### Mac

```bash
pip install -r requirements.txt
brew install redis
brew install node
npm install bower

cd product_folder/www
mkdir logs
python manage.py migrate
python manage.py bower install
python manage.py createsuperuser

sudo redis-server
. run_celery.sh
```