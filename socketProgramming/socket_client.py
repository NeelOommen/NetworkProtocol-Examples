import socket

def clientSide():
    host = socket.gethostname()
    server_port_address = 5000

    client_socket = socket.socket()
    client_socket.connect((host, server_port_address))

    print("Connection to server established.")

    message = input("Data to send: ")

    while message.lower().strip() != "!exit":
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()

        print("Recieved from server: " + data)
        message = input("Data to send: ")
    
    client_socket.close()
    print("Connection to server closed.")

if __name__ == "__main__":
    clientSide()