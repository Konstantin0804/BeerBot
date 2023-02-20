from pymongo import MongoClient

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'
    }
}

API_KEY = "6056645493:AAF_wNP3RDXygUAZreqWePS90wuHUcJHNpQ"

HEADERS = {'Content-Type': 'application/json', 'Authorization': 'Basic SEVMTE9ATUVUSE9EQkVFUi5SVTpYRmt2TXJyZzRVYkZLeXhXaXBVdw=='}

DB_PASSWORD = "qwerty%5"
DB_USER = "mbot"

db = MongoClient("mongodb+srv://mbottest-z04wi.gcp.mongodb.net/test", username=DB_USER, password=DB_PASSWORD).mbot_base

