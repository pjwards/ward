FROM ubuntu:14.04
MAINTAINER Donghyun Seo <egaoneko@naver.com>

RUN apt-get update
RUN apt-get install -y build-essential git
RUN apt-get install -y python python-dev python3 python3-dev python3-pip
RUN apt-get install -y nginx uwsgi uwsgi-plugin-python3

RUN pip3 install uwsgi

RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
RUN chown -R www-data:www-data /var/lib/nginx

# UWSGI
ENV UWSGIVERSION 2.0.11.2

RUN apt-get update && apt-get install -y --no-install-recommends \
            build-essential \
            libjansson-dev \
            libpcre3-dev \
            libssl-dev \
            libxml2-dev \
            wget \
            zlib1g-dev

RUN cd /usr/src && \
    wget --quiet -O - http://projects.unbit.it/downloads/uwsgi-${UWSGIVERSION}.tar.gz | \
    tar zxvf -

RUN cd /usr/src/uwsgi-${UWSGIVERSION} && make
RUN cp /usr/src/uwsgi-${UWSGIVERSION}/uwsgi /usr/local/bin/uwsgi
RUN PYTHON=/usr/local/python3.4/bin/python3.4
RUN cd /usr/src/uwsgi-${UWSGIVERSION} && ./uwsgi --build-plugin "plugins/python python34"
RUN mkdir -p /usr/local/lib/uwsgi/plugins
RUN cp /usr/src/uwsgi-${UWSGIVERSION}/*.so /usr/local/lib/uwsgi/plugins

# Java
ENV VERSION 7
ENV UPDATE 80
ENV BUILD 15

ENV JAVA_HOME /usr/lib/jvm/java-${VERSION}-oracle
ENV JRE_HOME ${JAVA_HOME}/jre

RUN apt-get update && apt-get install ca-certificates curl -y && \
	curl --silent --location --retry 3 --cacert /etc/ssl/certs/GeoTrust_Global_CA.pem \
	--header "Cookie: oraclelicense=accept-securebackup-cookie;" \
	http://download.oracle.com/otn-pub/java/jdk/"${VERSION}"u"${UPDATE}"-b"${BUILD}"/server-jre-"${VERSION}"u"${UPDATE}"-linux-x64.tar.gz \
	| tar xz -C /tmp && \
	mkdir -p /usr/lib/jvm && mv /tmp/jdk1.${VERSION}.0_${UPDATE} "${JAVA_HOME}" && \
	apt-get autoclean && apt-get --purge -y autoremove && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN update-alternatives --install "/usr/bin/java" "java" "${JRE_HOME}/bin/java" 1 && \
	update-alternatives --install "/usr/bin/javac" "javac" "${JAVA_HOME}/bin/javac" 1 && \
	update-alternatives --set java "${JRE_HOME}/bin/java" && \
	update-alternatives --set javac "${JAVA_HOME}/bin/javac"

# Node
RUN \
  apt-get update && \
  apt-get install -yqq curl \
  wget git python build-essential g++ libkrb5-dev libfreetype6 libfontconfig \
  libjpeg8 libpng12-0 libicu-dev libcurl3 libcurl3-gnutls libcurl4-openssl-dev \
  libcurl3 libcurl3-gnutls libcurl4-openssl-dev && \
  curl --silent --location https://deb.nodesource.com/setup_0.10 | bash - && \
  apt-get install -yqq nodejs && \
  wget -O - 'https://s3.amazonaws.com/travis-phantomjs/phantomjs-2.0.0-ubuntu-14.04.tar.bz2' | tar xjf - -C ~/ && \
  mv ~/phantomjs /usr/local/bin/ && \
  npm install -g npm@2.7.5 && \
  apt-get autoremove -yqq && \
  apt-get clean
RUN npm install -g bower

# Redis
RUN apt-get update -qq && apt-get install -y python-software-properties sudo
RUN apt-get install -y redis-server

# Psycopg2
RUN apt-get install -y python-psycopg2

# Project
ENV PROJECT_DIR /home/ubuntu/workspace/ward
ADD . ${PROJECT_DIR}
RUN ls -s ${PROJECT_DIR}/conf/redis.conf /etc/redis/redis.conf
RUN ls -s ${PROJECT_DIR}/conf/nginx-app.conf /etc/nginx/sites-enabled/
RUN ls -s ${PROJECT_DIR}/conf/uwsgi.ini /etc/uwsgi/apps-enabled/

RUN cd ${PROJECT_DIR} && bower --allow-root install
RUN cd ${PROJECT_DIR} && pip3 install -r requirements.txt
RUN ls ${PROJECT_DIR}

VOLUME ["/data", \
		"/etc/nginx/site-enabled", "/var/log/nginx", \
		"/etc/uwsgi/apps-enabled", "/var/log/uwsgi",  \
		"/var/lib/redis", "/etc/redis"]

# CMD ["/usr/local/bin/run"]

EXPOSE 80
EXPOSE 443
# EXPOSE 6379
