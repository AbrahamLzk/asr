# -*- coding: utf-8 -*-

from huaweicloud_sis.client.tts_client import TtsClient
from huaweicloud_sis.bean.tts_request import TtsRequest
from huaweicloud_sis.bean.sis_config import SisConfig
from huaweicloud_sis.exception.exceptions import ClientException
from huaweicloud_sis.exception.exceptions import ServerException
import json


def tts_example():
    """ 语音合成demo """
    ak = ''         # 参考https://support.huaweicloud.com/sdkreference-sis/sis_05_0003.html
    sk = ''         # 参考https://support.huaweicloud.com/sdkreference-sis/sis_05_0003.html
    region = ''     # region，如cn-north-1
    text = ''       # 待合成文本，不超过500字
    path = ''       # 保存路径，如D:/test.wav。 可在设置中选择不保存本地

    # step1 初始化客户端
    config = SisConfig()
    config.set_connect_timeout(5)       # 设置连接超时
    config.set_read_timeout(10)         # 设置读取超时
    # 设置代理，使用代理前一定要确保代理可用。 代理格式可为[host, port] 或 [host, port, username, password]
    # config.set_proxy(proxy)
    tts_client = TtsClient(ak, sk, region, sis_config=config)

    # step2 构造请求
    tts_request = TtsRequest(text)
    # 设置请求，所有参数均可不设置，使用默认参数
    # 设置发声人，默认xiaoyan，可参考api文档
    tts_request.set_voice_name('xiaoyan')
    # 设置采样率，默认8k
    tts_request.set_sample_rate('8k')
    # 设置音量，[-20, 20]，默认0
    tts_request.set_volume(0)
    # 设置音高, [-500, 500], 默认0
    tts_request.set_pitch_rate(0)
    # 设置音速, [-500, 500], 默认0
    tts_request.set_speech_speed(0)
    # 设置是否保存，默认False
    tts_request.set_saved(True)
    # 设置保存路径，只有设置保存，此参数才生效
    tts_request.set_saved_path(path)

    # step3 发送请求，返回结果,格式为json. 如果设置保存，可在指定路径里查看保存的音频
    result = tts_client.get_tts_response(tts_request)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    try:
        tts_example()
    except ClientException as e:
        print(e)
    except ServerException as e:
        print(e)
