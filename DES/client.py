import socket
from des import (des_decrypt, des_encrypt)

plaintext = input("Enter the plaintext:")
c = socket.socket()
c.connect(('localhost', 9999))
key = "AABB09182736CCDD"

while True:
    cypher = des_encrypt(plaintext, key)
    print("Encrypted text on client side is:", cypher)
    c.send(bytes(cypher, "utf-8"))