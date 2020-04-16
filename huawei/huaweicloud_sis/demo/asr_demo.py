# -*- coding: utf-8 -*-

from huaweicloud_sis.client.asr_client import AsrClient
from huaweicloud_sis.bean.asr_request import AsrRequest
from huaweicloud_sis.bean.sis_config import SisConfig
from huaweicloud_sis.utils import io_utils
from huaweicloud_sis.exception.exceptions import ClientException
from huaweicloud_sis.exception.exceptions import ServerException
import json


def asr_short_example():
    """ 短语音识别demo """
    ak = ''         # 参考https://support.huaweicloud.com/sdkreference-sis/sis_05_0003.html
    sk = ''         # 参考https://support.huaweicloud.com/sdkreference-sis/sis_05_0003.html
    region = ''     # region，如cn-north-1
    path = ''       # 待识别音频的本地路径，需具体到文件路径。如D:/test.wav

    # step1 初始化客户端
    config = SisConfig()
    config.set_connect_timeout(5)       # 设置连接超时
    config.set_read_timeout(10)         # 设置读取超时
    # 设置代理，使用代理前一定要确保代理可用。 代理格式可为[host, port] 或 [host, port, username, password]
    # config.set_proxy(proxy)
    asr_client = AsrClient(ak, sk, region, sis_config=config)

    # step2 构造请求
    asr_request = AsrRequest()
    # 通过data传递音频或者obs url传递音频，二选一。
    data_str = io_utils.encode_file(path)
    asr_request.set_data(data_str)
    # 或者可以通过obs url传入连接, 当两者都设置，仅data会生效。
    # asr_request.set_url(obs_url)
    # 设置采样率, 8k or 16k，默认8k
    asr_request.set_sample_rate('8k')
    # 设置音频格式，可自动识别，支持格式详见api文档
    # asr_request.set_encode_type('')

    # step3 发送请求，返回结果，为json格式
    result = asr_client.get_asr_response(asr_request)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    try:
        asr_short_example()
    except ClientException as e:
        print(e)
    except ServerException as e:
        print(e)
