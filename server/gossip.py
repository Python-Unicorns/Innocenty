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
        self.si = self.create_socket_instance()
        self.so = self.create_socket_instance()
        self.outf = 'test' + self.name
        self.queue = {}

    def create_socket_instance(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)



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
                        print(sock_data)
                        # time.delay(3)
                        # self.so.connect(sock_data)
                        sock.send('add_nodes ' + json.dumps(self.nodes))
                        # self.so.sendto('test', sock_data)
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
            self.si.bind((self.host, self.port))
            self.log('successfully binded')
            self.si.listen(5)
            self.log('add 5 listeners')
            th = threading.Thread(name='th1', target=self.conn_accept)
            th.start()
        except Exception as e:
            self.log('error : ' + str(e))
            print('sock')

    def accept(self):
        self.log('accept connection')
        return self.si.accept()




    def add_node(self, gossip_socket):
        print(gossip_socket)
        self.nodes.append(gossip_socket)

    def parse_command(self, res):
        d = res.split(' ')
        c = d[0]
        data_array = ' '.join(d[1::])
        if (c == 'add_nodes'):
            self.parse_nodes_list(data_array)

    def parse_nodes_list(self, nodes_list=[]):
        d = json.loads(nodes_list)
        print(d)
        for i in d:
            self.add_node((i[0], i[1]))
        # for i in nodes_list:
        #     print(i)
        #     d = json.loads(i)
        #     print(d)
        #     for j in d:
        #         print(j)

    def add_master(self, port):
        self.so.bind((self.host, self.port))
        self.connect(port)
        self.nodes.append(port)
        self.so.send('add_to_list')
        self.log('master added')
        b = self.so.recv(1024)
        # print(b)
        self.parse_command(b)
        self.so.close()
        self.so = self.create_socket_instance()
        # self.so.bind((self.host, self.port))



    def connect(self, port):
        self.so.connect(('localhost', int(port)))

    def send(self, data):
        print(data)
        port = random.randint(5000, 9000)
        if (self.nodes.__len__() != 0):
            node = self.nodes[random.randint(0, len(self.nodes) - 1)]
            self.connect(node.port)
        self.so.send(data.encode('utf-8'))
