CMSC 461 Group Project
Fall 2016
GSA/SOAP DB
---------------------------------------------------

Group Members:
Tristan Adams
Dean Fleming
Jack Gordon
Justus Jackson
Joseph Peterson

Our implementation of the project uses Python, Bottle, and SQLite to display a simple web application for accessing the SOAP database. Supported functions are running SELECT, DELETE, and INSERT queries; clearing all the tables; and loading .csv files - as requested in the project description.

How to start up the web app:
1.	Run controller.py
2.	Open localhost:8080 in a web browser

Project Directory
---------------------------------------------------
csv (folder) - This folder is where CSV files are saved after uploading into the webpage/database.

web (folder) - This folder contains the html used to display the web app and interface with Bottle, in addition to a GSA logo image and images of the ER diagram and relational schema.

bottle.py - This is the Python code that enables use of Bottle (unmodified).

controller.py - This is our web app engine that handles running SQL queries on the database via SQLite and locally serving the web application via Bottle.

soap.sql - This is the sql script used to generate the SQLite database.

---------------------------------------------------
***Query that calculates the total square footage managed by each office:
SELECT office.name, SUM(rental.squareFt) AS sqFt FROM rental NATURAL JOIN office GROUP BY office.name;

A good sample query:
SELECT t.rental_ID,t.name,agency.name FROM (SELECT * FROM rental NATURAL JOIN agreement) AS t JOIN agency ON t.agency_ID=agency.agency_ID;