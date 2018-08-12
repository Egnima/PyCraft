from threading import Thread
import queue
import socket as sock

class APIHandlerThread(Thread):
    def __init__(self, msg_queue):
        Thread.__init__(self)
        self.msg_queue = msg_queue



    def run(self):
        print('API Hander Thread Started')

        self.server_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.server_socket.bind(('localhost', 8057))
        self.server_socket.listen(0)
        self.client_socket, self.addr = self.server_socket.accept()

        print('Connected Client : ', self.addr[0], self.addr[1])


        while True:
            try:
                data = self.client_socket.recv(65535)
            except Exception as ex:
                print('Error : ', ex)
                continue

            try:
                if data != b'':
                    message = data.decode('utf-8')
                    print('Received : ', message)
            except Exception as ex:
                print('Error : ', ex)
                continue

            self.msg_queue.put_nowait(message)



