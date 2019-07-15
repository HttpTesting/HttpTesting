import requests
from HttpTesting.base.base_config import BaseConfig
import json
from HttpTesting.library.scripts import retry
from requests.exceptions import (
    RequestException, 
    HTTPError
    )

class HttpWebRequest(object):

    
    payload = {
        "id":"b9b0e8e985a911e894a01c3947952e7e",
        "secret":"71ee217e2f1bdfcc"
        }

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }

    def __init__(self, url='/xxx/xxxx'):
        self.baseUrl  = BaseConfig.base_url()
        self.url = '{}{}'.format(self.baseUrl, str(url).strip())

    def get(self, **kwargs):
        """"""
        try:
            res =requests.request("GET", self.url, **kwargs)

        except HTTPError as ex:
            return {"errcode": 9002, "errmsg": str(ex.message)}

        if res.status_code ==200:
            res = res.json()
        else:
            return {"errcode": 9001, "errmsg": str(res)}


    # post请求
    @retry(reNum=3)
    def post(self, **kwargs):
        try:
            res = requests.request("POST",self.url, **kwargs)
        except HTTPError as ex:
            return {"errcode": 9002, "errmsg": str(ex.message)}

        if res.status_code ==200:
            res = res.json()
        else:
            return {"errcode": 9001, "errmsg": str(res)}


# if __name__ == "__main__":
#     print json.dumps(HttpWebRequest().post())\
#         .decode('unicode-escape')


