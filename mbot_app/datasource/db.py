from pymongo import MongoClient

from service.settings import (DATABASE_URL, DB_PASSWORD, DB_USER)

db = MongoClient(DATABASE_URL, username=DB_USER, password=DB_PASSWORD).mbot_base
