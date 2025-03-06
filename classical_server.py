import socket
from classical import (
    caesar_cipher_encrypt, caesar_cipher_decrypt,
    monoalphabetic_encrypt, monoalphabetic_decrypt,
    playfair_encrypt, playfair_decrypt,
    hill_cipher_encrypt, hill_cipher_decrypt,
    vigenere_cipher_encrypt, vigenere_cipher_decrypt,
    one_time_pad_encrypt, one_time_pad_decrypt,
    rail_fence_encrypt, rail_fence_decrypt
)

def handle_request(request):
    parts = request.split("|")
    cipher_type = parts[0]
    operation = parts[1]  # encrypt or decrypt
    message = parts[2]
    key = parts[3] if len(parts) > 3 else None

    if cipher_type == "Caesar":
        key = int(key)
        return caesar_cipher_encrypt(message, key) if operation == "encrypt" else caesar_cipher_decrypt(message, key)

    elif cipher_type == "Monoalphabetic":
        key_map, reverse_key_map = generate_monoalphabetic_key()
        return monoalphabetic_encrypt(message, key_map) if operation == "encrypt" else monoalphabetic_decrypt(message, reverse_key_map)

    elif cipher_type == "Playfair":
        return playfair_encrypt(message, key) if operation == "encrypt" else playfair_decrypt(message, key)

    elif cipher_type == "Hill":
        key_matrix = [[6, 24], [1, 13]]  # Example key matrix
        inv_key_matrix = [[13, 24], [1, 6]]  # Example inverse key matrix
        return hill_cipher_encrypt(message, key_matrix) if operation == "encrypt" else hill_cipher_decrypt(message, inv_key_matrix)

    elif cipher_type == "Vigenere":
        return vigenere_cipher_encrypt(message, key) if operation == "encrypt" else vigenere_cipher_decrypt(message, key)

    elif cipher_type == "One-Time Pad":
        return one_time_pad_encrypt(message, key) if operation == "encrypt" else one_time_pad_decrypt(message, key)

    elif cipher_type == "Rail Fence":
        rails = int(key)
        return rail_fence_encrypt(message, rails) if operation == "encrypt" else rail_fence_decrypt(message, rails)

    return "Invalid Cipher Type"

def start_server():
    server = socket.socket()
    server.bind(('localhost', 65432))
    server.listen(5)
    print("Server started, waiting for connections...")
    
    while True:
        conn, addr = server.accept()
        print(f"Connected to {addr}")
        received_data = conn.recv(1024).decode()
        print(f"Received request: {received_data}")
        
        response = handle_request(received_data)
        print(f"Sending response: {response}")
        conn.send(response.encode())
        conn.close()

if __name__ == "__main__":
    start_server()