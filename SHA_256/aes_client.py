import socket
from aes import aes256_encrypt

HOST = 'localhost'
PORT = 9999
KEY = b'ThisIsA256BitKeyForAES256!!!!!'  # 32-byte key

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

message = input("Enter a message to send securely: ")
encrypted_message = aes256_encrypt(message, KEY)

print(f"Encrypted Message Sent: {encrypted_message}")
client.send(encrypted_message.encode())

client.close()
