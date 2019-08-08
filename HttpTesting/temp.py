import json
a = {'req': {'cno': '1623770534820512'}, 'appid': 'dp1svA1gkNt8cQMkoIv7HmD1', 'sig': '5', 'v': 2.0, 'ts': 123}
m = json.dumps(a,sort_keys=True, indent=4, ensure_ascii=False)
print(m)