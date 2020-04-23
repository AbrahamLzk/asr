# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
import tkinter.filedialog
import tkinter.messagebox
import stat
import shutil
from tkinter import *
from tkinter import scrolledtext


import vlc

def readonly_handler(func, path, execinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

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

        self.show_video = Text(frame1, width=150, height=40, wrap=WORD, bd=3, bg="white")
        self.show_video.grid(row=15, column=1, rowspan=1, columnspan=3, sticky=W)
        self.show_video.insert(END, "等待视频播放")
        self.media = vlc.MediaPlayer()

        self.bt_play = Button(frame1, text="视频播放", command=lambda: self.play_button(self.file_path,self.p_path), bd=2,
                              width=49)
        self.bt_play.grid(row=16, column=1, rowspan=1, sticky=W)
        
        self.bt_pause = Button(frame1, text="视频暂停", command=lambda: self.pause_media(button=self.media), bd=2,
                               width=48)
        self.bt_pause.grid(row=16, column=2, rowspan=1, sticky=W)

        self.bt_stop = Button(frame1, text="视频停止", command=lambda: self.stop_play_vlc(), bd=2,
                              width=49)
        self.bt_stop.grid(row=16, column=3, rowspan=1, sticky=W)

        self.file_path = ''
        self.p_path = ''
        self.name = ''

        global e
        e = StringVar()

        if "Windows" == platform.system():
            # 主子设备视频播放
            self.media.set_hwnd(self.show_video.winfo_id())
        else:
            print("错误", "不支持此平台！")
            exit(-1)

        self.bt_play = Label(frame, text="")
        self.bt_play.grid(row=0, sticky=W)
        self.entry = Entry(frame, textvariable = e, bd=2, width=23)
        self.entry.grid(row=1, column=1, rowspan=1, sticky=W)
        e.set('请先进行语音分析')
        self.bt_play = Button(frame, text="搜索", command=lambda: self.search(self.p_path), bd=2,
                              width=4)
        self.bt_play.grid(row=1, column=2, rowspan=1, sticky=W)

        self.bt_play = Button(frame, text="打开文件", command=lambda: self.fn_open_file(), bd=3,
                              width=30)
        self.bt_play.grid(row=2, column=1, rowspan=1, columnspan=2, sticky=W)

        self.bt_open = Button(frame, text="语音分析", command=lambda: self.speech(self.file_path), bd=3,
                              width=30)
        self.bt_open.grid(row=3, column=1, rowspan=1, columnspan=2, sticky=W)

        self.bt_stop = Button(frame, text="敏感词审核", command=lambda: self.nlpir(self.p_path), bd=3,
                              width=30)
        self.bt_stop.grid(row=4, column=1, rowspan=1, columnspan=2, sticky=W)

        self.bt_stop = Button(frame, text="获得知识点", command=lambda: self.textrank(self.p_path), bd=3,
                              width=30)
        self.bt_stop.grid(row=5, column=1, rowspan=1, columnspan=2, sticky=W)

        self.bt_stop = Button(frame, text="加入字幕", command=lambda: self.subtitles(self.p_path,self.file_path), bd=3,
                              width=30)
        self.bt_stop.grid(row=6, column=1, rowspan=1, columnspan=2, sticky=W)


        self.text = scrolledtext.ScrolledText(frame, width=31, height=28, wrap=WORD, bd=3, bg="white")
        self.text.grid(row=7, column=1, rowspan=1, columnspan=2, sticky=W)
        self.text.insert(END, "请选择视频文件，并进行语音分析")

    def play_media(self, button=None, f_path=None):
        if button and f_path:
            print("button: %s, filepath: %s" % (button, f_path))
            button.set_mrl(f_path)
            button.play()
            self.show_video.delete(0.0, END)
            self.show_video.insert(END, "等待视频播放")

    def play_button(self, f=None, p=None):
        if f:
            a = tkinter.messagebox.askyesnocancel('提示','请选择播放视频类型：\n是：播放无字幕视频\n否：播放有字幕视频')
            if a == True:
                self.play_media(button=self.media, f_path=f)
            elif a == False:
                if os.path.exists(p+'\\final.mp4'):
                    self.play_media(button=self.media, f_path=p+'\\final.mp4')
                else:
                    tkinter.messagebox.showwarning('提示', '请先生成字幕视频')
        else:
            tkinter.messagebox.showwarning('提示', '请先选择视频文件')


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
        except:
            self.show_video.insert(END, "\n文件打开失败")
            return False
        if f:
            self.text.delete(1.0,END)
            self.text.insert(1.0, "视频路径:\n"+f)
            print("File: %s" % f)
            self.file_path = f
            name = f.split('/')[-1]
            name = name.split('.')[0]
            self.name = name
            p = os.getcwd()+'\\'+name
            self.p_path = p
            if os.path.exists(p+'\\result.txt') and os.path.exists(p+'\\result1.txt') and os.path.exists(p+'\\time_data.txt'):
                self.text.insert(END, "\n本视频已有语音分析结果，语音分析结果路径:\n"+p)
                e.set('多个查询词请用/分开')        
            if tkinter.messagebox.askyesno('提示','是否开始播放本视频？') ==True:
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
                shutil.rmtree(filePath, onerror=readonly_handler)
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
            #if os.system("python iat_ws_python3.py %s"%(p,)) == 0:
            if os.system("python asr_json.py %s"%(p,)) == 0:
                #self.text.delete(END)
                self.text.insert(END, "\n语音识别成功，文档位置:\n"+p+"\\result.txt")
                result = ''
                with open(p+'\\result.txt', "r", encoding='utf-8') as file:
                    result = file.readlines()
                    file.close()
                e.set('多个查询词请用/分开')
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
            if os.system("python textrank.py %s %s"%(p,self.name,)) == 0:
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
        if os.path.exists(p+'\\result1.txt') and os.path.exists(p+'\\time_data.txt'):
            self.text.insert(END, "\n正在进行敏感词审核，请勿关闭")
            root.update()
            #if os.system("python nlpir_DFA.py %s"%(p,)) == 0:
            if os.system("python nlpir_ac.py %s"%(p,)) == 0:
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
        if os.path.exists(p+'\\result1.txt') and os.path.exists(p+'\\time_data.txt'):
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
    def search(self, p=None):
        if os.path.exists(p+'\\result1.txt') and os.path.exists(p+'\\time_data.txt'):
            self.text.insert(END, "\n正在进行搜索，请勿关闭")
            root.update()
            if e.get() != '':
                text = str(e.get())
                with open(p+'\\search.txt', "a", encoding='utf-8') as file:
                    for element in text.split('/'):
                        file.write(element)
                        file.write('\n')
                    file.close()
                if os.system("python search.py %s"%(p,)) == 0:
                    #self.text.delete(END)
                    self.text.insert(END, "\n搜索完成，搜索历史存储位置:\n"+p+"\\search_history.txt")                
                    if os.path.exists(p+'\\search_result.txt'):
                        result = ''
                        with open(p+'\\search_result.txt', "r", encoding='utf-8') as file:
                            result = file.read()
                            file.close()
                        tkinter.messagebox.showinfo('搜索结果', result)
                    else:
                        tkinter.messagebox.showinfo('搜索结果', '未发现该文本')               
                else:
                    #self.text.delete(END)
                    self.text.insert(END, "\n搜索失败，请重试")
                    root.update()
                    return
            else:
                tkinter.messagebox.showwarning('提示', '请输入搜索文本')
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
    x, y = 1320, 600
    root.geometry("%dx%d+%d+%d" % (x, y, (w_width - x) / 2, (w_height - y) / 2))

    app = Production_Tool(root)

    # app.show.insert(END, ("\n屏幕比例: %s x %s" % (w_width, w_height)))
    app.dport_st = False

    root.mainloop()

    print("exit###")

    app.stop_play_vlc()
