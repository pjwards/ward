[![Stories in Ready](https://badge.waffle.io/egaoneko/ward.png?label=ready&title=Ready)](https://waffle.io/egaoneko/ward)

# [Ward](http://pjwards.com)
Ward collects data of Facebook groups using Facebook Graph API and shows various information about each group of Facebook.
* Ward does not collect data of all Facebook groups. Only gets data of requested public groups from users.


## Requirements

#### Back-End

* python (tested with version 3.5) ([python](https://www.python.org), [Python License](./NOTICE/LICENSE.python))
* django (tested with version 1.8.5) ([django](https://www.djangoproject.com), [BSD License](./NOTICE/LICENSE.django))
* celery (tested with version 3.1.18) ([celery](http://www.celeryproject.org), [BSD License](./NOTICE/LICENSE.celery))
* django-celery (tested with version 3.1.17) ([django-celery](https://pypi.python.org/pypi/django-celery), [BSD License](./NOTICE/LICENSE.django-celery))
* facebook-sdk (tested with version 1.0.0a0) ([facebook-sdk](https://github.com/pythonforfacebook/facebook-sdk), [Apache License 2.0](./NOTICE/LICENSE.facebook-sdk))
* mezzanine (tested with version 4.0.1) ([mezzanine](http://mezzanine.jupo.org), [BSD License](./NOTICE/LICENSE.mezzanine))
* django-rest-framework (tested with version 3.3.0) ([django-rest-framework](http://www.django-rest-framework.org), [BSD License](./NOTICE/LICENSE.django-rest-framework))
* markdown (tested with version 2.6.3) ([markdown](https://pypi.python.org/pypi/Markdown), [BSD License](./NOTICE/LICENSE.markdown))
* django-filter (tested with version 0.11.0) ([django-filter](https://github.com/alex/django-filter), [BSD License](./NOTICE/LICENSE.django-filter))
* beautifulsoup4 (tested with version 4.4.1) ([beautifulsoup4](http://www.crummy.com/software/BeautifulSoup/), [MIT License](./NOTICE/LICENSE.beautifulsoup4))
* lxml (tested with version 3.5.0) ([lxml](http://lxml.de), [BSD License](./NOTICE/LICENSE.lxml))
* django-registration (tested with version 2.0.2) ([django-registration](https://github.com/macropin/django-registration), [BSD License](./NOTICE/LICENSE.django-registration))
* JPype1-py3 (tested with version 0.5.5.2) ([JPype1-py3](https://pypi.python.org/pypi/JPype1-py3), [Apache License 2.0](./NOTICE/LICENSE.jpype1-py3))
* konlpy (tested with version 0.4.4) ([konlpy](http://konlpy.org/ko/v0.4.3/), [GPL v3](./NOTICE/LICENSE.konlpy))
* django-allauth (tested with version 0.24.1) ([django-allauth](https://github.com/pennersr/django-allauth), [MIT License](./NOTICE/LICENSE.django-allauth))
* redis (tested with version 2.10.3) ([redis](http://redis.io), [BSD License](./NOTICE/LICENSE.redis))
* uwsgi (tested with version 2.0.11.2) ([uwsgi](https://github.com/unbit/uwsgi), [GPL v2](./NOTICE/LICENSE.uwsgi))
* pylibmc (tested with version 1.5.0) ([pylibmc](https://pypi.python.org/pypi/pylibmc), [BSD License](./NOTICE/LICENSE.pylibmc))
* psycopg2 (tested with version 2.6.1) ([psycopg2](http://initd.org/psycopg/), [LGPL with exceptions or ZPL](./NOTICE/LICENSE.psycopg2))


#### Front-End

* Bootstrap ([Bootstrap](http://getbootstrap.com), [MIT License](./NOTICE/LICENSE.bootstrap))
* Bootstrap Social ([Bootstrap Social](http://lipis.github.io/bootstrap-social/), [MIT License](./NOTICE/LICENSE.bootstrap-social))
* jQuery ([jQuery](https://jquery.com), [MIT License](./NOTICE/LICENSE.jquery))
* jQuery UI ([jQuery UI](https://jqueryui.com), [MIT License](./NOTICE/LICENSE.jquery-ui))
* Font Awesome ([Font Awesome](https://fortawesome.github.io/Font-Awesome/), [SIL OFL 1.1, MIT License](./NOTICE/LICENSE.fontawesome))
* Font Awesome Animation ([Font Awesome Animation](https://github.com/l-lin/font-awesome-animation), [MIT License](./NOTICE/LICENSE.fontawesome-animation))
* JUI ([JUI](http://jui.io/ko/index.php), [MIT License](./NOTICE/LICENSE.jui))
* Start Bootstrap Creative ([Start Bootstrap](http://www.startbootstrap.com), [Apache License 2.0](./NOTICE/LICENSE.startbootstrap))
* Start Bootstrap SB Admin 2 ([Start Bootstrap](http://www.startbootstrap.com), [Apache License 2.0](./NOTICE/LICENSE.startbootstrap))
* Bootstrap Login Form ([AZMIND](http://azmind.com/2015/04/19/bootstrap-login-forms/), [MIT License](./NOTICE/LICENSE.azmind))
* html2canvas ([html2canvas](https://html2canvas.hertzen.com), [MIT License](./NOTICE/LICENSE.html2canvas))
* jqPlot ([jqPlot](http://www.jqplot.com), [GPL v2, MIT License](./NOTICE/LICENSE.jqplot))


#### Etc

* PostgreSQL ([PostgreSQL](http://www.postgresql.org))
* Redis ([Redis](http://www.redis.io))
* Node.js ([Node.js](https://nodejs.org/en/))
* Bower ([Bower](http://bower.io))


## Installation

#### How to install?

##### Docker

Ward uses Docker, so you can install easily by using Docker.
If you learn more about Docker, [this site](https://docs.docker.com) helps you.

```bash
cd [product_forder]
docker build -t=ward .
docker run --name ward -it -p 80:80 -v /var/log/ward:/var/log ward:latest
```


##### Mac

```bash
pip install -r requirements.txt
brew install redis
brew install node
npm install bower
bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)

cd [product_forder]
bower install
cd [product_forder]/www
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

# Mecab
sudo apt-get install curl
bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)

cd workspace
sudo chown www-data:www-data -R *

cd [product_forder]
bower install
cd [product_forder]/www
python manage.py migrate
python manage.py createsuperuser

```


## Local Setting


#### setting.py

You must modify `local_settings.py` of `ward/wwww/fb_archive` in your environment.


#### OAuth Setting

1. Go social application in admin page([http://localhost/admin](http://localhost/admin)).
2. Click `Add social application` and input fackebook for `Name`, app id for `Client id` and app secret for`Secret key`.
If you learn more, [this site](https://godjango.com/65-starting-with-django-allauth/) helps you.


## TIP

### Pycharm

If you face unresolved reference issue in pycharm, check below.

1. Right click `www` folder and go `Source root` in `Mark Directory As` and set this.
2. Go `Preferences...` > `Build, Execution, Deployment` > `Console` > `Python Console` and check `add source roots to PYTHONPATH`.
3. If you don't understand previous steps, [This site](http://stackoverflow.com/questions/21236824/unresolved-reference-issue-in-pycharm) helps you to set.
4. Go `Preferences...` > `Languages & Frameworks` > `Django` and input `www` folder for `Django project root`, 
`fb_archive/settings.py` for `Settings` and `manage.py` for `Manage script`. 


## License
Ward uses the [MIT License](./LICENSE).
