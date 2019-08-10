NOTICE: This is a Work In Progress Project. Merge requests are welcomed.

# Flask Empty Compose

This is a simple boilerplate for rapid creating [flask](https://flask.palletsprojects.com) projects with [docker-compose](https://docs.docker.com/compose/) support.

The main idea behind this project is to make it easy to create a production grade project, with **database**, **http server** and **web application** that can be deployed to a **swarm cloud** with little hassle.

If you usually spends too much time configuring [docker](https://www.docker.com/) for new projects, **flask-empty-compose** is for you.

## What do you get?

This template provides you with:

* docker-compose configuration
* configured [nginx](https://www.nginx.com/) http server with [letsencrypt](https://letsencrypt.org)
* configured [flask-empty](https://github.com/italomaia/flask-empty) template
* optional: configured [postgres](https://www.postgresql.org) database
* optional: configured [mongodb](https://www.mongodb.com/)
* optional: configured [redis](https://redis.io/)

## Getting Started

```
# install if cookiecutter not installed
pip install cookiecutter  # might be called pip3 in your system

# install if fabric not installed
pip install fabric  # might be called pip3 in your system

# create project from the template - linux/Mac
cookiecutter https://github.com/italomaia/flask-empty-compose

# call setup to create your web app with flask-empty
fab setup

# you're ready!
```

```
# now you're ready to go
fab env:dev up  # docker-compose up in development mode
fab env:prd up  # docker-compose up in production mode

fab env:dev build  # docker-compose build in development mode
fab env:prd build  # docker-compose build in production mode

fab env:dev on:<service_name> run:"<command>"  # docker-compose run in development mode
fab env:prd on:<service_name> run:"<command>"  # docker-compose run in production mode

fab env:dev logs:name  # docker logs on container called <name> in development mode
fab env:prd logs:name  # docker logs on container called <name> in production mode
```
