import pyodbc
connection = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-RNTE44E;DATABASE=HR-REPORTS-FINAL;Trusted_Connection=yes;')
cursor = connection.cursor()