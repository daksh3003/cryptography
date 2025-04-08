import socket

def simplified_md5_hash(message:str)->str:
    hash_val = 0x12345678
    for char in message:
        hash_val = ((hash_val << 5) + hash_val)^ ord(char)
        hash_val = hash_val & 0xFFFFFFFF
    return hex(hash_val)[2:].zfill(8)

def generate_mac(secret_key,message) ->str:
    return simplified_md5_hash(secret_key+message)

def start_server():
    HOST = "localhost"
    PORT  = 12345
    
    secret_key = input("Enter the secret key")
    
    with socket.socket() as server_socket:
        server_socket.bind((HOST,PORT))
        server_socket.listen(1)
        print("Server in listening...")
        
        conn,addr = server_socket.accept()
        with conn:
            print("Connected by {addr}")
            data = conn.recv(1024).decode()
            message,recieved_mac = data.split("||")
            expected_mac = generate_mac(secret_key,message)
            if(expected_mac == recieved_mac):
                response = "Mac verified. authenticated"
            else:
                response  = "Mac verificaton failed."
                
            conn.sendall(response.encode())
if __name__ == "__main__":
    start_server()