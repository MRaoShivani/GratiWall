import sqlite3
from flask import g

import os

#DATABASE = 'C:\Users\AHLocal\Documents\GratiWall\gratitude_db.db'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
print(f'based_dir = {BASE_DIR}')

class Config:
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(BASE_DIR,"gratitude_db.db")
    )
    print(f'SQLALCHEMY_DATABASE_URI= {SQLALCHEMY_DATABASE_URI}')

    SQLALCHEMY_TRACK_MODIFICATIONs = False

