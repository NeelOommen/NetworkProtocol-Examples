import socket

def serverFunction():
    hostName = socket.gethostname() 
    server_port = 5000

    server_socket = socket.socket()
    server_socket.bind((hostName, server_port))

    server_socket.listen(2)
    conn, conn_address = server_socket.accept()
    print("Connection acquired from client at: " + str(conn_address))

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("Data recieved from client: " + str(data))
        data = input("Data to send to client: ")
        conn.send(data.encode())
    
    conn.close()
    print("Connection from client terminated.")

if __name__ == "__main__":
    serverFunction()