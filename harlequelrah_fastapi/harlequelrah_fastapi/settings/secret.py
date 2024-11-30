from harlequelrah_fastapi.authentication.authenticate import Authentication

database_username = ""
database_password = ""
connector = ""
database_name = ""
server = ""
authentication = Authentication(
    database_username, database_password, connector, database_name, server
)
