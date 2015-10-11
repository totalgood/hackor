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
ENV HACKORDATA hackoregon_dump_by_wil_2015-08-11-1824

##########################
# Postgres Database Setup
##########################

# Install and configure postgres
RUN apt-get update -y
RUN apt-get install -y postgresql
RUN apt-get install -y postgresql-client

ENV PG_VERSION=9.4 \
    PG_USER=postgres \
    PG_HOME=/var/lib/postgresql \
    PG_RUNDIR=/run/postgresql \
    PG_LOGDIR=/var/log/postgresql
ENV PG_CONFDIR="/etc/postgresql/${PG_VERSION}/main" \
     PG_BINDIR="/usr/lib/postgresql/${PG_VERSION}/bin" \
     PG_DATADIR="${PG_HOME}/${PG_VERSION}/main"

USER postgres

# Copy an export of the HackOR data into the Docker machine for loading into the postgresql DB
COPY $HACKORDATA /tmp/hackor-dbdata

# Create the empty postgres database then load the HackOR data,
RUN /etc/init.d/postgresql start &&\
   psql --command "CREATE USER hackor WITH SUPERUSER PASSWORD 'hackor';" &&\
   createdb -O hackor hackordb &&\
   psql hackordb < /tmp/hackor-dbdata &&\
   /etc/init.d/postgresql stop

# Now let's clean up our mess
USER root
RUN rm /tmp/*
RUN apt-get clean

##########################
# Django App Setup
##########################

RUN apt-get install -y \
   apt-utils \
#   build-essential \
   python \
   python-pip
   #python-dev

RUN pip install --upgrade pip
RUN pip install --upgrade virtualenv

# Create restricted user for the django app process
RUN addgroup --gid 500 apps
RUN useradd -g apps -ms /bin/bash django

# Create the app tree
RUN mkdir -p /usr/src/app/tmpdata && mkdir -p /usr/src/app/tmpdata
RUN chown -R django:apps /usr/src/app

# Expose the port where the app is listening
EXPOSE 4567

# Switch to the restricted user
#USER django

# Move to the app directory
WORKDIR /usr/src/app

USER root

ENTRYPOINT service postgresql restart && bash
