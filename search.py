# -*- coding:utf-8 -*-
import pynlpir  # 引入依赖包
import os
import sys

import time
time1=time.time()

# DFA算法
class DFAFilter():
    def __init__(self):
        self.keyword_chains = {}
        self.delimit = '\x00'

    def add(self, keyword):
        keyword = keyword.lower()
        chars = keyword.strip()
        if not chars:
            return
        level = self.keyword_chains
        for i in range(len(chars)):
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def parse(self, path):
        with open(path,encoding='utf-8') as f:
            for keyword in f:
                self.add(str(keyword).strip())

    def filter(self, message, repl="*"):
        message = message.lower()
        ret = []
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        break
                else:
                    ret.append(message[start])
                    break
            else:
                ret.append(message[start])
            start += 1

        return ''.join(ret)

def strDiff(str1,str2):
    tmp = {index:val for index,val in enumerate(str1) if len(str2)<=index or (len(str2)>index and not str2[index]==val)}
    return "".join(tmp.values())

if __name__ == '__main__':
    if os.path.exists(str(sys.argv[1])+'\\search_result.txt'):
        os.remove(str(sys.argv[1])+'\\search_result.txt')
    with open(str(sys.argv[1])+'\\search_history.txt', "a", encoding='utf-8') as file:
        f = open(str(sys.argv[1])+'\\search.txt', mode='r', encoding='utf-8')
        file.write('本次搜索记录：\n')
        file.write(f.read())
        file.write('\n')
        f.close()
        file.close()
    with open(str(sys.argv[1])+'\\time_data.txt', "r", encoding='utf-8') as file:
        temp = file.readline()
        print(temp)
        file.close()
    f = open(str(sys.argv[1])+'\\result1.txt', mode='r', encoding='utf-8')
    for i in range(int(temp)):
        text = f.readline()
        if text != '':
            #gfw = DFAFilter()
            path=str(sys.argv[1])+'\\search.txt'
            gfw = DFAFilter()
            gfw.parse(path)
            result = gfw.filter(text)
            #print(result)
            if result.find('*') != -1:
                #print(result)
                text_r = strDiff(text.lower(),result)
                text_result = ''
                pynlpir.open()
                for t in pynlpir.segment(text_r, pos_tagging=False):
                    text_result += str(t)
                    text_result += '，'
                pynlpir.close()
                print(text_result+'在第%s句:'%(i+1,))
                print(text)
                with open(str(sys.argv[1])+'\\search_result.txt', "a", encoding='utf-8') as file:
                    file.write(text_result+'在第%s句：\n'%(i+1,))
                    file.write(text)
                    file.write('\n')
                    file.close()
                with open(str(sys.argv[1])+'\\search_history.txt', "a", encoding='utf-8') as file:
                    file.write(text_result+'在第%s句：\n'%(i+1,))
                    file.write(text)
                    file.write('\n')
                    file.close()
    f.close()
    os.remove(str(sys.argv[1])+'\\search.txt')
    time2 = time.time()
    print('总共耗时：' + str(time2 - time1) + 's')