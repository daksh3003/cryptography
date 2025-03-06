import socket
from rsa import encoder, decoder, prime_filler, set_keys

# Take user input
message = input("Enter the plaintext: ")
print("\nInitial message:")
print(message)

# Create socket and connect to server
c = socket.socket()
c.connect(('localhost', 9999))

# Receive public key from the server
string = c.recv(1024).decode()
print("\nReceived public key from server:", string)

# Extract public key and n
try:
    num1, num2 = map(int, string.strip().split())
except ValueError:
    print("Error: Invalid public key format received.")
    c.close()
    exit()

# Encrypt the message
coded = encoder(message, num1, num2)

# Convert the coded list into a space-separated string
coded_str = ' '.join(map(str, coded))
print("\nThe encoded message sent to the server (encrypted by public key):")
print(coded_str)

# Send the encrypted message
c.send(coded_str.encode("utf-8"))

# Close the connection
c.close()
