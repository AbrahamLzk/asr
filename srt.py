#-*- coding:utf-8 -*-
import os
import sys


if __name__ == '__main__':
    if os.path.exists(str(sys.argv[1])+'\\subtitles.srt'):
        os.remove(str(sys.argv[1])+'\\subtitles.srt')
    if os.path.exists(str(sys.argv[1])+'\\subtitles.txt'):
        os.remove(str(sys.argv[1])+'\\subtitles.txt')
    if os.path.exists(str(sys.argv[1])+'\\final.mp4'):
        os.remove(str(sys.argv[1])+'\\final.mp4')
    f0 = open(str(sys.argv[1])+'\\time_data.txt', mode='r', encoding='utf-8')
    temp = f0.readline()
    f1 = open(str(sys.argv[1])+'\\result1.txt', mode='r', encoding='utf-8')
    for i in range(int(temp)):
        t = f0.readline()
        time_start = t.split('-')[0]
        time_start = float(time_start)
        ts_point = format(time_start, '.3f')
        #print(ts_point)
        ts_point = int(float(ts_point)*1000)-(int(time_start)*1000)
        #print(str(ts_point))
        m_s, s_s = divmod(int(time_start), 60)
        h_s, m_s = divmod(m_s, 60)
        text_s = "%d:%02d:%02d,%03d" % (h_s, m_s, s_s,ts_point)
        print("%d:%02d:%02d,%03d" % (h_s, m_s, s_s,ts_point))

        time_end = t.split('-')[1]
        time_end = float(time_end)
        te_point = format(time_end, '.3f')
        te_point = int(float(te_point)*1000)-(int(time_end)*1000)
        #print(str(te_point))
        m_e, s_e = divmod(int(time_end), 60)
        h_e, m_e = divmod(m_e, 60)
        text_e = "%d:%02d:%02d,%03d" % (h_e, m_e, s_e,te_point)
        print("%d:%02d:%02d,%03d" % (h_e, m_e, s_e,te_point))

        sentence = f1.readline()
        char_1=str('，')
        count=0
        str_list0 = list(sentence)
        tem = []
        for each_char in str_list0:
            count+=1
            if each_char==char_1:
                tem.append(count-1)
                #print(each_char,count-1)
        if len(sentence) >= 25:
            if len(tem) >= 2:
                if len(tem)%2 == 0:
                    list0 = list(sentence)
                    list0.insert(tem[int((len(tem)/2)-1)]+1,'\n')
                    sentence = ''.join(list0)
                    #print(sentence)
                else:
                    list0 = list(sentence)
                    list0.insert(tem[int(((len(tem)+1)/2)-1)]+1,'\n')
                    sentence = ''.join(list0)
                    #print(sentence)        
        with open(str(sys.argv[1])+'\\subtitles.txt', "a", encoding='utf-8') as file:
            file.write(str(i+1)+'\n'+text_s)
            file.write(' --> ')
            file.write(text_e)
            file.write('\n')
            file.write(sentence)
            file.write('\n')
            file.close()

    f0.close()
    f1.close()
