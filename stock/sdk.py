import hmac
import logging
import time
import os
import environ
import requests
from pathlib import Path
import json

# load env
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, 'envs/.local'))
from pip._vendor.pyparsing import Optional
from rest_framework.response import Response

# @staticmethod
# def base_get(base_path:str='', detail_path: str='', params:Optional[dict]=None)-> Response:
#     logging.info("请求方式：GET, 请求url:  %s  , 请求参数： %s " % (base_path + detail_path, params))
#     response = requests.get(base_path + detail_path, params=params)
#     logging.info("请求方式：GET, 请求url:  %s  , 请求参数： %s , 结果：%s" % (base_path + detail_path, params, response))
#     return response


uts = int(time.time())  # 時間戳記
url = f'http://127.0.0.1:8000/item/api/list/?uts={uts}'
payload = f'GET/item/api/list/uts={uts}'
api_secret_key = env('API_SECRET')
x_stock_token = env('X_STOCK_TOKEN')
x_stock_signature = hmac.new(api_secret_key.encode(), payload.encode(), 'sha256').hexdigest()
headers = {'x-stock-token': x_stock_token,
           'x-stock-signature': x_stock_signature}
print(x_stock_signature)
response = requests.get(url=url, headers=headers)
print(response.status_code)
print(response.json())

# res = requests.get("https://nidss.cdc.gov.tw/nndss/DiseaseMap?id=19CoV")
#
# print(res.text)


# url = 'http://127.0.0.1:8000/item/api/7/detail'
# headers = {"token": "b528ca33d4681b39ed7d"}
# r = requests.get(url=url, headers=headers)
# print(r.status_code)
# print(r.json())
# "signature": "8427ecb4f757f58798fb7a6ab8c6fb97882d153d63246e4eb8839406492a3874"

# class Shiba:
#     pee_length = 10
#
#     def __init__(self, height, weight):
#         self.height = height
#         self.weight = weight
#
#     @classmethod
#     def pee(cls):
#         print("pee" + "." * cls.pee_length)
#
#
# Shiba.pee()
# # result: pee..........
#
# black_shiba = Shiba(30, 40)
# black_shiba.pee()
