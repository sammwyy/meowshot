import threading

class Server(object):
    def __init__(self, meowshot, sock):
        self.meowshot = meowshot
        self.sock = sock

    def listen_async(self):
        threading.Thread(target = self.listen).start()

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        connected = True
        while connected:
            try:
                data = client.recv(size)
                if data:
                    signal = data.decode()
                    print("Received remote signal " + signal)

                    if signal == "take_screenshot":
                        self.meowshot.open_gui()
                else:
                    connected = False
                    client.close()
            except:
                client.close()
                return False