##Overview

This code connects to a redshift database, reads the tables and columns 
from the database, and writes them to a PDF file called Redshift_Tables.pdf.  Be warned, depending on your schema the resulting PDF can be very long.  In my case, with the Klaviyo instance, it is more than 32 pages long (with 8 point text).

##Notes

Before connecting to the Klaviyo Redshift database, don't forget to connect to VPN.

##Sources

I used the following sources for the overall structure / approach for connecting to the database: \
https://kb.objectrocket.com/postgresql/python-and-psycopg2-example-1053 \
https://www.blendo.co/blog/access-your-data-in-amazon-redshift-and-postgresql-with-python-and-r/

I used the following source for the SQL to return all tables & columns in the database: \
https://www.flydata.com/blog/redshift-show-tables/

I used the following source for information about creating PDFs: \
https://www.geeksforgeeks.org/convert-text-and-text-file-to-pdf-using-python/

You can find information about information_schema.tables here: \
https://www.cmi.ac.in/~madhavan/courses/databases10/mysql-5.0-reference-manual/information-schema.html#tables-table

##Database Credentials

I use a separate json file to hold my database connection credentials.  For security reasons, I do not include this json file in this Github repository.  It has the following format:
```
{
  "user": <my_user_name>,
  "password": <my_password>,
  "host": <the_host_name>,
  "port": <the_port>,
  "database": <the_database_name>
}