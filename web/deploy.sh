#!/bin/bash

echo start deploy...

kill -HUP `cat application.pid`
kill `cat application.pid`

cd ~/project/xmind
export PYTHONPATH=`pwd`

cd ~/project/xmind/web
gunicorn application:app -p application.pid -b 0.0.0.0:8000 -w 4 -D

echo finish deploy...