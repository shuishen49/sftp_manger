
#!/usr/bin/python
# -*- coding: UTF-8 -*-
# python3  使用 tkinter
import tkinter as tk
import paramiko
from tkinter import filedialog
import json
import os

def putfile(port,server,username,password,file_list,path):
    port=int(port)
    transport = paramiko.Transport((server, port))    # 获取Transport实例
    transport.connect(username=username, password=password)    # 建立连接
    # 创建sftp对象，SFTPClient是定义怎么传输文件、怎么交互文件
    sftp = paramiko.SFTPClient.from_transport(transport)
    # 将本地 api.py 上传至服务器 /www/test.py。文件上传并重命名为test.py
    for file in file_list:
        if(len(file)>=5):
            print("file:"+file)
            path2=path+os.path.basename(file)
            print("path:"+path2)
            sftp.put(file, path2)
    # 将服务器 /www/test.py 下载到本地 aaa.py。文件下载并重命名为aaa.py
    # sftp.get("/www/test.py", "E:/test/aaa.py")
    print("# 关闭连接")
    transport.close()

def loadconfig():
    fp = open('config.txt', 'r')
    edc_string = fp.read()
    dec_string = json.loads(edc_string)
    config = dec_string
    return config

def choosefile():
    cur=filedialog.askopenfilenames(filetypes=[('所有文件', '.*')])
    if cur:
        for everyOne in cur:
            print(everyOne)
            t_file_list.insert(1.0,everyOne+"\n")
    else:
        print('你没有选择任何文件')
    return cur

def saveconfig():
    config={}
    #服务器列表
    config['server_list'] = str(t_server_list.get('0.0','end'))

    config['t_file_list'] = str(t_file_list.get('0.0','end'))

    #端口
    config['t_port'] = str(t_port.get())
    port=config['t_port']
    #密码
    config['t_pass'] = str(t_pass.get())   
    password=config['t_pass'] 
    #user
    config['t_user'] = str(t_user.get())
    username=config['t_user']
    #t_path
    config['t_path'] = str(t_path.get())
    path=config['t_path']
    print(config)
    enc_string=json.dumps(config)
    with open("config.txt", "w") as fp:
        fp.write(enc_string)
    server_list=config['server_list'].split('\n',); # 以空格为分隔符，分隔成两个
    file_list=config['t_file_list'].split('\n',); # 以空格为分隔符，分隔成两个
    for server in server_list:
        if(len(server)>10):
            print(server)
            print(file_list)
            putfile(port,server,username,password,file_list,path)


root = tk.Tk()

root.geometry('700x300+500+200')
root.title('sftp批量服务器维护')  # 设置窗体的标题栏

 
w = tk.Label(root, text="服务器列表:")
w.grid(row=1,column=1)
t_server_list=tk.Text(root,width = 60,height = 5)
t_server_list.grid(row=2,column=1,columnspan=4)

w = tk.Label(root, text="端口:")
w.grid(row=3,column=1)

t_port = tk.StringVar()
# t1.set('春季里那个百花开')
entry = tk.Entry(root, textvariable = t_port)
entry.grid(row=3,column=2)
# print (t_port.get())

w = tk.Label(root, text="密码:")
w.grid(row=3,column=3)

t_pass = tk.StringVar()
# t1.set('春季里那个百花开')
entry1 = tk.Entry(root, textvariable = t_pass)
entry1.grid(row=3,column=4)

w = tk.Label(root, text="用户名:")
w.grid(row=3,column=5)

t_user = tk.StringVar()
# t1.set('春季里那个百花开')
entry2 = tk.Entry(root, textvariable = t_user)
entry2.grid(row=3,column=6)

button1=tk.Button(root,text='选择需要上传的文件',command=choosefile)
button1.grid(row=4,column=1)

t_file_list=tk.Text(root,width = 40,height = 5)
t_file_list.grid(row=5,column=1,columnspan=2)

w = tk.Label(root, text="上传文件目录")
w.grid(row=4,column=3)

t_path = tk.StringVar()
entry = tk.Entry(root, textvariable = t_path)
entry.grid(row=4,column=4,sticky='n')

button2=tk.Button(root,text='开始执行',command=saveconfig)
button2.grid(row=5,column=3)

try:
    config=loadconfig()
    t_server_list.insert(1.0,config['server_list'])
    t_file_list.insert(1.0,config['t_file_list'])
    t_port.set(config['t_port'])
    t_pass.set(config['t_pass'])
    t_path.set(config['t_path'])
    t_user.set(config['t_user'])
except:
    pass

root.mainloop()
