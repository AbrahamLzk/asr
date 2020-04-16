# -*- coding: utf-8 -*-
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.asr.v20190614 import asr_client, models 
import base64

#通过本地语音上传方式调用    

for i in range(5):
    path = 'E:\\vad\\1006964305_78675b121ee04a9fa82627a8fa92bf3c_sd\\test0chunk-%002d.wav'%(i+1)
    try: 

        #重要：<Your SecretId>、<Your SecretKey>需要替换成用户自己的账号信息
        #请参考接口说明中的使用步骤1进行获取。
        cred = credential.Credential("", "") 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "asr.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        clientProfile.signMethod = "TC3-HMAC-SHA256"  
        client = asr_client.AsrClient(cred, "ap-shanghai", clientProfile) 

        #读取文件以及base64
        with open(path, 'rb') as f:
            data = f.read()
            dataLen = len(data)
        base64Wav = base64.b64encode(data).decode()

        #发送请求
        req = models.SentenceRecognitionRequest()
        params = {"ProjectId":0,"SubServiceType":2,"EngSerViceType":"16k","SourceType":1,"Url":"","VoiceFormat":"wav","UsrAudioKey":"session-123", "Data":base64Wav, "DataLen":dataLen}
        req._deserialize(params)
        resp = client.SentenceRecognition(req) 
        print(resp.to_json_string()) 
        #windows系统使用下面一行替换上面一行
        #print(resp.to_json_string().decode('UTF-8').encode('GBK') )


    except TencentCloudSDKException as err: 
        print(err) 