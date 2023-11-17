import socket
import os
import base64

IP = "127.0.0.1"
PORT = 59000
FOLDER_NAME = "localFolder"
SERVER_BUFFERSIZE = 5120

def main():
    # Connect to server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect( (IP, PORT) )
    
    # Get list of file names in folder
    files = os.listdir(FOLDER_NAME) # Grab the contents of the file to send

    for fileName in files:
        # Pad the file name to make it the size of the server's buffersize
        paddedFileName = (fileName + "\n").ljust(SERVER_BUFFERSIZE)

        # Send to the server the file name
        server.send( paddedFileName.encode() )

        # Open each file in byte read mode
        with open(os.path.join(FOLDER_NAME, fileName), "rb") as file:
            # Send the file content to the server
            print("Sending contents of " + fileName + " to server...")
            fileContent = file.read()
            server.sendall( fileContent )

if __name__ == "__main__":
    main()