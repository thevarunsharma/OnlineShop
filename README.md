# OnlineShop
An E-Commerce Website using Flask(Python) Backend

## Components of the Project :
 - <strong>`__init__.py`</strong> : The main python program to be run in order to run the server(<em>Flask App</em>). This program takes Port Number as a command line argument.
 - <strong>dbaccess.py</strong> : Python code with all the utitlity functions for accessing the <em>SQL</em> database. Uses python's inbuilt library <em>sqlite3</em> as SQL database connector. This file has been imported as <code>import dbaccess</code> inside __init__.py and all the utility functions are used thereby.
 - <strong>templates</strong> : This folder contains all the <em>Jinja2</em> templates to be rendered through the Flask App.
 - <strong>static</strong> : This folder contains the static files i.e. CSS, JavaScript, Images, etc.

## Requirements :
 - <strong>Python</strong> (version 3.0 or above)
 - <strong>Flask</strong> : Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions.

## How to run the server :
First set the environment variable by running the following command (once for a terminal session):
 - On Linux/MacOS
 ```
 $ export FLASK_APP=OnlineShop
 ```
 - On Windows
 ```
 $ set FLASK_APP=OnlineShop
 ```
 To run the server execute the following command, each time:<br/>
 ```
 $ flask run
 ```
 (make sure you have installed <em>Flask</em>, in order to run the server.)<br/>
 Now the server is running at `http://localhost:5000`
