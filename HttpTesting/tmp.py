import requests

url = "http://wechat.bioderma.net.cn/API/VendingMachine/PostOrderStatus"

querystring = {"input":"{\"OrderStatus\": 11, \"MachineCode\": 18495848, \"OrderNo\": \"201906241639578563619\", \"OpenId\": \"oRFjUjpoh-QZbtcsjOyk53W91mNg\"}"}

payload = ""
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "7afe3edf-7179-7b9c-8c75-fcd357655108"
    }

response = requests.request("POST", url, data=querystring, headers=headers)

print(response.text)