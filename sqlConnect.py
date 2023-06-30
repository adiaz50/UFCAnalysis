import sqlalchemy
from openpyxl.workbook import Workbook
import pandas as pd
import pyodbc as odbccon
import datetime

# conn = odbccon.connect("Driver={ODBC Driver 17 for SQL Server};"
#             "Server=MSI\SQLEXPRESS01;"
#             "Database=UFCData;"
#             "Trusted_Connection=yes;")

# cursor = conn.cursor()

engine = sqlalchemy.create_engine('mssql+pyodbc://MSI\SQLEXPRESS01/UFCData?driver=ODBC Driver 17 for SQL Server')

d = [
    (26, datetime.datetime(2010, 10, 18), "X", 27.5, True),
    (42, datetime.datetime(2010, 10, 19), "Y", -12.5, False),
    (63, datetime.datetime(2010, 10, 20), "Z", 5.73, True),
]
c = ["id", "Date", "Col_1", "Col_2", "Col_3"]
data = pd.DataFrame(d, columns=c)



data.to_sql("DATATEST2", engine)
# cursor.execute('Create Table UFCTest1 (column1 string)) Bulk INSERT UFCTEST1 FROM "C:\Users\Axel\Documents\DataCleaning\UFC\output.xlsx"')
# cursor.execute('Select * from covidDeaths')
# for i in cursor:
#     print(i)

