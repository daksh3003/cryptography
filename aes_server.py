import socket
from aes import aes256_decrypt

HOST = 'localhost'
PORT = 9999
KEY = b'ThisIsA256BitKeyForAES256!!!!!'  # 32-byte key

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server is listening on port", PORT)

client_socket, client_address = server.accept()
print(f"Connection established with {client_address}")

# Receive encrypted message
encrypted_message = client_socket.recv(1024).decode()
print(f"Encrypted Message Received: {encrypted_message}")

# Decrypt the message
decrypted_message = aes256_decrypt(encrypted_message, KEY)
print(f"Decrypted Message: {decrypted_message}")

client_socket.close()
server.close()
