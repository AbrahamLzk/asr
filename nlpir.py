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


if __name__ == '__main__':
    with open(str(sys.argv[1])+'\\time_data.txt', "r", encoding='utf-8') as file:
        temp = file.readline()
        print(temp)
        file.close()
    f = open(str(sys.argv[1])+'\\result1.txt', mode='r', encoding='utf-8')
    for i in range(temp):
        text = f.readline()
        if text != '':
            pynlpir.open()  # 打开分词器
            #print(pynlpir.segment(text, pos_tagging=False))
            with open(str(sys.argv[1])+'\\words.txt', "a", encoding='utf-8') as f:
                for t in pynlpir.segment(text, pos_tagging=False):
                    if str(t) != '，' and str(t) != '。' and str(t) != '？':
                        f.write(str(t))
                        f.write(str(','))
                f.close()
            sentence = ''
            for t in pynlpir.segment(text, pos_tagging=False):
                if str(t) != '，' and str(t) != '。' and str(t) != '？':
                    sentence += str(t)
                    sentence += ','
            pynlpir.close()
            gfw = DFAFilter()
            sensitive = ['色情','反动']
            for sen in sensitive:
                path=os.getcwd()+'\\' +sen+ '.txt'
                gfw.parse(path)
                result = gfw.filter(sentence)
                print(result)
                print('\n'+sen+'敏感词'+'，在第%s句'%(i,))
            time2 = time.time()
            print('总共耗时：' + str(time2 - time1) + 's')