import socket
import string

def mod_exp(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

def simple_hash(message, prime):
    return sum(ord(c) for c in message) % prime

p = 97 
g = 5   
y = int(input("Enter the sender's public key (y): ")) 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen(1)
print("DSS Server started, waiting for client...")

client, addr = server.accept()
print(f"Connected to {addr}")

data = client.recv(1024).decode()
message, r, s = data.split("|")
r, s = int(r), int(s)

hash_value = simple_hash(message, p)
w = mod_exp(s, p-2, p)
u1 = (hash_value * w) % (p - 1)
u2 = (r * w) % (p - 1)
v = ((mod_exp(g, u1, p) * mod_exp(y, u2, p)) % p) % (p - 1)

if v == r:
    client.send("Signature Valid".encode())
else:
    client.send("Signature Invalid".encode())

client.close()
server.close()
