# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName: weChatClient
@Author  : sky
@Date    : 2022/8/1 15:48
@Desc    : 客户端

"""
import wx
import socket
import threading


# 客户端继承wx.frame，就拥有了窗口界面
class WeChatClient(wx.Frame):
    def __init__(self, c_name):
        # 调用父类的构造函数
        wx.Frame.__init__(self, None, id=101, title='%s的客户端界面'%c_name, pos=wx.DefaultPosition, size=(400, 700))
        pl = wx.Panel(self)  # 在窗口初始化一个面板
        box = wx.BoxSizer(wx.VERTICAL)
        pl.SetSizer(box)

        g1 = wx.FlexGridSizer(wx.HORIZONTAL)

        conn_button = wx.Button(pl, size=(200, 40), label="连接")
        dis_conn_button = wx.Button(pl, size=(200, 40), label="断开")
        g1.Add(conn_button, 1, wx.TOP | wx.LEFT)
        g1.Add(dis_conn_button, 1, wx.TOP | wx.Right)
        box.Add(g1, 1, wx.ALIGN_CENTER)

        self.text = wx.TextCtrl(pl, size=(400, 250), style=wx.TE_MULTILINE | wx.TE_READONLY)
        box.Add(self.text, 1, wx.ALIGN_CENTER)

        self.input_text = wx.TextCtrl(pl, size=(400, 100), style=wx.TE_MULTILINE)
        box.Add(self.input_text, 1, wx.ALIGN_CENTER)

        g2 = wx.FlexGridSizer(wx.HORIZONTAL)
        clear_button = wx.Button(pl, size=(200, 40), label="重置")
        send_button = wx.Button(pl, size=(200, 40), label="发送")
        g2.Add(clear_button, 1, wx.TOP | wx.LEFT)
        g2.Add(send_button, 1, wx.TOP | wx.RIGHT)
        box.Add(g2, 1, wx.ALIGN_CENTER)

        pl.SetSizer(box)

        '''给所有按钮绑定点击事件'''
        self.Bind(wx.EVT_BUTTON, self.connect_to_server, conn_button)
        self.Bind(wx.EVT_BUTTON, self.send_to, send_button)
        self.Bind(wx.EVT_BUTTON, self.go_out, dis_conn_button)
        self.Bind(wx.EVT_BUTTON, self.reset, clear_button)

        '''客户端属性'''
        self.name = c_name
        self.isConnected = False  # 客户端是否已经连上服务器
        self.client_socket = None

    # 连接服务器
    def connect_to_server(self, event):
        print(f"客户端{self.name}，开始连接服务器")
        if not self.isConnected:
            server_host_port = ('localhost', 8888)
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(server_host_port)
            # 之前规定客户端只要连接成功，马上把自己的名字发给服务器
            self.client_socket.send(self.name.encode('utf-8'))
            self.isConnected = True
            t = threading.Thread(target=self.recive_data)
            t.setDaemon(True)  # 客户端界面如果关闭，当前守护线程也自动关闭
            t.start()

    # 接收服务器数据
    def recive_data(self):
        while self.isConnected:
            data = self.client_socket.recv(1024).decode('utf-8')
            # 从服务器接收到的数据，需要显示
            self.text.AppendText(f"{data}\n")

    # 客户端发送消息到聊天室
    def send_to(self, event):
        if self.isConnected:
            info = self.input_text.GetValue()
            if len(info) > 0:
                self.client_socket.send(info.encode('utf-8'))
                # 输入框中的数据如果已经发送，输入框设置为空
                self.input_text.Clear()

    # 客户端离开聊天室
    def go_out(self, event):
        self.client_socket.send('A^disconnect^B'.encode('utf-8'))
        # 客户端主线程也要关闭
        self.isConnected = False

    # 客户端输入框的信息重置
    def reset(self, event):
        self.input_text.Clear()


if __name__ == "__main__":
    app = wx.App()
    name = input("请输入客户端名字：")
    WeChatClient(name).Show()
    app.MainLoop()  # 循环刷新显示
