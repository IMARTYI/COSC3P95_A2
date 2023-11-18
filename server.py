import socket
import os
import threading
from cryptography.fernet import Fernet
from dotenv import load_dotenv

### Environment variables
load_dotenv()

IP = os.getenv("IP")
PORT = int( os.getenv("PORT") )
NUM_OF_FILES = int( os.getenv("NUM_OF_FILES") )
HEADER_SIZE = int( os.getenv("HEADER_SIZE") )
FORMAT = os.getenv("FORMAT")

### Encryption data
key = Fernet.generate_key()
cipherSuite = Fernet(key)

### Server status
exitServer = False

def handleClient(clientSocket, address):
    global exitServer

    # Send the encryption key to the client
    clientSocket.sendall(key)

    # Init folder that will hold the client's files
    # Clears out the illegal characters in folder names like . and ' by replacing them away
    folderName = "Client " + str(address).replace(".", "_").replace("\'", "")
    
    # Make the folder with the client's address as the name
    os.makedirs(folderName, exist_ok = True)

    for i in range(NUM_OF_FILES):
        # No need to decode as we recieve as bytes and then write it later into the file as bytes
        headerData = clientSocket.recv(HEADER_SIZE).decode(FORMAT).split(",")
        fileName = headerData[0]
        fileSize = int( headerData[1] )

        if fileName == "KILL":
            exitServer = True
            os.rmdir(folderName)
            break

        encryptedContent = clientSocket.recv(fileSize)
        fileContent = cipherSuite.decrypt(encryptedContent)

        # Open file to write to
        with open(os.path.join(folderName, fileName), "wb") as file:
            file.write(fileContent)
            print("Created " + fileName)
        
    clientSocket.close()

def main():
    global exitServer

    # Initialize socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind( (IP, PORT) )
    sock.listen()
    print("Server is listening on port", PORT)
    
    # Listen for client requests
    while not exitServer:
        client, address = sock.accept()
        print("Got connection from", address)
        
        # Start a thread for each client
        clientThread = threading.Thread(target=handleClient, args=(client, address))
        clientThread.start()
    
    sock.close()

if __name__ == "__main__":
    main()