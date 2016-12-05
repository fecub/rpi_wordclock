import socket

TCP_IP = '192.168.0.132'
TCP_PORT = 5005
BUFFER_SIZE = 1024

class wordclock_socket:
    '''
    A class for open socket to controll remotely the interface buttons
    '''
    def __init__(self):
        '''
        setup socket
        '''
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "Connection initialized"
        self.s.bind((TCP_IP, TCP_PORT))
        self.s.listen(1)
        self.open()

    def open(self):
        conn, addr = self.s.accept()
        print 'Connection address:', addr
        while 1:
            data = conn.recv(BUFFER_SIZE)
            print "received data:", data
            conn.send(data)  # echo
        # if not data: break
        # conn.close()

    def close(self):
        self.s.close()
