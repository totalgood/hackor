# Dockerfile for a Django Application for querying Oregon campaign data as part of the Hack Oregon project
# More info on the project at http://totalgood.github.io/hackor/
# This container has no external dependencies and should automatically run the application when started

# Note: this is a terrible example of how Dockerfiles should be written
# Normally one should not combine the database and the app in the same container,
# nor should the data be baked into the container.
# This is special case to help develop and run the demo app.

# Stat with a bloated but useful Ubuntu linux image
FROM ubuntu:15.10

MAINTAINER Dan Anolik <dan@anolik.net>
LABEL version="0.1"

# Name of the current Hack Oregon data dump file
# This file should be at the same level as this Dockerfile
# Update the name for the latest data backup file
#ENV HACKORDATA hackoregon_dump_by_wil_2015-08-11-1824
ENV HACKORDATA https://dl.dropboxusercontent.com/u/27181407/hackoregon_dump_by_wil_2015-08-11-1824.gz

##########################
# Postgres Database Setup
##########################

# Install and configure postgres
RUN apt-get update -y
RUN apt-get install -y \
   postgresql \
   postgresql-client \
   curl &&\
   apt-get clean

# Switch to the postgres user and setup the environment
USER postgres
ENV PG_VERSION=9.4 \
    PG_USER=postgres \
    PG_HOME=/var/lib/postgresql \
    PG_RUNDIR=/run/postgresql \
    PG_LOGDIR=/var/log/postgresql
ENV PG_CONFDIR="/etc/postgresql/${PG_VERSION}/main" \
     PG_BINDIR="/usr/lib/postgresql/${PG_VERSION}/bin" \
     PG_DATADIR="${PG_HOME}/${PG_VERSION}/main"

# Create the empty postgres database,
# download the HackOR data, then then load it
RUN /etc/init.d/postgresql start &&\
   psql --command "CREATE USER hackor WITH SUPERUSER PASSWORD 'hackor';" &&\
   createdb -O hackor totalgood &&\
   curl -o /tmp/hackor-dbdata.gz $HACKORDATA &&\
   gunzip /tmp/hackor-dbdata.gz &&\
   psql totalgood < /tmp/hackor-dbdata &&\
   rm /tmp/hackor-dbdata &&\
   /etc/init.d/postgresql stop

##########################
# Django App Setup
##########################

USER root

RUN apt-get install -y \
   apt-utils \
#   build-essential \
   python \
   #python-dev
   python-pip &&\
   apt-get clean

RUN pip install --upgrade pip
RUN pip install --upgrade virtualenv

# Create restricted user for the django app process
RUN addgroup --gid 500 apps
RUN useradd -g apps -ms /bin/bash django

# Create the app tree
RUN mkdir -p /usr/src/app/tmpdata && mkdir -p /usr/src/app/tmpdata
RUN chown -R django:apps /usr/src/app

# Copy app files
COPY . /usr/src/app/

# Expose the port where the app is listening
EXPOSE 4567

# Switch to the django user and setup the environment
USER django
ENV DATABASE_USER=hackor
ENV DATABASE_PASSWORD=hackor

# Move to the app directory
WORKDIR /usr/src/app

USER root

ENTRYPOINT service postgresql restart && bash
