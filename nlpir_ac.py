# -*- coding:utf-8 -*-
import os
import sys
import time
import pynlpir  # 引入依赖包


# AC自动机算法
class node(object):
    def __init__(self):
        self.next = {}
        self.fail = None
        self.isWord = False
        self.word = ""

class ac_automation(object):

    def __init__(self):
        self.root = node()

    # 添加敏感词函数
    def addword(self, word):
        temp_root = self.root
        for char in word:
            if char not in temp_root.next:
                temp_root.next[char] = node()
            temp_root = temp_root.next[char]
        temp_root.isWord = True
        temp_root.word = word

    # 失败指针函数
    def make_fail(self):
        temp_que = []
        temp_que.append(self.root)
        while len(temp_que) != 0:
            temp = temp_que.pop(0)
            p = None
            for key,value in temp.next.item():
                if temp == self.root:
                    temp.next[key].fail = self.root
                else:
                    p = temp.fail
                    while p is not None:
                        if key in p.next:
                            temp.next[key].fail = p.fail
                            break
                        p = p.fail
                    if p is None:
                        temp.next[key].fail = self.root
                temp_que.append(temp.next[key])

    # 查找敏感词函数
    def search(self, content):
        p = self.root
        result = []
        currentposition = 0

        while currentposition < len(content):
            word = content[currentposition]
            while word in p.next == False and p != self.root:
                p = p.fail

            if word in p.next:
                p = p.next[word]
            else:
                p = self.root

            if p.isWord:
                result.append(p.word)
                p = self.root
            currentposition += 1
        #print(result)
        return result

    # 加载敏感词库函数
    def parse(self, path):
        with open(path,encoding='utf-8') as f:
            for keyword in f:
                self.addword(str(keyword).strip())

    # 敏感词替换函数
    def words_replace(self, text):
        """
        :param ah: AC自动机
        :param text: 文本
        :return: 过滤敏感词之后的文本
        """
        result = list(set(self.search(text)))
        t = ''
        for x in result:
            #print(x)
            m = text.replace(x, '*' * len(x))
            text = m
            t += x
            t += '/'
        text = text + '.' + t
        return text


if __name__ == '__main__':
    if os.path.exists(str(sys.argv[1])+'\\sen_words.txt'):
        os.remove(str(sys.argv[1])+'\\sen_words.txt')
    if os.path.exists(str(sys.argv[1])+'\\words.txt'):
        os.remove(str(sys.argv[1])+'\\words.txt')
    with open(str(sys.argv[1])+'\\time_data.txt', "r", encoding='utf-8') as file:
        temp = file.readline()
        print(temp)
        file.close()
    f = open(str(sys.argv[1])+'\\result1.txt', mode='r', encoding='utf-8')
    for i in range(int(temp)):
        text = f.readline()
        if text != '':
            pynlpir.open()  # 打开分词器
            #print(pynlpir.segment(text, pos_tagging=False))
            with open(str(sys.argv[1])+'\\words.txt', "a", encoding='utf-8') as file:
                for t in pynlpir.segment(text, pos_tagging=False):
                    if str(t) != '，' and str(t) != '。' and str(t) != '？':
                        file.write(str(t))
                        file.write(str(','))
                file.write('\n')
                file.close()
            pynlpir.close()
            time1=time.time()
            sensitive = ['色情','反动','暴恐','民生','贪腐','其他']
            for sen in sensitive:
                path=os.getcwd()+'\\' +sen+ '.txt'
                ah = ac_automation()
                ah.parse(path)
                r=ah.words_replace(text)
                if r.find('*') != -1:
                    word = r.split('.')[1]
                    word = word.split('/')
                    result = ''
                    for s in word:
                        result += s
                        result += ' '
                    result.strip()
                    with open(str(sys.argv[1])+'\\sen_words.txt', "a", encoding='utf-8') as file:
                        file.write(result)
                        file.write(sen+'敏感词'+'，在第%s句：\n'%(i+1,))
                        file.write(text)
                        file.write('\n')
                        file.close()
                #print(r)

    f.close()
    time2 = time.time()
    print('总共耗时：' + str(time2 - time1) + 's')