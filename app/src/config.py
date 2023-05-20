import os

ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = '88092a518f2f340cfb45fa83f3e05b6968143c5992a3fbc6a5b36d336d7e669a'
ALGORITHM = 'HS256'
DATABASE_URL = 'postgresql://postgres:postgres@db:5432/postgres'

_data_folder_pieces = ['app', 'data', 'dataseti']
DATA_FOLDER_PATH = os.path.abspath(os.getcwd())
for piece in _data_folder_pieces:
    DATA_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, piece)
