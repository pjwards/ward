#!/bin/sh

# Start Celery (but, before you must run rabbitmq-server or redis-server)
celery --app=fb_archive.celery:app worker --loglevel=INFO
