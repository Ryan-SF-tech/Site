import os
import app

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "Lobovien")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg://usuario:senha@localhost:5432/usuarios")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    