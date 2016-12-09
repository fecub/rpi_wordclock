__author__ = 'fecub'

import socket
import threading


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
    def __init__(self):
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
        if (self.request() != self.tmp):
            self.tmp = self._request
            return True


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