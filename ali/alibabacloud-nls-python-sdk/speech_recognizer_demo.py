# -*- coding: utf-8 -*-

"""
 * Copyright 2015 Alibaba Group Holding Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
"""

import os
import time
import threading
import ali_speech
import create_token_demo
import difflib
from ali_speech.callbacks import SpeechRecognizerCallback
from ali_speech.constant import ASRFormat
from ali_speech.constant import ASRSampleRate


class MyCallback(SpeechRecognizerCallback):
    """
    构造函数的参数没有要求，可根据需要设置添加
    示例中的name参数可作为待识别的音频文件名，用于在多线程中进行区分
    """
    def __init__(self, name='default'):
        self._name = name

    def on_started(self, message):
        print('MyCallback.OnRecognitionStarted: %s' % message)

    def on_result_changed(self, message):
        print('MyCallback.OnRecognitionResultChanged: file: %s, task_id: %s, result: %s' % (
            self._name, message['header']['task_id'], message['payload']['result']))

    def on_completed(self, message):
        #print('MyCallback.OnRecognitionCompleted: file: %s, task_id:%s, result:%s' % (
        #    self._name, message['header']['task_id'], message['payload']['result']))
        with open(os.getcwd()+'\\result0.txt', "w", encoding='utf-8') as f:
            f.write(message['payload']['result'])
            f.close
        print(message['payload']['result'])
        '''
        for r in str(message['payload']['result']):
            if str(r) != '。' and str(r) != '？' and str(r) != '！'and str(r) != '，':
                asr_result += str(r)
        print('原文结果：\n')
        print(c)
        print('识别结果：\n')
        print(asr_result)
        '''

    def on_task_failed(self, message):
        print('MyCallback.OnRecognitionTaskFailed: %s' % message)

    def on_channel_closed(self):
        print('MyCallback.OnRecognitionChannelClosed')


def process(client, appkey, token, path):
    audio_name = path
    callback = MyCallback(audio_name)
    recognizer = client.create_recognizer(callback)
    recognizer.set_appkey(appkey)
    recognizer.set_token(token)
    recognizer.set_format(ASRFormat.PCM)
    recognizer.set_sample_rate(ASRSampleRate.SAMPLE_RATE_16K)
    recognizer.set_enable_intermediate_result(False)
    recognizer.set_enable_punctuation_prediction(True)
    recognizer.set_enable_inverse_text_normalization(True)

    try:
        ret = recognizer.start()
        if ret < 0:
            return ret

        print('sending audio...')
        with open(audio_name, 'rb') as f:
            audio = f.read(3200)
            while audio:
                ret = recognizer.send(audio)
                if ret < 0:
                    break
                time.sleep(0.1)
                audio = f.read(3200)

        recognizer.stop()
    except Exception as e:
        print(e)
    finally:
        recognizer.close()

def get_equal_rate_1(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

def process_multithread(client, appkey, token, number):
    thread_list = []
    for i in range(0, number):
        thread = threading.Thread(target=process, args=(client, appkey, token))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

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

if __name__ == "__main__":
    i = 0
    sum = 0
    i_number = []
    zero_count = 0
    asr = ''
    client = ali_speech.NlsClient()
    # 设置输出日志信息的级别：DEBUG、INFO、WARNING、ERROR
    client.set_log_level('INFO')

    appkey = '4V6o1MnJiGXvWu2F'
    time_start = time.time()
    token = create_token_demo.get_token()
    #token = '0aad3fbfa84f47d3bd5a504d7bbeec27'
    with open('E:\\vad\\thchs_test.txt', 'r', encoding='utf-8-sig') as f:
        line = f.readline()
        while line:
            asr_result = ''
            a = line.split('	')[0]
            c = line.split('	')[2]
            path = a
            process(client, appkey, token, path)
            with open(os.getcwd()+'\\result0.txt', "r", encoding='utf-8') as file:
                asr = file.readline()
                file.close
            for r in str(asr):
                if str(r) != '。' and str(r) != '？' and str(r) != '！'and str(r) != '，'and str(r) != '、':
                    asr_result += str(r)
            if is_contain_number(asr_result):
                i_number.append(i+1)
                i += 1
                line = f.readline()
                continue
            print('原文结果：\n')
            print(c)
            print('识别结果：\n')
            print(asr_result)
            cer = get_equal_rate_1(asr_result.strip(), c.strip())
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
        f.close()
    time_end = time.time()
    print('总时长', time_end - time_start)
    print(i_number)
    print(zero_count)
    with open('compare_result.txt', 'w', encoding='utf-8') as f:
        f.write(str(sum/(i-len(i_number))))
        f.write('\n')
        f.write(str(time_end - time_start))
        f.write('\n')
        f.write(str(i_number))
        f.write('\n')
        f.write(str((zero_count/(i-len(i_number)))*100))

    # 多线程示例
    # process_multithread(client, appkey, token, 10)




