import os

RAIZ_APP = os.path.dirname(os.path.abspath(__file__))
# é necessário um secret_key para que a sessão da aplicação não fique acessível para qualquer um
SECRET_KEY = '*#caleum&*'
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "admin"
MYSQL_DB = "jogoteca"
MYSQL_PORT = 3306
UPLOAD_FOLDER = RAIZ_APP + '/uploads'
