import psycopg2  # pip install psycopg2-binary
import numpy as np  # pip install numpy
from fpdf import FPDF  # pip install FPDF
import json


# Function that adds information about a table to the PDF file.
def add_output_to_pdf(output_schema_str, output_table_str, output_column_str):
    # pdf.cell takes the following arguments:
    #   <cell width>
    #   <cell height>
    #   <string to print>
    #   border=<value> (default = 0, which is no border)
    #   ln=<position> (1 = to the beginning of next line)
    #   align=<alignment> (L = left align)
    #   fill=<boolean>
    #   link=<URL>
    pdf.cell(200, 4, txt=output_schema_str, ln=1, align='L')
    pdf.cell(200, 4, txt=output_table_str, ln=1, align='L')
    pdf.cell(200, 4, txt=output_column_str, ln=1, align='L')


# Function to convert the contents of a list into a string, separated by commas.
# By default, the query will return a list of tuples:
#   [('klaviyo_account_id',), ('cycle_end_date',), ('cycle_start_date',)]
# We want:
#   klaviyo_account_id, cycle_end_date, cycle_start_date
def response_to_output(response_to_convert):
    strl = ""
    i = 0
    length = len(response_to_convert)
    if length != 0:
        tuple_to_convert = response_to_convert[i]
        strl = str(tuple_to_convert[0])
        i += 1
        while i < length:
            tuple_to_convert = response_to_convert[i]
            strl = strl + ", " + str(tuple_to_convert[0])
            i += 1
    return strl


pdf = FPDF()
pdf.add_page()
pdf.set_font("Courier", size=8)

# Read the database credentials from a separate file (that is not included in
# this repository).  See README.md for more information.
f = open('credentials.json')
db_credentials = json.load(f)

# Wrap this in a function that will also handle any errors.
try:
    connection = psycopg2.connect(
        user=db_credentials['user'],
        password=db_credentials['password'],
        host=db_credentials['host'],
        port=db_credentials['port'],
        database=db_credentials['database']
    )

    cursor = connection.cursor()

    # information_schema.tables is a table that holds information about the tables in a database.
    # This table has 21 columns, including:
    #   0: TABLE_CATALOG
    #   1: TABLE_SCHEMA
    #   2: TABLE_NAME
    #   ...
    #   21: TABLE_COMMENT
    # This selects all columns from the information_schema.tables table, and sorts them by the
    # values in the table_schema column.
    cursor.execute("SELECT * FROM information_schema.tables ORDER BY table_schema;")
    data = np.array(cursor.fetchall())

    # Assign the initial table schema to the value of row 0, column 1 of the table.  Remember
    # that column 1 is TABLE_SCHEMA.  We assign this out here because we want to treat the
    # first table in a schema differently when printing to the PDF.
    table_schema = str(data[0, 1])
    # Iterate through each row in the table (information_schema.tables).
    for i in range(0, len(data)):
        if (i != 0) and (table_schema == str(data[i, 1])):
            # If we're not working with the first table in a schema (remember, the tables are
            # sorted by schema name)...
            # Assign table_schema to the value of column 1 of the table.  Remember that
            # column 1 is TABLE_SCHEMA.
            # table_schema = str(data[i, 1])
            # There's no need to repeat the schema name.
            schema_output_str = '\t\t\t'

            # Assign table_name to the value of column 2 of the table.  Remember that
            # column 2 is TABLE_NAME.
            table_name = str(data[i, 2])
            # Assign table_comments to the value of column -1 of the table (that is,
            # the last column).  Remember that the last column is TABLE_COMMENT.
            table_comments = str(data[i, -1])
            table_output_str = f"{schema_output_str} Table: {table_name} \t\t\t Comments: {table_comments}"

            # Get the column data for that table...
            sql_query_string = f"SELECT column_name FROM information_schema.columns WHERE TABLE_NAME = '{table_name}';"
            print(table_name)
            cursor.execute(sql_query_string)
            column_info = cursor.fetchall()
            column_str = response_to_output(column_info)
            column_output_str = f"\t\t\t\t\t\t Columns: {column_str}"

            # Add information about this table to the PDF file.
            add_output_to_pdf(schema_output_str, table_output_str, column_output_str)
        else:
            # If we are working with the first table in a schema...
            # Assign table_schema to the value of column 1 of the table.  Remember that
            # column 1 is TABLE_SCHEMA.
            table_schema = str(data[i, 1])
            schema_output_str = f"Schema: {table_schema}"

            # Assign table_name to the value of column 2 of the table.  Remember that
            # column 2 is TABLE_NAME.
            table_name = str(data[i, 2])
            # Assign table_comments to the value of column -1 of the table (that is,
            # the last column).  Remember that the last column is TABLE_COMMENT.
            table_comments = str(data[i, -1])
            table_output_str = f"\t\t\t Table: {table_name} \t\t\t Comments: {table_comments}"

            # Now let's get the column data for that table.
            sql_query_string = f"SELECT column_name FROM information_schema.columns WHERE TABLE_NAME = '{table_name}';"
            print(table_name)
            cursor.execute(sql_query_string)
            column_info = cursor.fetchall()
            column_str = response_to_output(column_info)
            column_output_str = f"\t\t\t\t\t\t Columns: {column_str}"

            # Add information about this table to the PDF file.
            add_output_to_pdf(schema_output_str, table_output_str, column_output_str)

except(Exception, psycopg2.Error) as error:
    print("Error connecting to database", error)
    connection = None

finally:
    if connection is not None:
        cursor.close()
        connection.close()
        print("Database connection now closed")
    f.close()

# Save the pdf with name Redshift_Tables.pdf
pdf.output("Redshift_Tables.pdf")
