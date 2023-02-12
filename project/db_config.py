from decouple import config


DB_NAME = config("DB_NAME")
DB_PASSWORD = config("DB_PASSWORD")
DB_HOST = config("DB_HOST")
DB_USER = config("DB_USER")
DB_PORT = config("DB_PORT")


db_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
