import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))
message = input("Enter message to hash: ")
client.send(message.encode())
print("SHA-256 Hash:", client.recv(1024).decode())
client.close()
