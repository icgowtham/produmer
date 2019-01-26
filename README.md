# README

This is a Python based producer and consumer application which makes use of:
  - RabbitMQ
  - Celery
  - Postgres Database

# Prerequisites
### NOTE: The instructions are given as on Ubuntu (> 16.04)

For testing the application, the following packages need to be installed first:
  - RabbitMQ Server
  - Python 3
  - Docker
  - Postgresql Client
### Installation

#### Using the ansible-playbook to install the dependent packages
An ansible playbook is made available for installing most of the depedent packages. It can be used as below:
```sh
$ ansible-playbook app_setup.yaml --extra-vars "location=/home/gowtham/work"
```


#### Manually installing the dependent packages
Install the dependencies as root user.

```sh
$ apt-get install rabbitmq-server
$ apt install python3-pip
$ apt install virtualenv
$ apt install docker.io
$ apt-get install postgresql-client-common
$ apt-get install postgresql-client
```

Download the repo to disk:
```sh
$ git clone https://github.com/icgowtham/produmer.git
```

Change to the source code directory:
```sh
$ cd produmer
```

Create a Python3 virtual environment and install the application requirements:
```sh
$ virtualenv -p python3 env
$ source env/bin/activate
$ pip3 install --upgrade pip
$ pip3 install -r requirements.txt
```

Setup the Postgres database container:
```sh
$ sudo docker pull postgres
$ mkdir -p $HOME/docker/volumes/postgres
$ sudo docker run --rm --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data postgres
```

Create the database table:
```sh
$ export PGPASSWORD='docker'; psql -h localhost -U postgres -d postgres

CREATE TABLE user_info(user_id SERIAL PRIMARY KEY, username VARCHAR (50) UNIQUE NOT NULL, email VARCHAR (355) UNIQUE NOT NULL);

\q
```

Under one SSH terminal start the Celery worker(s) from the application directory:
```sh
$ celery -A tasks.tasks worker --loglevel=info
```

In another SSH terminal, change to the project directory and execute the client code:
```sh
python3 client.py
```
