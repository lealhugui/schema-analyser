# schema-analyser

Open source framework and interface for database analysis. Relation fragmentation, data consistency... you name.
Designed to be extensible, multi database, easy to use and fully dynamic.

## Dependencies

As both client and server are on this repo (will change it in the future), there are 2 separate sets of dependencies:

* Server:
  * Python 3+ (with pip for the install)
  * Any suported DB provider (currently only MySQL is fully suported)
* Client:
  * Nodejs 5+ (with npm for the install and test)

## Instalation

Download the source and:

* Server:
  * Assuming that on terminal, you are on the root of the project;
  * `$ cd app\server`
  * `$ pip install -r requirements.txt`

* Client:
  * Assuming that on terminal, you are on the root of the project;
  * `$ cd app\client`
  * `$ npm install`

## Run

As the client and server are completely decoupled, today you'll have to work on 2 terminal windows (or use some concurrent work lib)

* Server:
  * Assuming that on terminal, you are on the root of the project;
  * `$ cd app\server`
  * `$ ./manage.py runserver`

* Client:
  * Assuming that on terminal, you are on the root of the project;
  * `$ cd app\client`
  * `$ npm start`

![alt text](./app/client/public/jetbrains-logo.svg)