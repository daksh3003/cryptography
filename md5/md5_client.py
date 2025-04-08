import socket
def simplified_md5_hash(message)->str:
    hash_val = 0x12345678
    for char in message:
        hash_val = ((hash_val<<5)+hash_val)^ord(char)
        hash_val = hash_val & 0xFFFFFFFF
    return hex(hash_val)[2:].zfill(8)

def generate_mac(secret_key,message)->str:
    return simplified_md5_hash(secret_key+message)

def send_message():
    HOST = "localhost"
    PORT = 12345
    
    secret_key = input("Enter the secret key")
    message = input("Enter the message")
    
    mac = generate_mac(secret_key, message)
    combined = message + "||" + mac
    
    with socket.socket() as client_socket:
        client_socket.connect((HOST,PORT))
        client_socket.sendall(combined.encode())
        
        response = client_socket.recv(1024).decode()
        print("Server respoonse: ",response)
        
if __name__ == "__main__":
    send_message()