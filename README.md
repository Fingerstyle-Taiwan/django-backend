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
make build
```

### Start docker apps (Django and PostgreSQL)
This command will launch django server and database.
See [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
```console
make up
```

### Setup a superuser for development
```console
make superuser
```

### See APIs docs
See [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)
![APIs docs screenshot](https://i.imgur.com/PnnrX91.png)


### Stop docker apps (Django and PostgreSQL)
```console
make down
```

## Usage

### Lint and test (IMPORTANT:do this before you git push, github actions will auto lint and test)

- lint
```console
make lint
```

- test
```console
make test
```



### Django commands

- create a django app
```console
 make create-app NAME=YouAppName
```

- create superuser
```console
make superuser
```

- migrations
```console
make migrations
```

- migrate
```console
make migrate
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
