from azure.identity import InteractiveBrowserCredential
import pyodbc

server = "jarbdatabase.database.windows.net"
database = "Azure_EmployeeDB"
credential = InteractiveBrowserCredential()
token = credential.get_token("https://database.windows.net/.default")

conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
)

conn = pyodbc.connect(conn_str, attrs_before={1256: token.token})  # 1256 = SQL_COPT_SS_ACCESS_TOKEN
