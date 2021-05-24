# Pokemon REST API with Python, Django and DRF


[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Pokemon REST API to manage pokemons.

## Requirements
This Requirements are necessary to get the environment working:
- Python <= 3.7.0
- asgiref == 3.2.3
- Django == 3.0.2
- django-cors-headers == 3.2.1
- django-environ == 0.4.5
- djangorestframework == 3.11.0
- djangorestframework-simplejwt == 4.4.0
- environ == 1.0
- psycopg2 == 2.8.4
- PyJWT == 1.7.1
- pytz == 2019.3
- sqlparse == 0.3.0


## Database


- PostgreSQL


## Installation

1) Create .env file using .env.example file from the root folder:

```sh
cp .env.example .env
```

2) Change the database name on the PostgreSQL URL to yours or use the one from the example:

```sh
DATABASE_URL=psql://postgres:postgres@127.0.0.1:5432/<YOUR_DATABASE_NAME_HERE>
```

3) Run pip to install the requirements on the requirements.txt file from the root folder:

```sh
pip install -r requirements.text
```
4) Run the migrations to create the tables needed on the DB from the root folder:

```sh
python manage.py migrate
```

5) Run the server from the root folder:

```sh
python manage.py runserver
```

You can now access from this URL: http://127.0.0.1:8000/
## Populate DB

Run the following route to populate the DB using the .json files containing pokemons, regions, locations and areas data:

- *api/populate/*


## List of routes availables

- [GET] *api/populate/*
- [POST] *api/register/*
- [POST] *api/login/*
- [GET] *api/pokemons/*
- [GET] *api/pokemons/<int:pk>/*
- [GET - POST] *api/pokemons/own/*
- [PUT - PATCH - DELETE] *api/pokemons/own/<int:pk>/*
- [GET] *api/pokemons/own/party/*
- [POST] *api/pokemons/own/swap/*
- [GET] *api/regions/*
- [GET] *api/regions/<int:pk>/*
- [GET] *api/locations/*
- [GET] *api/locations/<int:pk>/*
- [GET] *api/areas/*
- [GET] *api/areas/<int:pk>/*

## Postman Collection

Postman collection file included with routes and data examples.

## License

MIT


