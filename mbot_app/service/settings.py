import os
from dotenv import load_dotenv

load_dotenv()

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
         'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'
                                  }
         }

API_KEY = os.getenv("API_KEY")

HEADERS = {'Content-Type': 'application/json', 'Authorization': 'Basic '
                                                                'SEVMTE9ATUVUSE9EQkVFUi5SVTpYRmt2TXJyZzRVYkZLeXhXaXBVdw=='}

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USER = os.getenv("DB_USER")
DATABASE_URL = os.getenv("DB_SERVER")

TAP_URL = "https://business.untappd.com/api/v1/menus/81847?full=true"
BOTTLE_URL = "https://business.untappd.com/api/v1/menus/94668?full=true"

NEW_USER = 0
ADD_ADDRESS = 99
