import socket
import base64



port= 55345
localHost = ' 127.0.0.1'

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((localHost,port))
server.listen()

format = 'utf-8'