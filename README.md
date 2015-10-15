# Facebook Archive

## Requirements

* python >= 3.5 (tested with version 3.5)
* django >= 1.8.5 (tested with version 1.8.5)
* celery (tested with version 3.1.18)
* django-celery (tested with version 3.1.17)
* facebook-sdk (tested with version 1.0.0a0)

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
brew install redis-server
```


#### django-celery

[django-celery install](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-the-django-orm-cache-as-a-result-backend)

