import pynlpir  # 引入依赖包
import os
import sys
if __name__ == '__main__':
    pynlpir.open()  # 打开分词器
    f = open(str(sys.argv[1])+'\\result.txt', mode='r', encoding='utf-8')
    text = f.read()
    f.close()
    #print(pynlpir.segment(text, pos_tagging=False))
    with open(str(sys.argv[1])+'\\words.txt', "a", encoding='utf-8') as f:
        for t in pynlpir.segment(text, pos_tagging=False):
            if str(t) != '，' and str(t) != '。' and str(t) != '？':
                f.write(str(t))
                f.write(str(','))
        f.close()
    pynlpir.close()