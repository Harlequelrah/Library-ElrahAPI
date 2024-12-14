from harlequelrah_fastapi.authentication.authenticate import Authentication


database_username=""
database_password=""
connector = "mysql+mysqlconnector"
database_name = ""
server = ""
authentication = Authentication(
    database_username=database_username,
    database_password=database_password,
    connector=connector,
    database_name=database_name,
    server=server,
)


