# srv-engine
GraphSQL and Django Server

# Install
```
$ git clone ...srv-engine
$ cd srv-engine
$ pip install -r requirements.txt
$ cd frontend
$ npm install
$ npm run deploy
$ cd ..
$ python manage.py migrate
$ python manage.py runserver
```
Navigate to http://localhost:8000 and be happy :)

# Release state
Still on alpha (frontend been builted). Beta comming this Jan/2017

# Some notes....

The frontend initial setup uses the amazing [relay-fullstack](https://github.com/lvarayut/relay-fullstack) and [django-webpack-loader](https://github.com/owais/django-webpack-loader).