import requests
import time
import hashlib




def md5(arg):
    hs = hashlib.md5()
    hs.update(arg.encode('utf-8'))
    return hs.hexdigest()

key = "asdfuasodijfoausfnasdf"
ctime = str(time.time())
new_key = "%s|%s" %(key,ctime,) # asdfuasodijfoausfnasdf|时间戳
md5_str = md5(new_key)
# 6f800b6a11d3f9c08c77ef8f77b2d460，  # asdfuasodijfoausfnasdf|时间戳
auth_header_val = "%s|%s" %(md5_str,ctime,) # 6f800b6a11d3f9c08c77ef8f77b2d460|时间戳
print(auth_header_val)




response = requests.get('http://127.0.0.1:8000/api/test.html',headers={'auth-api':auth_header_val})
print(response.text)