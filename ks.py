# KILL SERVER SCRIPT
import socket
import os
from dotenv import load_dotenv

load_dotenv()

IP = os.getenv("IP")
PORT = int( os.getenv("PORT") )
NUM_OF_FILES = int( os.getenv("NUM_OF_FILES") )
HEADER_SIZE = int( os.getenv("HEADER_SIZE") )
FORMAT = os.getenv("FORMAT")

def main():
    # Connect to server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect( (IP, PORT) )
    server.send( "KILL,0".encode(FORMAT) )

if __name__ == "__main__":
    main()
    main()