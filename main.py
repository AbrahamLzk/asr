# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
import tkinter.filedialog
import tkinter.messagebox
import stat
import shutil
#from iat_ws_python3 import *
from tkinter import *


import vlc


class Production_Tool(Frame):
    def __init__(self, master):

        # 视频和音频区域
        frame = Frame(master)
        frame.pack(side=RIGHT, fill=BOTH, expand=YES)

        frame1 = Frame(master)
        # frame1 = Frame(master,bg="gray")
        frame1.pack(side=LEFT, fill=BOTH, expand=YES)

        self.pwd = os.getcwd()

        self.pauseFlag = False

        # 获取PC机本地IP
        self.local_ip = "192.168.1.5"

        """
        播放画面区域 bg="Gainsboro"
        """

        self.lab_tmp = Label(frame1, text="", width=1, fg="black", font=("宋体", 12, "bold"), justify="left")
        self.lab_tmp.grid(row=0, column=0, rowspan=1, sticky=W)

        self.show_video = Text(frame1, width=150, height=40, wrap=WORD, bd=4, bg="white")
        self.show_video.grid(row=15, column=1, rowspan=1, sticky=W)
        self.show_video.insert(END, "等待视频播放")
        self.media = vlc.MediaPlayer()

        self.file_path = ''
        self.p_path = ''

        if "Windows" == platform.system():
            # 主子设备视频播放
            self.media.set_hwnd(self.show_video.winfo_id())
        else:
            print("错误", "不支持此平台！")
            exit(-1)

        # self.bt_play = Button(frame1, text="播  放", command=lambda: self.play_media(button=self.media), bd=3,
        #                       width=8)
        # self.bt_play.grid(row=15, column=2, rowspan=2, sticky=N)
        #
        # self.bt_pause = Button(frame1, text="暂  停", command=lambda: self.pause_media(button=self.media), bd=3,
        #                       width=8)
        # self.bt_pause.grid(row=15, column=2, rowspan=2, sticky=N)
        #
        # self.bt_open = Button(frame1, text="打开文件", command=lambda: self.fn_open_file(), bd=3,
        #                       width=8)
        # self.bt_open.grid(row=15, column=2, rowspan=2, sticky=E)
        #
        # self.bt_stop = Button(frame1, text="停  止", command=lambda: self.stop_play_vlc(), bd=3,
        #                       width=8)
        # self.bt_stop.grid(row=15, column=2, rowspan=2, sticky=S)

        self.bt_play = Label(frame, text="")
        self.bt_play.grid(row=0, sticky=W)
        self.bt_play = Button(frame, text="打开文件", command=lambda: self.fn_open_file(), bd=3,
                              width=30)
        self.bt_play.grid(row=1, column=2, rowspan=1, sticky=W)

        self.bt_pause = Button(frame, text="视频暂停", command=lambda: self.pause_media(button=self.media), bd=3,
                               width=30)
        self.bt_pause.grid(row=2, column=2, rowspan=1, sticky=W)

        self.bt_stop = Button(frame, text="视频停止", command=lambda: self.stop_play_vlc(), bd=3,
                              width=30)
        self.bt_stop.grid(row=3, column=2, rowspan=1, sticky=W)

        self.bt_open = Button(frame, text="语音分析", command=lambda: self.speech(self.file_path), bd=3,
                              width=30)
        self.bt_open.grid(row=4, column=2, rowspan=1, sticky=W)

        self.bt_stop = Button(frame, text="获取知识点", command=lambda: self.textrank(self.p_path), bd=3,
                              width=30)
        self.bt_stop.grid(row=5, column=2, rowspan=1, sticky=W)

        self.bt_stop = Button(frame, text="加入字幕", command=lambda: self.subtitles(self.p_path,self.file_path), bd=3,
                              width=30)
        self.bt_stop.grid(row=6, column=2, rowspan=1, sticky=W)

        self.bt_stop = Button(frame, text="敏感词审核", command=lambda: self.nlpir(self.p_path), bd=3,
                              width=30)
        self.bt_stop.grid(row=7, column=2, rowspan=1, sticky=W)

        self.text = Text(frame, width=30, height=23, wrap=WORD, bd=4, bg="white")
        self.text.grid(row=8, column=2, rowspan=1, sticky=W)
        self.text.insert(END, "请选择视频文件")

    def play_media(self, button=None, f_path=None):
        if button and f_path:
            print("button: %s, filepath: %s" % (button, f_path))
            button.set_mrl(f_path)
            button.play()
            self.show_video.delete(0.0, END)
            self.show_video.insert(END, "等待视频播放")

    def pause_media(self, button=None):
        self.pauseFlag = not self.pauseFlag
        if self.pauseFlag:
            self.bt_pause["text"] = "继  续"
            button.pause()
        else:
            self.bt_pause["text"] = "暂  停"
            button.set_pause(0)

    def fn_open_file(self):
        try:
            f = tkinter.filedialog.askopenfilename(title="打开视频文件",
                                                   filetypes=[("视频文件", ".mp4 .mp3"), ("All", "*")])
            self.text.delete(1.0,END)
            self.text.insert(1.0, "视频路径:\n"+f)
        except:
            self.show_video.insert(END, "\n文件打开失败")
            return False
        print("File: %s" % f)
        self.file_path = f
        self.play_media(button=self.media, f_path=f)

    def speech(self, f=None):
        if f is not '':
            self.text.delete(1.0,END)
            self.text.insert(0.0, "正在进行语音分析，请勿关闭")
            root.update()
            name = f.split('/')[-1]
            name = name.split('.')[0]
            print(name)
            if not os.path.exists(os.getcwd()+'\\'+name):
                os.mkdir(name)
                print('mk_new_succeed')
            else:
                filePath = os.getcwd()+'\\'+name
                for fileList in os.walk(filePath):
                    for n in fileList[2]:
                        os.chmod(os.path.join(fileList[0],n), stat.S_IWRITE)
                        os.remove(os.path.join(fileList[0],n))
                shutil.rmtree(filePath)
                os.mkdir(name)
                print('mk_succeed')
            p = os.getcwd()+'\\'+name
            self.p_path = p
            if os.system("D:\\ffmpeg\\bin\\ffmpeg -i %s -vn -ar 16000 -ac 1 -f wav %s\\test0.wav"%(f,p)) == 0:
                self.text.insert(END, "\n音频提取成功，音频位置:\n"+p+"\\test0.wav")
                root.update()
            else:
                self.text.insert(END, "\n音频提取失败，请重试")
                root.update()
                return
            if os.system("python vad.py %s"%(p,)) == 0:
                self.text.insert(END, "\n音频分割成功，路径:\n"+p)
                root.update()
            else:
                self.text.insert(END, "\n音频分割失败，请重试")
                root.update()
                return
            if os.system("python iat_ws_python3.py %s"%(p,)) == 0:
                #self.text.delete(END)
                self.text.insert(END, "\n语音识别成功，文档位置:\n"+p+"\\result.txt")
                result = ''
                with open(p+'\\result.txt', "r", encoding='utf-8') as file:
                    result = file.readlines()
                    file.close()
                tkinter.messagebox.showinfo('语音识别结果', result)
            else:
                #self.text.delete(END)
                self.text.insert(END, "\n语音识别分割失败，请重试")
                root.update()
                return
            '''
            def task():
                solve = tkinter.after(50000,task)
                command = ''
                if os.path.exists(os.getcwd()+'\\command.txt'):
                    with open(os.getcwd()+'\\command.txt', "r", encoding='utf-8') as file:
                        command = file.readline()
                    if command == 'ASR_Done':
                        tkinter.after_cancel(solve)
            '''
        else:
            print('尚未打开文件')
            self.text.insert(END, "\n尚未打开文件")

    def stop_play_vlc(self):
        if self.media:
            self.media.stop()
    
    def textrank(self, p=None):
        if os.path.exists(p+'\\result.txt'):
            self.text.insert(END, "\n正在进行知识点提取，请勿关闭")
            root.update()
            if os.system("python textrank.py %s"%(p,)) == 0:
                #self.text.delete(END)
                self.text.insert(END, "\n知识点标签提取成功，文档位置:\n"+p+"\\keywords.txt")
                result = ''
                with open(p+'\\keywords.txt', "r", encoding='utf-8') as file:
                    result = file.read()
                    file.close()
                self.text.delete(1.0,END)
                self.text.insert(END,'知识点提取结果：\n')
                self.text.insert(END,result)
                tkinter.messagebox.showinfo('知识点提取结果', result)
            else:
                #self.text.delete(END)
                self.text.insert(END, "\n知识点提取失败，请重试")
                root.update()
                return
        else:
            tkinter.messagebox.showwarning('提示', '请先进行语音分析')
            return

    def nlpir(self, p=None):
        if os.path.exists(p+'\\result.txt'):
            self.text.insert(END, "\n正在进行敏感词审核，请勿关闭")
            root.update()
            if os.system("python nlpir.py %s"%(p,)) == 0:
                #self.text.delete(END)
                self.text.insert(END, "\n敏感词审核完成，分词存储位置:\n"+p+"\\words.txt")                
                if os.path.exists(p+'\\sen_words.txt'):
                    result = ''
                    with open(p+'\\sen_words.txt', "r", encoding='utf-8') as file:
                        result = file.read()
                        file.close()
                    tkinter.messagebox.showinfo('敏感词结果', result)
                else:
                    tkinter.messagebox.showinfo('敏感词结果', '未发现敏感词')               
            else:
                #self.text.delete(END)
                self.text.insert(END, "\n敏感词审核失败，请重试")
                root.update()
                return
        else:
            tkinter.messagebox.showwarning('提示', '请先进行语音分析')
            return

    def subtitles(self, p=None, f=None):
        if os.path.exists(p+'\\result1.txt'):
            self.text.insert(END, "\n正在进行字幕生成，请勿关闭")
            root.update()
            if os.system("python srt.py %s"%(p,)) == 0:
                #self.text.delete(END)
                if os.path.exists(p+'\\subtitles.txt'):
                    os.rename(p+"\\subtitles.txt",p+"\\subtitles.srt")
                    if os.path.exists(p+'\\subtitles.srt'):
                        self.text.insert(END, "\n字幕生成完成，字幕存储位置:\n"+p+"\\subtitles.srt")
                        self.text.insert(END, "\n正在加载字幕，请勿关闭")
                        root.update()
                        now_path = os.getcwd()
                        os.chdir(p)
                        print(os.getcwd())
                        if os.system("D:\\ffmpeg\\bin\\ffmpeg -i %s -vf subtitles=subtitles.srt -y %s\\final.mp4"%(f,p)) == 0:
                            os.chdir(now_path)
                            print(os.getcwd())
                            self.text.insert(END, "\n字幕视频加载完成，视频存储位置:\n"+p+"\\final.mp4")
                            root.update()
                            if tkinter.messagebox.askyesno('字幕加载完成', '视频存储位置:\n'+p+'\\final.mp4\n是否播放视频？') == True:
                                try:
                                    file = p + '\\final.mp4'
                                    #self.text.delete(1.0,END)
                                    self.text.insert(END, "视频路径:\n"+f)
                                    self.play_media(button=self.media, f_path=file)
                                except:
                                    self.show_video.insert(END, "\n文件打开失败")
                                    return False
                            else:
                                return
                        else:
                            #self.text.delete(END)
                            os.chdir(now_path)
                            print(os.getcwd())
                            self.text.insert(END, "\n字幕加载失败，请重试")
                            root.update()
                            return
                    else:
                        #self.text.delete(END)
                        self.text.insert(END, "\n字幕生成失败，请重试")
                        root.update()
                        return
                else:
                    #self.text.delete(END)
                    self.text.insert(END, "\n字幕生成失败，请重试")
                    root.update()
                    return              
                              
            else:
                #self.text.delete(END)
                self.text.insert(END, "\n字幕生成失败，请重试")
                root.update()
                return
        else:
            tkinter.messagebox.showwarning('提示', '请先进行语音分析')
            return

if __name__ == '__main__':
    # 软件版本号
    soft_ver = "v1.0"

    # 通过tk与mainloop做一个窗口，标题为：厂测软件
    root = Tk()
    # 窗口不可调整大小
    root.resizable(True, True)
    # 标题
    root.title("在线课程视频语音分析系统 版本: %s" % soft_ver)
    root.update()
    # 图标
    # root.iconbitmap("E:\\Trunk_SVN\\xbox1\\test\\tools\\prduct_tool\\main\\ico.ico")
    # ImageTk.PhotoImage(file=".\\ico.ico")

    # 设置窗口大小
    # 获取屏幕长宽
    w_height = root.winfo_screenheight()
    w_width = root.winfo_screenwidth()
    print("屏幕比例: %s x %s" % (w_width, w_height))
    # 笔记本分辨率 1536 * 864
    # root.geometry("1280x720+400+200") # 固定位置
    x, y = 1320, 570
    root.geometry("%dx%d+%d+%d" % (x, y, (w_width - x) / 2, (w_height - y) / 2))

    app = Production_Tool(root)

    # app.show.insert(END, ("\n屏幕比例: %s x %s" % (w_width, w_height)))
    app.dport_st = False

    root.mainloop()

    print("exit###")

    app.stop_play_vlc()
