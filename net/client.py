import socket

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")

    def send_message(self, message):
        self.client_socket.sendall(message.encode())

    def receive_message(self):
        data = self.client_socket.recv(1024).decode()
        print(f"Received from server: {data}")
        return data

    def close_connection(self):
        self.client_socket.close()



if __name__ == '__main__':
    # Create and start the client
    client = Client('192.168.1.104', 12345)
    # Send a message to the server
    client.send_message("Hello from the client!")
    # Receive a response from the server
    received_response = client.receive_message()
    # Close the connection
    client.close_connection()
