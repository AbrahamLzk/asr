# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
from numpy.random import randn
import matplotlib.pyplot as plt
i_num = []
num_list0 = []
num_list1 = []
num_list2 = []
if os.system('python E:\\vad\\baidu\\asr_json.py') == 0:
    with open('compare_result.txt', 'r', encoding='UTF-8') as f:
        cer0 = f.readline()
        time0 = f.readline()
        i_number0 = f.readline()
        zero_count0 = f.readline()
        f.close()
num_list0.append(float(cer0))
num_list1.append(float(time0))
num_list2.append(float(zero_count0))

if os.system('python E:\\vad\\tencent\\asr_tencent.py') == 0:
    with open('compare_result.txt', 'r', encoding='UTF-8') as f:
        cer1 = f.readline()
        time1 = f.readline()
        i_number1 = f.readline()
        zero_count1 = f.readline()
        f.close()
num_list0.append(float(cer1))
num_list1.append(float(time1))
num_list2.append(float(zero_count1))

if os.system('python E:\\vad\\xunfei\\iat_ws_python3.py') == 0:
    with open('compare_result.txt', 'r', encoding='UTF-8') as f:
        cer2 = f.readline()
        time2 = f.readline()
        i_number2 = f.readline()
        zero_count2 = f.readline()
        f.close()
num_list0.append(float(cer2))
num_list1.append(float(time2))
num_list2.append(float(zero_count2))

if os.system('python E:\\vad\\ali\\alibabacloud-nls-python-sdk\\speech_recognizer_demo.py') == 0:
    with open('compare_result.txt', 'r', encoding='UTF-8') as f:
        cer3 = f.readline()
        time3 = f.readline()
        i_number3 = f.readline()
        zero_count3 = f.readline()
        f.close()
num_list0.append(float(cer3))
num_list1.append(float(time3))
num_list2.append(float(zero_count3))

with open('compare_result.txt', 'w', encoding='UTF-8') as f:
    f.write(i_number0)

if os.system('python E:\\vad\\huawei\\asr_customization_demo.py') == 0:
    with open('compare_result.txt', 'r', encoding='UTF-8') as f:
        cer4 = f.readline()
        time4 = f.readline()
        i_number4 = f.readline()
        zero_count4 = f.readline()
        f.close()
num_list0.append(float(cer4))
num_list1.append(float(time4))
num_list2.append(float(zero_count4))

print('CER(%):\nbaidu:', cer0, ';tencent:', cer1, ';xunfei', cer2, ';ali', cer3, ';huawei', cer4)
print('time(s):\nbaidu', time0, ';tencent', time1, ';xunfei', time2, ';ali', time3, ';huawei', time4)
print('correct_rate(%):\nbaidu', zero_count0, ';tencent', zero_count1, ';xunfei', zero_count2, ';ali', zero_count3, ';huawei', zero_count4)
fig = plt.figure()
ax = fig.add_subplot(111) 
x =list(range(len(num_list0))) 
#print(x) 
total_width, n = 0.5, 2  
width = total_width / n 
#print(width) 
a = plt.bar(x, num_list0, width=width, label='CER(%)',fc = 'y')  
for i in range(len(x)):  
    x[i] = x[i] + width  
b = plt.bar(x, num_list1, width=width, label='time(s)',fc = 'b')
for i in range(len(x)):  
    x[i] = x[i] + width 
c = plt.bar(x, num_list2, width=width, label='correct_rate(%)',fc = 'r')  
for rect in a:
    height = round(rect.get_height(), 2)
    #print(str(height))
    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=8, ha='center', va='bottom')
for rect in b:
    height = round(rect.get_height(), 2)
    #print(str(height))
    plt.text(rect.get_x() + rect.get_width() / 3, height, str(height), size=8, ha='center', va='bottom')
for rect in c:
    height = round(rect.get_height(), 2)
    #print(str(height))
    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=8, ha='center', va='bottom')
ax.set_xticklabels(['','baidu','tencent','xunfei','ali','huawei'],rotation=45,fontsize=  'small')
plt.title('语音识别接口性能测试')
plt.legend()  
plt.show()