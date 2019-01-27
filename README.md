`produmer` - A Python based producer-consumer application.

**Table of Contents**

[TOCM]

[TOC]
## Introduction

This is a Python based producer and consumer application which makes use of:
  - RabbitMQ
  - Celery
  - Postgres Database

## Prerequisites
### NOTE: The instructions are given as on Ubuntu (> 16.04)

For testing the application, the following packages need to be installed first:
  - RabbitMQ Server
  - Python 3
  - Docker
  - Postgresql Client
  - Ansible (if using the ansible playbook for setting up the dependencies)
### Installation

#### Manually installing the dependent packages
Install the dependencies using `sudo` (i.e. as `root` user).

```sh
$ sudo apt-get install rabbitmq-server
$ sudo apt-get install python3-pip
$ sudo apt-get install virtualenv
$ sudo apt-get install docker.io
$ sudo apt-get install postgresql-client-common
$ sudo apt-get install postgresql-client
```

Download the repo:
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

Pull the Postgres database docker container from Docker Hub:
```sh
$ sudo docker pull postgres
```

#### Using the ansible-playbook to install the dependent packages
An ansible playbook is made available for installing most of the depedent packages.
```sh
$ sudo apt-get install ansible
```

An example usage of the ansible playbook is given below:
```sh
$ ansible-playbook app_setup.yaml --user=gowtham --extra-vars "ansible_sudo_pass=gowtham location=/home/gowtham/work/tmp"
```

```sh
$ ansible-playbook app_setup.yaml --user=<user> --extra-vars "ansible_sudo_pass=<sudo_password> location=<location_for_files>"
```


The ansible playbook does the following:
  - Installs the following packages:
    - python3-pip
    - python-virtualenv
    - rabbitmq-server
    - docker.io
    - postgresql-client-common
    - postgresql-client
  - Pulls the postgres docker image
  - Clones this repo
  - Sets up the Python3 virtual environment
  - Installs the project requirements

---


Create a volume to store the postgres table data. For e.g.
```sh
$ mkdir -p /home/gowtham/docker/volumes/postgres
```


Start the postgres database docker container.
```sh
$ sudo docker run --rm --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 -v /home/gowtham/docker/volumes/postgres:/var/lib/postgresql/data postgres
```


Create the database table:
```sh
$ export PGPASSWORD='docker'; psql -h localhost -U postgres -d postgres

CREATE TABLE user_info(user_id SERIAL PRIMARY KEY, username VARCHAR (50) UNIQUE NOT NULL, email VARCHAR (355) UNIQUE NOT NULL);

\q
```

---

## Running the application


Under one SSH terminal start the Celery worker(s) from the project directory:
```sh
$ celery -A tasks.tasks worker --loglevel=info
```

In another SSH terminal, change to the project directory and execute the client code:
```sh
python3 client.py
```

To check the command line options provided by the client, execute: 
```sh
python3 client.py -h
```

---

## TODO
    - Write Unit Tests
    - Test with more clients
    - Dockerize the application (including components like the RabbitMQ server, etc.)

---


## Tech

This application uses a number of open source projects to work properly:

* [Python] - an interpreted, high-level, general-purpose programming language
* [Celery] - an asynchronous task queue/job queue based on distributed message passing
* [RabbitMQ] - an open source message broker software that originally implemented the Advanced Message Queuing Protocol 
* [PostgreSQL] - an open source object-relational database system that uses and extends the SQL language combined with many features 
* [Docker] - computer program that performs operating-system-level virtualization, also known as "containerization"
* [Ubuntu] - an open source software operating system


---


License
----

MIT



   [Python]: <https://www.python.org/>
   [Celery]: <http://www.celeryproject.org/>
   [RabbitMQ]: <https://www.rabbitmq.com/>
   [PostgreSQL]: <https://www.postgresql.org/>
   [Docker]: <https://hub.docker.com/>
   [Ubuntu]: <https://www.ubuntu.com/>
