#!/bin/bash

do_start() {
   POSTGRES_DIR=/Applications/Postgres.app/
   VIRTUALENV_NAME=env
   VIRTUALENV_BINARY=/usr/local/bin/virtualenv
   POSTGRES_BINARY=/Applications/Postgres.app/Contents/Versions/9.5/bin
   MIGRATIONS_DIR=$(pwd)/migrations

   if [ ! -d "$POSTGRES_DIR" ]; then
       echo "Postgres installation not found. Please download the Mac App from
       https://github.com/PostgresApp/PostgresApp/releases/download/v2.0.2/Postgres-2.0.2.dmg
       and follow instructions in https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/"
       exit 1
   fi

   $POSTGRES_BINARY/psql -lqt | cut -d \| -f 1 | grep -qw "homecookedfood"
   if [ $? -ne 0 ]; then
       echo "Creating database homecookedfood..."
       $POSTGRES_BINARY/psql -c "CREATE DATABASE homecookedfood"
   fi

   if [ ! -x "$VIRTUALENV_BINARY" ]; then
       echo "Installing virtualenv..."
       pip install virtualenv virtualenvwrapper
   fi

   echo "Setup Flask in a virtual env..."
   $VIRTUALENV_BINARY $VIRTUALENV_NAME
   source $VIRTUALENV_NAME/bin/activate
   export PATH="$PATH:$POSTGRES_BINARY"
   echo $PATH

   echo "Installing flask and other things..."
   pip install psycopg2 Flask-SQLAlchemy Flask-Migrate flask-httpauth passlib gunicorn flask_cors

   echo "Exporting flask settings..."
   export APP_SETTINGS=config.DevelopmentConfig
   export FLASK_APP=app.py
   export DATABASE_URL="postgresql://localhost/homecookedfood"

   if [ ! -d "$MIGRATIONS_DIR" ]; then
       echo "Initializing database..."
       flask db init
   fi
   flask db migrate
   flask db upgrade
   python manage.py db upgrade

   $VIRTUALENV_NAME/bin/flask run &
   echo "Starting flask server on localhost:5000 with pid: $!"

   cd UI
   ../$VIRTUALENV_NAME/bin/python  -m http.server 8080 &
   echo "Starting HTTP server on localhost:8080 with pid: $!"
}

do_stop() {
   FLASK_SERVER_PID=$(ps -ef | grep flask | grep -v grep | awk '{print $2}')
   if [ ! -z $FLASK_SERVER_PID ]; then
      echo "Killing flask server, pid: $FLASK_SERVER_PID"
      kill $FLASK_SERVER_PID
   fi

   WEB_SERVER_PID=$(ps -ef | grep "http.server" | grep -v grep | awk '{print $2}')
   if [ ! -z $WEB_SERVER_PID ]; then
      echo "Killing HTTP server, pid: $WEB_SERVER_PID"
      kill $WEB_SERVER_PID
   fi
}

case "$1" in
   --start)
      do_start
      shift
      ;;
   --stop)
      do_stop
      shift
      ;;
   *)
      echo "Usage: $0 [--start | --stop]"
      exit 1
      ;;
esac
