import pypyodbc as odbc
import pandas as pd
from credentials import username, password

server = 'jarbdatabase.database.windows.net'
database = 'Azure_EmployeeDB'

# Toggle: set use_aad=True to use Azure AD interactive auth (opens interactive prompt)
# When using AAD interactive, DO NOT pass UID/PWD in the connection string.
use_aad = True

if use_aad:
	# Active Directory Interactive authentication (requires ODBC Driver 18+ and internet access)
	# The driver will open an interactive sign-in window for the user account.
	connection_string = (
		'DRIVER={ODBC Driver 17 for SQL Server};'
		f'SERVER={server};DATABASE={database};ENCRYPT=yes;'
		#'Authentication=ActiveDirectoryInteractive;'
		# Optional: TrustServerCertificate=yes can help debugging TLS issues locally.
		# 'TrustServerCertificate=yes;'
	)
else:
	# Traditional SQL authentication using UID/PWD from credentials.py
	connection_string = (
		'DRIVER={ODBC Driver 18 for SQL Server};'
		f'SERVER={server};DATABASE={database};ENCRYPT=yes;'
		f'UID={username};PWD={password};'
	)

print('Using connection string:')
print(connection_string.replace(password, '***') if not use_aad else connection_string)

conn = odbc.connect(connection_string)

sql = '''
SELECT * FROM SalesLT.Customer
'''
cursor = conn.cursor()
cursor.execute(sql)
#dataset = cursor.fetchall()

#columns = [column[0] for column in cursor.description]
#df = pd.DataFrame(dataset, columns=columns)
#print(df)