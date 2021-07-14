#!/bin/bash
celery -A tasks.app worker --loglevel=info  -Q default -n worker0@0.0.0.0 &
celery -A tasks.app worker --loglevel=info  -Q sunshine -n worker1@0.0.0.0 &
celery -A tasks.app worker --loglevel=info  -Q moon  -n worker2@0.0.0.0
