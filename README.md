# PUB CRAWL POLL
#### Video Demo:  https://youtu.be/laws3P6pxqI
#### Description:

This web application allows user to create a poll by which they may vote with other people on which pub they shall go.

The application is built on the Flask framework. The communication between the application and PostgreSQL database is maintained via Psycopg database adapter.

#### Overview:

The essence of the application lies in the possibility to generate a poll based on the information available in the database, to give a vote to one of the offered options and at the same time to send other users a unique link through which they can contribute to the same poll.

New pubs can be added to the database.

### app.py

The application consists of three routes:

* **/**\
    The index view function through GET method retrieves and shows available data from the database. 
    It also checks whether there is a poll_id in session , indicating that there is a poll already running. If there is not active poll, it will generate new unique identifier for the poll.

    When the user posts data, i. e. casts a vote, the POST method will insert the vote into database and change the session["voted"] variable to True. This prevents repeated voting by the same user (however, the user may delete the session data from the browser on purpose).

    The user can be also redirected to the add.html page, or the /add route, respectively,  if clicking the **ADD PUB** button.

    The user can also initiate new poll by clicking the **NEW POLL** button. 

* **/result/\<seq>**\
    The result page namely shows the current results by querying the database.

    This is also the route that user is directed if receiving the unique link.
    If that is the case and the session["voted"] variable has initial False value, the user may vote.

    Again, the user has the option to initiate new poll.

    The user can refresh the results using the **REFRESH** button and the GET method subscribed to it.

* **/add**\
    Users can add new pub to the database through this route.

    The application checks, whether the user provided all three necessary details (name, address, web). If not, the data will not be inserted and the user will receive an error message requesting that all data be provided.

    Then it is checked, whether the given pub is not already in the database. If it is, the user is informed accordingly.

    If the above checks are passed, then the new data are inserted to the database and the user is redirected to the index page.


### /templates

All .html pages adhere to a three-section layout.

* #### **Top left section**

    This is area for any messages that the user should be aware of, be it the information on having successfully voted, or displaying error messages.

* #### **Top button section**

    In this area are any buttons, except the vote button itself.

* #### **Table section**

    In this place the table with voting button, information and votes is generated via "for loop".

    In the add.html there is the form to provide necessary details to insert new pub to database.


### styles.css

The .html pages were styled via CSS.
When deciding whether or not to take advantage of the Bootstrap framework, I came to the conclusion that in the given scenario, where the idea was to keep the application's design clean and simple, its use would be redundant.


### / helpers

I wrote three helper functions outside the main application.

* #### **csv_loader.py**
    This function was to load initial data from a .csv file into database instead of inserting them manually. In may be reused again to load new data from another file, if available.

* #### **db_conn.py**
    The role of this function is to manage database connections and queries, and to ensure that each database connection is properly closed and cleaned up.

* #### **str_generator.py**
    Function to create unique identifiers for each new poll.