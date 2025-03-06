import socket
from rsa import encoder, decoder, prime_filler, set_keys, get_keys

s = socket.socket()
prime_filler()
set_keys()
public_key, n = get_keys()

s.bind(("localhost", 9999))
s.listen(1)
print("Server is listening...")

c, addr = s.accept()
print("Connected with", addr)

# Send the public key to the client
key_string = f"{public_key} {n}"
c.send(key_string.encode("utf-8"))

# Receive the encrypted message
cypher = c.recv(2048).decode()
print("Received encrypted message:", cypher)

# Convert to integer list
try:
    coded_list = list(map(int, cypher.strip().split()))
    decyphered_text = decoder(coded_list)
    print("Decrypted text (Decrypted with private key):")
    print(decyphered_text)
except ValueError as e:
    print(f"Error in decryption: {e}")

# Close the connection
c.close()
s.close()
