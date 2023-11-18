import socket
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

### Environment variables
load_dotenv()

IP = os.getenv("IP")
PORT = int( os.getenv("PORT") )
NUM_OF_FILES = int( os.getenv("NUM_OF_FILES") )
HEADER_SIZE = int( os.getenv("HEADER_SIZE") )
FORMAT = os.getenv("FORMAT")
FOLDER_NAME = "localFolder"

def main():
    # Connect to server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect( (IP, PORT) )

    key = server.recv(44) # 44 is size of key sent by server
    cipherSuite = Fernet(key)
    print(key)

    # Get list of file names in folder
    files = os.listdir(FOLDER_NAME) # Grab the contents of the file to send

    for fileName in files:
        # Open each file in byte read mode
        with open(os.path.join(FOLDER_NAME, fileName), "r") as file:
            fileContent = file.read().encode(FORMAT)
            encryptedContent = cipherSuite.encrypt(fileContent)
            contentSize = len(encryptedContent)

            # Pad the file name to make it the size of the server's buffersize
            paddedHeader = (f"{fileName},{contentSize},").ljust(HEADER_SIZE)

            # Send to the server the file name
            server.sendall( paddedHeader.encode(FORMAT) )

            # Send the file content to the server
            print(f"Sending contents of {fileName} to server...")
            server.sendall( encryptedContent )

if __name__ == "__main__":
    main()