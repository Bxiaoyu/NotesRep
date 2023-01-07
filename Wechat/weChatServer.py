# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@FileName: weChatServer
@Author  : sky
@Date    : 2022/8/1 16:25
@Desc    : 服务器

"""
import time

import wx
import threading
import socket


class WeChatServer(wx.Frame):
    def __init__(self, c_name=''):
        # 调用父类的构造函数
        wx.Frame.__init__(self, None, id=102, title='服务器', pos=wx.DefaultPosition, size=(400, 470))
        pl = wx.Panel(self)  # 在窗口初始化一个面板
        box = wx.BoxSizer(wx.VERTICAL)
        pl.SetSizer(box)

        g1 = wx.FlexGridSizer(wx.HORIZONTAL)

        start_server_button = wx.Button(pl, size=(133, 40), label="启动")
        record_save_button = wx.Button(pl, size=(133, 40), label="保存聊天记录")
        stop_server_button = wx.Button(pl, size=(133, 40), label="停止")
        g1.Add(start_server_button, 1, wx.TOP)
        g1.Add(record_save_button, 1, wx.TOP)
        g1.Add(stop_server_button, 1, wx.TOP)
        box.Add(g1, 1, wx.ALIGN_CENTER)

        self.text = wx.TextCtrl(pl, size=(400, 400), style=wx.TE_MULTILINE | wx.TE_READONLY)
        box.Add(self.text, 1, wx.ALIGN_CENTER)

        pl.SetSizer(box)

        """服务准备执行的一些属性"""
        self.isOn = False  # 服务器有没有启动
        self.host_port = ("localhost", 8888)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.host_port)
        self.server_socket.listen(5)
        self.session_thread_map = {}  # 存放所有的服务器会话线程

        """给所有的按钮绑定相应的动作"""
        self.Bind(wx.EVT_BUTTON, self.start_server, start_server_button)
        self.Bind(wx.EVT_BUTTON, self.save_record, record_save_button)
        self.Bind(wx.EVT_BUTTON, self.stop_server, stop_server_button)

    # 服务器启动函数
    def start_server(self, event):
        print('服务器开始启动')
        if not self.isOn:
            # 启动服务器的主线程
            self.isOn = True
            main_thread = threading.Thread(target=self.do_work)
            main_thread.setDaemon(True)  # 设置为守护线程
            main_thread.start()

    # 服务器运行之后的函数
    def do_work(self):
        print('服务器开始工作')
        while self.isOn:
            session_socket, client_addr = self.server_socket.accept()
            # 服务器首先接受客户端发送过来的第一条消息，我们呢规定第一条消息为客户端的名字
            username = session_socket.recv(1024).decode('utf-8')
            # 创建一个会话线程
            session_thread = SessionThread(session_socket, username, self)
            self.session_thread_map[username] = session_thread
            session_thread.start()
            # 表示有客户端进入
            self.show_info_and_send_client("服务器通知",f"欢迎{username}进入聊天室!", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        self.server_socket.close()

    # 在文本中显示信息并发送消息给所有客户端
    def show_info_and_send_client(self, source, data, date_time):
        """
        在文本中显示信息并发送消息给所有客户端
        :param source: 信息源
        :param data: 数据
        :param data_time: 时间
        :return:
        """
        send_data = f"{source} : {data}\n时间: {date_time}\n"
        self.text.AppendText(f"---------------------\n{send_data}")
        for client in self.session_thread_map.values():
            if client.isOn:
                client.user_socket.send(send_data.encode('utf-8'))

    # 保存服务器聊天记录
    def save_record(self, event):
        record = self.text.GetValue()
        filename = f"record_{time.strftime('%Y-%m-%d', time.localtime())}.log"
        with open(filename, "w+") as f:
            f.write(record)

    # 服务器停止
    def stop_server(self, event):
        self.show_info_and_send_client("服务器通知：", "服务器关闭服务！", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        self.isOn = False

# 服务器端会话线程的类
class SessionThread(threading.Thread):
    def __init__(self, socket, un, server):
        threading.Thread.__init__(self)
        self.user_socket = socket
        self.username = un
        self.server = server
        self.isOn = True  # 会话线程是否启动

    def run(self) -> None:
        print(f'客户端{self.username}，已经和服务器连接成功，服务器启动一个会话线程')
        while self.isOn:
            data = self.user_socket.recv(1024).decode('utf-8')  # 接受客户端的聊天信息
            if data == 'A^disconnect^B':  # 如果客户端点击断开按钮，先发一条消息给服务器，消息内容我们规定：A^disconnect^B
                self.isOn = False
                # 通知其他人有人下线了
                self.server.show_info_and_send_client("服务器通知：", f"{self.username}离开聊天室", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            else:
                # 其它聊天信息，我们应该显示给所有客户端，包括服务器
                self.server.show_info_and_send_client(self.username, data, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        self.user_socket.close()  # 保持和客户端连接的socket关闭

if __name__ == "__main__":
    app = wx.App()
    WeChatServer().Show()
    app.MainLoop()
