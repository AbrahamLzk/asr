#-*- coding:utf-8 -*-

import sys


if __name__ == '__main__':
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
