# api microservice

<a href="https://heroku.com/deploy?template=https://github.com/turbonemesis/heroku-s3-sync.git">
  <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy">
</a>

This repo contains Python backend code and configuration files for Heroku. 

https://devcenter.heroku.com/articles/heroku-button

https://github.com/app-json/app.json#validating-a-manifest

Sync videos repo

## Local setup

python==3.8.10

To develop locally create `.env` file within `./src` directory and add following code to it:  
```
DEBUG=True
SECRET_KEY=<insert_secret_key_here>
ALLOWED_HOSTS=*,
```

Once container is up and running apply migrations (a one-time operation) and create superuser by executing:  
`docker ps` -> to list all running containers and retrieve id or name of running backend container  
`docker exec -it <id_or_name_of_running_container> /bin/bash` -> to enter the container  
`python manage.py migrate` -> to execute migrations  
`python manage.py createsuperuser` -> to create superuser  
`exit` -> to exit the container  

Test review app

## create db
```shell
create user polls with password 'test1234' SUPERUSER;
```
```shell
create database polls with owner polls;
```


`. venv/bin/activate` (python 3.9)`

`pip install -r requirements/dev.txt`

`cd src && python manage.py makemigrations`


https://thinkster.io/tutorials/django-json-api/authentication

https://github.com/chase2981/conduit-django/blob/09-filtering/conduit/apps/articles/serializers.py

https://django-rest-framework-json-api.readthedocs.io/en/stable/usage.html#queryparametervalidationfilter

https://medium.com/@raaj.akshar/creating-reverse-related-objects-with-django-rest-framework-b1952ddff1c

https://stackoverflow.com/questions/41394761/the-create-method-does-not-support-writable-nested-fields-by-default

2023

```shell
python manage.py createsuperuser --username chase --email chase@gfic.io
python manage.py drf_create_token chase
```

```
curl --location 'http://localhost:8000/api/auth/login/' \
--header 'Content-type: application/json' \
--data '{
      "username": "chase",
      "password": "test"
  }'
```

```shell
python manage.py dumpdata auth.user authtoken account sessions sites --indent 2 > superuser.json

```


https://testdriven.io/blog/django-rest-auth/
https://github.com/turbonemesis/django-rest-allauth
https://simpleisbetterthancomplex.com/tutorial/2018/11/22/how-to-implement-token-authentication-using-django-rest-framework.html

custom user model

https://testdriven.io/blog/django-custom-user-model/

https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

angular

https://nx.dev/getting-started/tutorials/angular-standalone-tutorial
