import socket

from sha256 import SHA256
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))
server.listen(1)
print("Server is listening...")

while True:
    conn, addr = server.accept()
    print(f"Connection from {addr}")
    data = conn.recv(1024).decode()
    if data:
        hasher = SHA256()
        hash_value = hasher.hash(data)
        conn.send(hash_value.encode())
    conn.close()