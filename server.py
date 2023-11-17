import socket
import keyboard
import os
import base64
import threading

IP = "127.0.0.1"
PORT = 59000
NUM_OF_FILES = 20
BUFFERSIZE = 5120 # 5Kb

def handleClient(clientSocket, address):
    # Init folder that will hold the client's files
    # Clears out the illegal characters in folder names like . and ' by replacing them away
    folderName = "Client " + str(address).replace(".", "_").replace("\'", "")
    
    # Make the folder with the client's address as the name
    os.makedirs(folderName, exist_ok = True)

    for i in range(NUM_OF_FILES):
        # No need to decode as we recieve as bytes and then write it later into the file as bytes
        fileName = clientSocket.recv(BUFFERSIZE).decode().split("\n")[0]
        fileContent = clientSocket.recv(BUFFERSIZE)

        # Open file to write to
        # fileName = "file" + str(i+1) + ".txt"
        with open(os.path.join(folderName, fileName), "wb") as file:
            print("Creating " + fileName)
            file.write(fileContent)

def main():
    # Initialize socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind( (IP, PORT) )
    sock.listen()
    print("Server is listening on port", PORT)
    
    # Listen for client requests
    while True:
        client, address = sock.accept()
        print("Got connection from", address)
        
        # Start a thread for each client
        clientThread = threading.Thread(target=handleClient, args=(client, address,))
        clientThread.start()

if __name__ == "__main__":
    main()