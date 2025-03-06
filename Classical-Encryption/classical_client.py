import socket

def start_client():
    client = socket.socket()
    client.connect(('localhost', 9999))
    
    cipher_type = input("Enter cipher type (Caesar, Monoalphabetic, Playfair, Hill, Vigenere, One-Time Pad, Rail Fence): ")
    operation = input("Enter operation (encrypt/decrypt): ")
    message = input("Enter message: ")
    key = input("Enter key (if applicable): ")
    
    request = f"{cipher_type}|{operation}|{message}|{key}"
    client.send(request.encode())
    response = client.recv(1024).decode()
    print(f"Response from server: {response}")
    client.close()

if __name__ == "__main__":
    start_client()
