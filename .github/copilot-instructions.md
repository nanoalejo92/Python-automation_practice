## Quick repository overview

This is a small Python automation repo focused on CSV processing and a simple Azure SQL interaction. Primary entry points:

- `sql_serverconnection.py` — connects to a SQL Server (Azure SQL) using `pypyodbc`, runs a query, and demonstrates cursor usage.
- `credentials.py` — stores `username` and `password` used by `sql_serverconnection.py` (local/dev convenience; NOT secure).
- `read_csvfile.ipynb` and `sql_table_csv_file.ipynb` — notebooks used for interactive exploration and CSV <> DB flows.

## Big-picture architecture and data flow

- Data source: CSV files in the repo (e.g. `employee_data.csv`). Notebooks and scripts load CSVs with `pandas`.
- DB integration: `sql_serverconnection.py` builds an ODBC connection string and runs a SELECT against `SalesLT.Customer`.
- Purpose: small automation experiments — scripts are standalone (no package structure). Expect to run them directly with `python` or from notebooks.

## Project-specific conventions and important patterns

- Credentials are stored in `credentials.py` as simple variables (`username`, `password`). When modifying, keep this local-only — do not commit secrets.
- ODBC connection is created like:

```py
server = 'jarbdatabase.database.windows.net'
database = 'Azure_EmployeeDB'
connection_string = (
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;'
    'UID='+username+';PWD='+password
)
``` 

- Dependencies used in repo: `pypyodbc`, `pandas`. If you run scripts, ensure these are installed in the Python environment.

## How to run & debug (developer workflows)

- Run the simple DB script locally:

```powershell
python sql_serverconnection.py
```

- Install dependencies (example):

```powershell
python -m pip install pandas pypyodbc
```

- Debugging tips for DB connections:
  - Print the non-secret parts of `connection_string` (e.g. server, database, UID) before connecting.
  - Catch and log exceptions from `odbc.connect()` to capture driver error text.
  - Confirm network access: Azure SQL requires port 1433 and the server's firewall to allow your client IP.

## Known pitfall seen in this repo (actionable)

- Error: "Cannot open server \"outlook.com\" requested by the login. The login failed." — this occurs in this repo because `credentials.py` contains an email-style username:

```py
username = 'johan.robelto.bayona@outlook.com'
```

In Azure SQL SQL-auth, the server/login parsing expects either a SQL user created on the server (often in the form `user@servername`) or use an Azure AD authentication flow. If you pass an email address whose domain is not the SQL server, the server tries to locate `outlook.com` as the requested server and fails.

Fix options (choose one depending on your setup):

1. Use a SQL-auth user that belongs to the server. Example: if you created a user `myuser` on `jarbdatabase`, use `myuser` or `myuser@jarbdatabase` as the `UID`.
2. If you intend to authenticate with Azure AD (an Outlook/Microsoft account), switch the connection to an AAD auth method (e.g., `Authentication=ActiveDirectoryInteractive` or use MSAL) rather than plain UID/PWD. ODBC Driver 18 supports Azure AD auth modes.
3. For quick local debugging only, create a SQL login on the Azure SQL server and use those credentials (sa-like user).

Also verify these items:
- `server` is correct: `jarbdatabase.database.windows.net` (as used in `sql_serverconnection.py`).
- Driver is installed: "ODBC Driver 18 for SQL Server".
- Firewall and port 1433 allow the client IP.

## Files to update when changing connection behavior

- `credentials.py` — change username/password source (or replace with environment variable loader).
- `sql_serverconnection.py` — connection_string builder and parameters (e.g., add `TrustServerCertificate=yes` temporarily to bypass TLS issues while debugging, or add `Authentication=ActiveDirectoryInteractive` for AAD flows).

## Security note

- This repo currently stores credentials in plaintext in `credentials.py`. For production or shared repos, move secrets to environment variables or a secrets store (Azure Key Vault, `.env` with `python-dotenv`, etc.).

## What to do next / how I can help

- I can:
  - Remove the committed `credentials.py` and add a `.env` loader.
  - Update `sql_serverconnection.py` to support an AAD authentication flow (example using MSAL) if you need to use an Outlook/Azure AD account.
  - Add a small README or `requirements.txt` listing the dependencies.

If any of the assumptions above are incorrect (for example, a different SQL server name or you intentionally use an Outlook account for SQL auth), tell me and I'll update the instructions and the code accordingly.
