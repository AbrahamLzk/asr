# -*- coding:utf-8 -*-
import os
import sys
import time
time1=time.time()

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
    if os.path.exists(str(sys.argv[1])+'\\search_result.txt'):
        os.remove(str(sys.argv[1])+'\\search_result.txt')
    with open(str(sys.argv[1])+'\\search_history.txt', "a", encoding='utf-8') as file:
        f = open(str(sys.argv[1])+'\\search.txt', mode='r', encoding='utf-8')
        file.write('搜索记录：\n')
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
            path=str(sys.argv[1])+'\\search.txt'
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
                with open(str(sys.argv[1])+'\\search_result.txt', "a", encoding='utf-8') as file:
                    file.write(result+'在第%s句：\n'%(i+1,))
                    file.write(text)
                    file.write('\n')
                    file.close()
                with open(str(sys.argv[1])+'\\search_history.txt', "a", encoding='utf-8') as file:
                    file.write(result+'在第%s句：\n'%(i+1,))
                    file.write(text)
                    file.write('\n')
                    file.close()
                #print(r)
    f.close()
    os.remove(str(sys.argv[1])+'\\search.txt')
    time2 = time.time()
    print('总共耗时：' + str(time2 - time1) + 's')
    with open(str(sys.argv[1])+'\\search_history.txt', "a", encoding='utf-8') as file:
        file.write('本次搜索结束')
        file.write('本次搜索总共耗时：' + str(time2 - time1) + 's')
        file.write('\n')
        file.close()
