# Fingerstyle Taiwan Backend Project

![Github License](https://img.shields.io/badge/license-MIT-green) ![Code Coverage](https://img.shields.io/badge/coverage-100%25-green) ![Django 4](https://img.shields.io/badge/django-4.0.4-blue.svg) ![Python 3.10](https://img.shields.io/badge/python-3.10.7-blue.svg)


#### Fingerstyle Taiwan page backend project, using django and postresql for development.

## Table of content

- [**Getting Started**](#getting-started)
- [Built With](#built-with)
- [Contributing](#contributing)
- [License](#license)
- [Get Help](#get-help)
- [Acknowledgments](#acknowledgements)

## Getting Started

### Clone project
```console
git clone https://github.com/Fingerstyle-Taiwan/django-backend.git
cd django-backend
```

### Build docker container and apps
```console
make dev/build
```

### Start docker apps (Django and PostgreSQL)
This command will launch django server and database.
See [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
```console
make dev/up
```
If you get a database error after **make up**, just try the code below, it will remove the database from disk, then rebuild volume again.
```console
make dev/down
```
```console
make dev/database-init
```
```console
make dev/up
```

### Setup a superuser for development
```console
make dev/superuser
```

### See APIs docs
See [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
![APIs docs screenshot](https://i.imgur.com/PnnrX91.png)


### Stop docker apps (Django and PostgreSQL)
```console
make dev/down
```

## Usage

### make commands help
```console
make help
```
```console
Available targets:

  certbot/init                        SSL certification initialization
  dev/build                           Build docker image for development
  dev/check                           Run test and lint
  dev/create-app                      Create a Dajango Application used by "make dev/create-app NAME=YouAppNameHere"
  dev/database-init                   Initialization for docker volumes
  dev/down                            Stop development containers
  dev/lint                            Run code style tool
  dev/migrate                         Migrate for database
  dev/migrate-init                    Initialize migrations for database
  dev/migrations                      Make migrations for database
  dev/superuser                       Create a superuser
  dev/test                            Run unit test 
  dev/up                              Run development containers
  monitor/down                        Stop monitor service containers
  monitor/up                          Start monitor service containers
  prod/down                           Stop production containers 
  prod/logs                           Peek logs 
  prod/rebuild                        Rebuild Django app image
  prod/restart                        Rebuild Django app
  prod/superuser                      Create a superuser
  prod/up                             Run production containers
```

### Lint and test (IMPORTANT:do this before you git push, github actions will auto lint and test)

- lint
```console
make dev/lint
```

- test
```console
make dev/test
```



### Django commands

- create a django app
```console
 make dev/create-app NAME=YouAppName
```

- create superuser
```console
make dev/superuser
```

- migrations
```console
make dev/migrations
```

- migrate
```console
make dev/migrate
```

### Git commit

**Please use [commitizen-tools](https://github.com/commitizen-tools/commitizen) to submit your commit message.**
```console
cz c
```



## Built With

**[Docker](https://www.docker.com/)**

Docker is a software platform that allows you to quickly build, test, and deploy applications.


**[Make](https://www.gnu.org/software/make/)**

Make is a tool which controls the generation of executables and other non-source files of a program from the program's source files.

**[Django](https://www.djangoproject.com/)**

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.

**[PostgreSQL](https://www.postgresql.org/)**

PostgreSQL is a powerful, open source object-relational database system with over 30 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.



## Contributing

#### Issues
In the case of a bug report, bugfix or a suggestions, please feel very free to open an issue.

#### Pull request
Pull requests are always welcome, and I'll do my best to do reviews as fast as I can.

## License

This project is licensed under the [MIT License](https://github.com/this/project/blob/master/LICENSE)

## Get Help
- Contact us on [Discord](https://discord.gg/MjjfP5qpYt)
- If appropriate, [open an issue](https://github.com/Fingerstyle-Taiwan/django-backend/issues) on GitHub

## Acknowledgements
**[Django REST Framework](https://www.django-rest-framework.org/)** - Django REST framework is a powerful and flexible toolkit for building Web APIs.
