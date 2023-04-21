from sqlalchemy import create_engine

config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'newuser',
    'password': 'password2',
    'database': 'AniSong'
}

db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')

SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
