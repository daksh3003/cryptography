import json
import socket
from rsa import encrypt

HOST = 'localhost'
PORT  = 8080
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    data = s.recv(1024).decode()
    e, n = map(int, data.strip().split(','))

    print(f"Recieved public key: (e = {e}, n = {n})")
    message = input("Enter message to encrypt")
    encrypted = encrypt((e,n),message)
    print("Encrypted message:",encrypted)
    
    s.send(','.join(map(str,encrypted)).encode())