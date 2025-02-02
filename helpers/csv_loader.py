import psycopg2

"""This script loads the csv file with initial pubs data into the database"""


connect = psycopg2.connect(database="postgres", user="postgres", password="datadatabejs", host="localhost", port="5432")

connect.autocommit = True
cursor = connect.cursor() 

csv_copy = """COPY pubs(name, address, web, picture) FROM 'P:\Coding\CS50\cs50project\helpers\pubs.csv' DELIMITER ',' CSV HEADER;"""

cursor.execute(csv_copy)

connect.commit()
connect.close()