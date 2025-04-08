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
x = int(input("Enter sender's private key (x): "))  

message = input("Enter the message to sign: ")
hash_value = simple_hash(message, p)

k = int(input("Enter random value (k): "))  
r = mod_exp(g, k, p) % (p - 1)
s = ((hash_value + x * r) * k) % (p - 1)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))
client.send(f"{message}|{r}|{s}".encode())

response = client.recv(1024).decode()
print(response)

client.close()
