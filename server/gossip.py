import socket
# import SocketServer
import time
import sys
import os
import signal
import threading
# import Queue
import re
import getopt
import random
import json
# from tornado.platform.asyncio import AsyncIOMainLoop, AsyncIOLoop
# AsyncIOMainLoop().install()

# NODES = [333444, 334455, 4434435]

class GossipSocket(threading.Thread):


    def __init__(self, name, port, host=''):
        threading.Thread.__init__(self)
        self.name = name
        self.port = int(port)
        self.host = host
        self.nodes = []
        self.s = socket.socket()
        self.outf = 'test' + self.name
        self.queue = {}



    def log(self, message):
        f = open(self.outf, 'a')
        f.write(message + '\n')
        f.close()

    def conn_accept(self):
        self.log('socket_started')

        sock, addr = self.accept()
        self.log('socket accepted')
        while True:
            try:
                buf = sock.recv(1024)
                if (buf):
                    if (buf.decode('utf-8') == 'add_to_list'):                        
                        sock_data = sock.getpeername()
                        print(sock_data, addr)
                        self.nodes.append(sock_data)
                        self.s.sendto('test', sock_data)
                        sock, addr = self.accept()
                    else:
                        print()

            except Exception as e:
                print(self.name + ' nodata')
                self.log('error : ' + str(e))
                sock, addr = self.accept()

    def sstart(self):
        # self.start()
        self.log('thread_started')
        try:
            print(self.host, self.port)
            self.s.bind((self.host, self.port))
            self.log('successfully binded')
            self.s.listen(5)
            self.log('add 5 listeners')
            th = threading.Thread(name='th1', target=self.conn_accept)
            th.start()
        except Exception as e:
            self.log('error : ' + str(e))
            print('sock')

    def accept(self):
        self.log('accept connection')
        return self.s.accept()




    def add_node(self, gossip_socket):
        print(gossip_socket)
        self.nodes.append(gossip_socket)

    def add_master(self, port):
        self.connect(port)
        self.nodes.append(port)
        self.s.send('add_to_list')
        self.log('master added')
        self.s.close()
        self.s = socket.socket()


    def connect(self, port):
        self.s.connect(('localhost', int(port)))

    def send(self, data):
        print(data)
        port = random.randint(5000, 9000)
        if (self.nodes.__len__() != 0):
            node = self.nodes[random.randint(0, len(self.nodes) - 1)]
            self.connect(node.port)
        self.s.send(data.encode('utf-8'))
