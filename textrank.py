# coding:utf-8

from textrank4zh import TextRank4Keyword, TextRank4Sentence
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import sys
import pynlpir

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
    f = open(str(sys.argv[1])+'\\result.txt', mode='r', encoding='utf-8')
    text = f.read()
    f.close()
    if os.path.exists(str(sys.argv[1])+'\\keywords.txt'):
        os.remove(str(sys.argv[1])+'\\keywords.txt')
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=5)
    print('关键词：')
    with open(str(sys.argv[1])+'\\keywords.txt', "a", encoding='utf-8') as f:
        for item in tr4w.get_keywords(10, word_min_len=1):
            print(item['word'], item['weight'])
            f.write(item['word'])
            f.write('    权重：')
            f.write(str(item['weight']))
            f.write('\n')

    pynlpir.open()  # 打开分词器
    #print(pynlpir.segment(text, pos_tagging=False))
    with open(str(sys.argv[1])+'\\title.txt', "a", encoding='utf-8') as file:
        for t in pynlpir.segment(str(sys.argv[2]), pos_tagging=False):
            if str(t) != '，' and str(t) != '。' and str(t) != '？':
                file.write(str(t))
                file.write(str('\n'))
        file.close()
    pynlpir.close()
    with open(str(sys.argv[1])+'\\time_data.txt', "r", encoding='utf-8') as file:
        temp = file.readline()
        print(temp)
        file.close()
    result = []
    count = []
    f = open(str(sys.argv[1])+'\\result1.txt', mode='r', encoding='utf-8')
    for i in range(int(temp)):
        text = f.readline()
        if text != '':
            path=str(sys.argv[1])+'\\title.txt'
            ah = ac_automation()
            ah.parse(path)
            r=ah.words_replace(text)
            if r.find('*') != -1:
                word = r.split('.')[1]
                word = word.split('/') 
                for s in word:
                    if s is not '':
                        if s in result:
                            count[result.index(s)] += 1
                        else:
                            result.append(s)
                            count.append(1)
    with open(str(sys.argv[1])+'\\keywords.txt', "a", encoding='utf-8') as f:
        i = 0
        f.write('\n标题“' + str(sys.argv[2]) + '”相关词在语音文本中出现次数：\n')
        for i in range(len(result)):
            print(result)
            print(count)
            f.write(result[i])
            f.write('：' + str(count[i]) + '次\n')
        f.close()
               
    #for item in tr4w.get_keywords(10, word_min_len=1):
        #print(item['word'], item['weight'])

    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source = 'no_stop_words')
    data = pd.DataFrame(data=tr4s.key_sentences)
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    plt.figure(facecolor='w')
    plt.plot(data['weight'], 'ro-', lw=2, ms=5, alpha=0.7, mec='#404040')
    plt.grid(b=True, ls=':', color='#606060')
    plt.xlabel('句子', fontsize=12)
    plt.ylabel('重要度', fontsize=12)
    plt.title('句子的重要度曲线', fontsize=15)
    #plt.show()

    key_sentences = tr4s.get_key_sentences(num=10, sentence_min_len=2)
    for sentence in key_sentences:
        print(sentence['weight'], sentence['sentence'])