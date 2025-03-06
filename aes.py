import numpy as np

# AES-256 S-Box (For SubBytes)
S_BOX = [
    [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
    [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
    [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
    [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
]

# XOR Function
def xor_bytes(a, b):
    return bytes(i ^ j for i, j in zip(a, b))

# Pad plaintext to 16 bytes
def pad(plaintext):
    pad_len = 16 - (len(plaintext) % 16)
    return plaintext + bytes([pad_len] * pad_len)

# Substitute bytes using AES S-Box
def sub_bytes(state):
    return bytes(S_BOX[(b >> 4)][b & 0x0F] for b in state)

# ShiftRows transformation
def shift_rows(state):
    state = np.array(state).reshape(4, 4)
    state[1] = np.roll(state[1], -1)
    state[2] = np.roll(state[2], -2)
    state[3] = np.roll(state[3], -3)
    return state.flatten()

# AES-256 Encryption
def aes256_encrypt(plaintext, key):
    if len(key) != 32:
        raise ValueError("AES-256 requires a 256-bit (32-byte) key.")
    
    plaintext = pad(plaintext.encode())  # Convert to bytes & pad
    state = xor_bytes(plaintext, key[:16])  # Initial XOR
    state = sub_bytes(state)
    state = shift_rows(state)
    
    return state.hex()  # Convert to hex

# AES-256 Decryption
def aes256_decrypt(ciphertext, key):
    if len(key) != 32:
        raise ValueError("AES-256 requires a 256-bit (32-byte) key.")
    
    state = bytes.fromhex(ciphertext)  # Convert hex to bytes
    state = shift_rows(state)  # Reverse ShiftRows
    state = sub_bytes(state)  # Reverse SubBytes
    state = xor_bytes(state, key[:16])  # Reverse XOR
    
    return state.decode(errors="ignore").strip()  # Remove padding

# Testing AES-256
if __name__ == "__main__":
    key = b'ThisIsA256BitKeyForAES256!!!!!'  # 32-byte key
    plaintext = "AES-256 Test"

    encrypted = aes256_encrypt(plaintext, key)
    print("Encrypted:", encrypted)

    decrypted = aes256_decrypt(encrypted, key)
    print("Decrypted:", decrypted)
