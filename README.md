# OnlineShop
An E-Commerce Website using Flask(Python) Backend
<p>
<h2>Components of the Project :</h2>
<ul>
  <li><strong>__init__.py</strong> : The main python program to be run in order to run the server(<em>Flask App</em>). This program takes Port Number as a command line argument.</li>
  <li><strong>dbaccess.py</strong> : Python code with all the utitlity functions for accessing the <em>SQL</em> database. Uses python's inbuilt library <em>sqlite3</em> as SQL database connector. This file has been imported as <code>import dbaccess</code> inside __init__.py and all the utility functions are used thereby.</li>
  <li><strong>templates</strong> : This folder contains all the <em>Jinja2</em> templates to be rendered through the Flask App.</li>
  <li><strong>static</strong> : This folder contains the static files i.e. CSS, JavaScript, Images, etc.</li>
</ul>
</p>
<p>
<h2>Requirements :</h2>
<ul>
  <li><strong>Python</strong> (version 3.0 or above)</li>
  <li><strong>Flask</strong> : Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions.</li>
</ul>
</p>
<p>
<h2>How to run the server :</h2>
<p>On the Linux/Mac terminal or Windows Shell run the following command:<br/>
 <code>python3 __init__.py [port_number]</code><br/>
 for example to run the server at Port Number 5000 run:<br/>
 <code>python3 __init__.py 5000</code><br/>
  (make sure you have installed <em>Flask</em>, in order to run the server.)
 </p>
