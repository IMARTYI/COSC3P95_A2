import socket
import os
import threading

port = 59000 # Port Number
localHost = '127.0.0.1'
format = 'utf-8' # For encoding the data that is being transsfered
size = 1024


def receieve_file(client_socket):

    file_name = client_socket.recv(size).decode(format)

    with open(file_name,"wb") as file:
        data = client_socket.recv(size)
        while data:
            file.write(data)
            data = client_socket.recv(size)


def handle_client(client_socket):

    folder_path = client_socket.recv(size).decode(format)
    #print(folder_path)

    for _ in os.listdir(folder_path):
        receieve_file(client_socket)
        print("Files received from Client")

        client_socket.close()

def main():
    serverFolder = "ServerFolder"
    os.makedirs(serverFolder,exist_ok=True)

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((localHost,port)) # Create Socket
    server.listen() # Listen for connections by clients

    print(f"Server is Listening on {port}")

    while True:
        connections, addr = server.accept()
        print(f"Connection with {addr} is being established")
        client_thread = threading.Thread(target= handle_client,args=(connections,)) # Fork/join threading
        client_thread.start()

main()
