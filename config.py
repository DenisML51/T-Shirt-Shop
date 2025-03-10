import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Путь к файлу SQLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Ключ сессии и т.д.
SECRET_KEY = 'some_secret_key'
