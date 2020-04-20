# -*- coding: utf-8 -*-
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.asr.v20190614 import asr_client, models 
import base64
import difflib
import time

i = 0
sum = 0
i_number = []
zero_count = 0

def is_number(uchar):
    """
    判断一个unicode是否是数字
    :param uchar:
    :return:
    """
    if uchar >= u'\u0030' and uchar<=u'\u0039':
        return True
    else:
        return False

def is_contain_number(user_nick_name):
    """
    :param user_nick_name:名字
    :return: 返回名字是否包含中文，英文，数字三者。
    """
    # 名字含中文
    is_number_true_list = []
    for each in user_nick_name:
        #is_chinese_true_list.append(is_chinese(each))
        is_number_true_list.append(is_number(each))
        #is_alphabet_true_list.append(is_alphabet(each))

    if (True in is_number_true_list):
       return True
    else:
        return False

def get_equal_rate_1(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()
#通过本地语音上传方式调用    
with open('E:\\vad\\thchs_test.txt', 'r', encoding='utf-8-sig') as f:
    time_start = time.time()
    line = f.readline()
    while line:
        asr = ''
        a = line.split('	')[0]
        c = line.split('	')[2]
        path = a
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
            with open(path, 'rb') as file:
                data = file.read()
                dataLen = len(data)
                file.close()
            base64Wav = base64.b64encode(data).decode()

            #发送请求
            req = models.SentenceRecognitionRequest()
            params = {"ProjectId":0,"SubServiceType":2,"EngSerViceType":"16k","SourceType":1,"Url":"","VoiceFormat":"wav","UsrAudioKey":"session-123", "Data":base64Wav, "DataLen":dataLen}
            req._deserialize(params)
            resp = client.SentenceRecognition(req) 
            #print(resp.to_json_string())
            #print(resp.to_json_string().split('"')[3])
            for r in resp.to_json_string().split('"')[3]:
                if str(r) != '。' and str(r) != '？' and str(r) != '！'and str(r) != '，':
                    asr += str(r)
            if is_contain_number(asr):
                i_number.append(i+1)
                i += 1
                line = f.readline()
                continue
            print('原文结果：\n')
            print(c)
            print('识别结果：\n')
            print(asr)
            cer = get_equal_rate_1(asr.strip(), c.strip())
            cer = 100 - cer * 100
            print('本句字符错误率：', cer)
            if cer == 0:
                zero_count += 1
            sum += cer
            line = f.readline()
            i+=1
            if i >= 5:
                print('\n')
                print('平均字符错误率：\n', sum/(i-len(i_number)))
                break
            #windows系统使用下面一行替换上面一行
            #print(resp.to_json_string().decode('UTF-8').encode('GBK') )


        except TencentCloudSDKException as err: 
            print(err)
    f.close()
time_end = time.time()
print('总时长', time_end - time_start)
print(i_number)
print(zero_count)
<<<<<<< HEAD
with open('compare_result.txt', 'w', encoding='utf-8') as f:
    f.write(str(sum/(i-len(i_number))))
    f.write('\n')
    f.write(str(time_end - time_start))
    f.write('\n')
    f.write(str(i_number))
    f.write('\n')
    f.write(str((zero_count/(i-len(i_number)))*100))
=======
>>>>>>> origin/nlp
