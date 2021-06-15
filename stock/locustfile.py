import hmac
import json
import os
from pathlib import Path

import environ

from locust import HttpUser, TaskSet, task, between
import time

# load env
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, 'envs/.local'))

uts = int(time.time())
api_secret = env('API_SECRET')
# host = 'http:127.0.0.1:8000'
api_url = f'/item/api/list/?uts={uts}'
x_stock_token = env('X_STOCK_TOKEN')
payload = f'GET/item/api/list/uts={uts}'
x_stock_signature = hmac.new(api_secret.encode(), payload.encode(), 'sha256').hexdigest()


def auth_header():
    return {'x-stock-token': x_stock_token, 'x-stock-signature': x_stock_signature}


# 任務類
class WebsiteTasks(TaskSet):
    @task
    def on_start(self):
        self.tokenInfo = None
        headers = auth_header()
        response = self.client.request(method="GET", url=api_url, headers=headers)
        if response.status_code == 200:
            self.tokenInfo = json.loads(response.content)


class WebsiteUser(HttpUser):
    tasks = [WebsiteTasks]
    # host = host
    wait_time = between(0.5, 10)

# locust -f locustfile.py --host http://127.0.0.1:8000 --web-host 127.0.0.1 啟動蝗蟲指令


# uts = int(time.time())  # 時間戳記
# url = f'http://127.0.0.1:8000/item/api/list/?uts={uts}'
# payload = f'GET/item/api/list/uts={uts}'
# api_secret_key = '50fOE3yM3UCgfiBBZiJwZthentA'
# x_stock_signature = hmac.new(api_secret_key.encode(), payload.encode(), 'sha256').hexdigest()
# headers = {'x-stock-token': '5c6dd3ce9022fd807d50',
#            'x-stock-signature': x_stock_signature}
# print(x_stock_signature)
# response = requests.get(url=url, headers=headers)

# print('LOGIN RESULT:', response.status_code, response.content)

# def dummy_test(self):
#     if self.tokenInfo is not None:
#         token = self.tokenInfo['token']
#         headers = auth_header()
#         headers['Authorization'] = 'Bearer' + token
#         response = self.client.request(method='GET', url=api_url, headers=headers)
#         print('API RESULT:', response.status_code, response.content)
