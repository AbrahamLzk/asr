#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import urllib.request
import urllib.parse
import json
import hashlib
import base64
#接口地址
url ="http://ltpapi.xfyun.cn/v1/ke"
#开放平台应用ID
x_appid = "5e832769"
#开放平台应用接口秘钥
api_key = "e0d4b75ae5d94b0ea14742dbda26d900"
#语言文本
with open("result.txt",'r',encoding='UTF-8') as f:
    line = f.readline()
TEXT=line
print(TEXT)


def main():
    body = urllib.parse.urlencode({'text': TEXT}).encode('utf-8')
    param = {"type": "dependent"}
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = str(int(time.time()))
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    print(result.decode('utf-8'))
    word = ""
    for i in result:
        for w in i["data"]:
            for q in w["ke"]:
                word += q["word"]
    print(word)
    return


if __name__ == '__main__':
    main()
