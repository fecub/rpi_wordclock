__author__ = 'fecub'

import socket
import threading
import time

# color
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class wordclock_socket(threading.Thread):
    def __init__(self, config):
        # server things
        # self.bind_ip   = "127.0.0.1"
        self.bind_ip = "192.168.0.132"
        self.bind_port = 10001
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.bind_ip,self.bind_port))
        self.server.listen(5)

        # property
        self._request =''
        self.tmp=''


        self.button_left = int(config.get('wordclock_interface', 'pin_button_left'))
        self.button_return = int(config.get('wordclock_interface', 'pin_button_return'))
        self.button_right = int(config.get('wordclock_interface', 'pin_button_right'))

        self.virtual_button_left = int(config.get('wordclock_interface', 'virtual_pin_button_left'))
        self.virtual_button_return = int(config.get('wordclock_interface', 'virtual_pin_button_return'))
        self.virtual_button_right = int(config.get('wordclock_interface', 'virtual_pin_button_right'))

        threading.Thread.__init__(self)

        print (bcolors.OKGREEN + "[*] Listening on %s:%d" % (self.bind_ip, self.bind_port) + bcolors.ENDC)

    def handle_client(self, client_socket):
        # this is our client-handling thread
        # print out what the client sends
        self.tmp = ''
        # self._request = client_socket.recv(1024)
        self.set_request(client_socket.recv(1024))
        print (bcolors.OKGREEN + "[*] Received: %s" % self.request() + bcolors.ENDC)
        # send back a packet

        client_socket.send('HI') # verschiedene menues moeglich
        client_socket.close()


    def waitForEvent(self):
        # print("self.request: {0}", self.request())
        # print("self.tmp: {0}", self.tmp)
        while True:
            # if (self.request() != self.tmp):
            #     self.tmp = self._request
            returnvalue = -1
            if (self.request() == "bleft"):
                print("bleft girdi")
                returnvalue = 17
            if (self.request()== "bmiddle"):
                print("bmiddle girdi")
                returnvalue = 22
            if (self.request() == "bright"):
                print("bright girdi")
                returnvalue = 24

            return returnvalue

            # if (self.request() == "bleft"):
            #     print("bleft girdi")
            #     return 7
            # if (self.request()== "bmiddle"):
            #     print("bmiddle girdi")
            #     return 8
            # if (self.request() == "bright"):
            #     print("bright girdi")
            #     return 11

            time.sleep(1.0 / 10)

        # return returnvalue


    def set_request(self, p_request):
        if self._request != p_request:
            self._request = p_request


    def request(self):
        return self._request


    def run(self):
        while True:
            client,addr = self.server.accept()
            print (bcolors.OKGREEN + "[*] Accepted connection from: %s:%d" % (addr[0],addr[1]) + bcolors.ENDC)
            # spin up our client thread to handle incoming data
            client_handler = threading.Thread(target=self.handle_client,args=(client,))
            client_handler.start()