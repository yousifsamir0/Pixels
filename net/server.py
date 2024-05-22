import socket
import threading
import time
from driver.pixels_driver import Trade
class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.client_address = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}")

    def accept_connection(self):
        self.client_socket, self.client_address = self.server_socket.accept()
        print(f"Connection established with {self.client_address}")
        return self.client_socket

    def receive_message(self, client_socket):
        data = client_socket.recv(1024).decode()
        return data

    def send_message(self, client_socket, message):
        client_socket.sendall(message.encode())

    def close_connection(self, client_socket):
        client_socket.close()

    def handle_client(self, client_socket):
        username=None
        while True:
            try:
                # Receive message from the client
                message = self.receive_message(client_socket)
                print("Received message:", message)
                # Handle different cases
                if message == '':
                    self.close_connection(client_socket)
                    print("Connection closed by client")
                    self.client_socket =None
                    break
                elif 'start:' in message:
                    username = message.replace('start:','')
                    Trade.accept_trade(username)
                    self.send_message(client_socket,message)
                elif 'end' in message:
                    Trade.agree_trade()
                    self.send_message(client_socket,message)
                elif 'add' in message:
                    time.sleep(1)
                    trade_value=Trade.get_other_trade_value()
                    Trade.add_gold(trade_value)
                    self.send_message(client_socket,message)

            except ConnectionAbortedError:
                print('error: connection aborted')
                return
    def wait_for_connections(self):
        while True:
            if not self.client_socket:
                print("Waiting for a new connection...")
                client_socket = self.accept_connection()
            # Handle client connection in a separate thread
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,),daemon=True)
                client_thread.start()





if __name__ == '__main__':
    # Create and start the server
    server = Server('192.168.1.102', 12345)
    # Wait for connections
    server.wait_for_connections()



