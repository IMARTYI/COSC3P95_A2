import socket
import os
import base64
import threading

IP = "127.0.0.1"
port = 59000
format = "utf-8"
size = 1024

def handle_client(client_socket):

    file_path =client_socket.recv(size).decode(format)

    print(f"recivedfilePath{file_path}")

    with open(file_path,'wb') as data:

       content = data.read()
       print(content)

    #print(file_path)


def main():

    print(f"Server is listening on port{port}")
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((IP,port))
    server.listen()
    print("Server is listening for Clients")
    while True:

       conn,addr= server.accept()
       print(f"New Connection with{addr}")
       client_thread = threading.Thread(target=handle_client,args=(conn,))
       client_thread.start()

main()