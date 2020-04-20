# -*- coding: utf-8 -*-

from huaweicloud_sis.client.asr_client import AsrCustomizationClient
from huaweicloud_sis.bean.asr_request import AsrCustomShortRequest
from huaweicloud_sis.bean.asr_request import AsrCustomLongRequest
from huaweicloud_sis.exception.exceptions import ClientException
from huaweicloud_sis.exception.exceptions import ServerException
from huaweicloud_sis.utils import io_utils
from huaweicloud_sis.bean.sis_config import SisConfig
import json
import time
import difflib

# 鉴权参数
ak = 'YT9ZLDFXSIJ1OPWZVKV9'             # 参考https://support.huaweicloud.com/sdkreference-sis/sis_05_0003.html
sk = 't45PnAVQnW4ISVxidISyZzYb4bbFXmAbVnjBArb0'             # 参考https://support.huaweicloud.com/sdkreference-sis/sis_05_0003.html
region = 'cn-north-4'         # region，如cn-north-4
project_id = '0865ea9f7c00f4892f0ac0131b3a6b9e'     # 同region一一对应，参考https://support.huaweicloud.com/api-sis/sis_03_0008.html

"""
    todo 请正确填写音频格式和模型属性字符串
    1. 音频格式一定要相匹配.
         例如文件或者obs url是xx.wav, 则在一句话识别是wav格式，在录音文件识别是auto。具体参考api文档。
         例如音频是pcm格式，并且采样率为8k，则格式填写pcm8k16bit。
         如果返回audio_format is invalid 说明该文件格式不支持。具体支持哪些音频格式，需要参考api文档。
         
    2. 音频采样率要与属性字符串的采样率要匹配。
         例如格式选择pcm16k16bit，属性字符串却选择chinese_8k_common, 则会返回'audio_format' is not match model
         例如wav本身是16k采样率，属性选择chinese_8k_common, 同样会返回'audio_format' is not match model
"""

# 一句话识别参数，以音频文件的base64编码传入，1min以内音频
#path = r'E:\vad\1006964305_78675b121ee04a9fa82627a8fa92bf3c_sd\test0chunk-01.wav'                   # 文件位置, 需要具体到文件，如D:/test.wav
#path = r'E:/vad/huaweicloud-python-sdk-sis-1.1.0/data/16k16bit.wav'
path_audio_format = 'wav'      # 音频格式，如wav等，详见api文档
path_property = 'chinese_16k_common'          # language_sampleRate_domain, 如chinese_8k_common，详见api文档

# 录音文件识别参数，音频文件以obs连接方式传入（即先需要将音频传送到华为云的obs）
obs_url = ''                # 音频obs连接
obs_audio_format = ''       # 音频格式，如auto等，详见api文档
obs_property = ''           # language_sampleRate_domain, 如chinese_8k_common，详见api文档

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

def asrc_short_example(path):
    asr = ''
    """ 一句话识别示例 """
    # step1 初始化客户端
    config = SisConfig()
    config.set_connect_timeout(5)       # 设置连接超时
    config.set_read_timeout(10)         # 设置读取超时
    # 设置代理，使用代理前一定要确保代理可用。 代理格式可为[host, port] 或 [host, port, username, password]
    # config.set_proxy(proxy)
    asr_client = AsrCustomizationClient(ak, sk, region, project_id,  sis_config=config)

    # step2 构造请求
    data = io_utils.encode_file(path)
    asr_request = AsrCustomShortRequest(path_audio_format, path_property, data)
    # 所有参数均可不设置，使用默认值
    # 设置是否添加标点，yes or no，默认no
    asr_request.set_add_punc('yes')
    # 设置是否添加热词表id，没有则不填
    # asr_request.set_vocabulary_id(None)

    # step3 发送请求，返回结果,返回结果为json格式
    result = asr_client.get_short_response(asr_request)
    #print(json.dumps(result, indent=2, ensure_ascii=False))
    #print(json.dumps(result, indent=2, ensure_ascii=False).split('"')[9])
    for r in json.dumps(result, indent=2, ensure_ascii=False).split('"')[9]:
        if str(r) != '。' and str(r) != '？' and str(r) != '！'and str(r) != '，':
            asr += str(r)
    if is_contain_number(asr):
        cer = -1
        return cer
    print('原文结果：\n')
    print(c)
    print('识别结果：\n')
    print(asr)
    cer = get_equal_rate_1(asr.strip(), c.strip())
    cer = 100 - cer * 100
    print('本句字符错误率：', cer)
    return cer



def asrc_long_example():
    """ 录音文件识别示例 """
    # step1 初始化客户端
    config = SisConfig()
    config.set_connect_timeout(5)       # 设置连接超时
    config.set_read_timeout(10)         # 设置读取超时
    # 设置代理，使用代理前一定要确保代理可用。 代理格式可为[host, port] 或 [host, port, username, password]
    # config.set_proxy(proxy)
    asr_client = AsrCustomizationClient(ak, sk, region, project_id,  sis_config=config)

    # step2 构造请求
    asrc_request = AsrCustomLongRequest(obs_audio_format, obs_property, obs_url)
    # 所有参数均可不设置，使用默认值
    # 设置是否添加标点，yes or no，默认no
    asrc_request.set_add_punc('yes')
    # 设置 是否需要分析信息，True or False, 默认False。 只有need_analysis_info生效，diarization、channel、emotion、speed才会生效
    # 目前仅支持8k模型，详见api文档
    asrc_request.set_need_analysis_info(True)
    # 设置是否需要话者分离，默认True，需要need_analysis_info设置为True才生效。
    asrc_request.set_diarization(True)
    # 设置声道信息, 一般都是单声道，默认为MONO，需要need_analysis_info设置为True才生效
    asrc_request.set_channel('MONO')
    # 设置是否返回感情信息, 默认True，需要need_analysis_info设置为True才生效。
    asrc_request.set_emotion(True)
    # 设置是否需要返回语速信息，默认True，需要need_analysis_info设置为True才生效。
    asrc_request.set_speed(True)
    # 设置是否添加热词表id，没有则不填
    # asrc_request.set_vocabulary_id(None)

    # step3 发送请求，获取job_id
    job_id = asr_client.submit_job(asrc_request)

    # step4 根据job_id轮询，获取结果。
    status = 'WAITING'
    count = 0   # 每2s查询一次，尝试2000次，即4000s。如果音频很长，可适当考虑加长一些。
    while status != 'FINISHED' and count < 2000:
        print(count, ' query')
        result = asr_client.get_long_response(job_id)
        status = result['status']
        if status == 'ERROR':
            print('录音文件识别执行失败, %s' % json.dump(result))
            break
        time.sleep(2)
        count += 1
    if status != 'FINISHED':
        print('录音文件识别未在 %d 内获取结果，job_id 为%s' % (count, job_id))
    # result为json格式
    print(json.dumps(result, indent=2, ensure_ascii=False))

def get_equal_rate_1(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

if __name__ == '__main__':
    i = 0
    sum = 0
    i_number = []
    zero_count = 0
    with open('E:\\vad\\thchs_test.txt', 'r', encoding='utf-8-sig') as f:
        time_start = time.time()
        line = f.readline()
        while line:
            #asr = ''
            a = line.split('	')[0]
            c = line.split('	')[2]
            path = a
            try:
                cer = asrc_short_example(path)        # 一句话识别
                if cer == -1:
                    i_number.append(i+1)
                    i += 1
                    line = f.readline()
                    continue
                if cer == 0:
                    zero_count += 1
                sum += cer
                #asrc_long_example()         # 录音文件识别
                line = f.readline()
                i+=1
                if i == 15:
                    print('\n')
                    print('平均字符错误率：\n', sum/i)
                    break
            except ClientException as e:
                print(e)
            except ServerException as e:
                print(e)
        f.close()
    time_end = time.time()
    print('总时长', time_end - time_start)
    print(i_number)
    print(zero_count)