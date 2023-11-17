import socket
import os
import random
import string
import base64

IP = "127.0.0.1"
port = 59000
format = "utf-8"

#Function to populate the localFolder with 20 files with at least 5kbs of sizes DONT CALL THIS FUNCTION AGAIN !
def createFiles(folder_name):

    os.makedirs(folder_name,exist_ok=True)

    file_size = 5
    number_of_files =20

    for i in range(1,number_of_files+1):
        file_name = f"file{i}.txt"
        file_path = os.path.join(folder_name,file_name)

        # Generate random text content
        content = ''.join(random.choices(string.ascii_letters + string.digits, k=file_size * 1024))

        with open(file_path,'w') as file:
            file.write(content)

def send_files(client_socket,folder_name):

    files = os.listdir(folder_name) # Grab the contents of the file to send

    for file_name in files:

        data = open(file_name,'b')
        
        #file_path = os.path.join(folder_name,file_name)
        #client_socket.send(file_path.encode(format))
        
        #file_path = os.path.join(folder_name,file_name) # create file path to send
        #client_socket.send(file_path.encode())
        #file = open(file_path,"r")
        #data = file.read()
        #client_socket.send(data.encode(format)) # send the file contents to the server

def main():

    client_folder = "localFolder"
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((IP,port))
    send_files(client,client_folder)




main()