import socket
from rsa import generateKeypair,decrypt,isPrime
HOST = 'localhost'
PORT  = 8080

def get_prime_input(prompt):
    while True:
        try:
            val = int(input(prompt))
            if isPrime(val):
                return val
            else:
                print("Not a prime number")
        except ValueError:
            print("invalid input")
p = get_prime_input("enter a prime number")
q = get_prime_input("enter another prime number");

public,private = generateKeypair(p,q)

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen(1)
    print("server ready to listen")
    conn,addr = s.accept()
    with conn:
        conn.sendall(f"{public[0]},{public[1]}".encode())

        
        data = conn.recv(1024).decode()
        encrypted = list(map(int,data.strip().split(',')))
        print("encrypted:", encrypted)
        
        decrypted = decrypt(private,encrypted)
        print("decrypted message: ",decrypted)