import random

def caesar_cipher_encrypt(plaintext, key):
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            shift = key % 26
            base = ord('A') if char.isupper() else ord('a')
            ciphertext += chr((ord(char) - base + shift) % 26 + base)
        else:
            ciphertext += char
    return ciphertext

def caesar_cipher_decrypt(ciphertext, key):
    return caesar_cipher_encrypt(ciphertext, -key)

def generate_monoalphabetic_key():
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    shuffled = alphabet[:]
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled)), dict(zip(shuffled, alphabet))

def monoalphabetic_encrypt(plaintext, key_map):
    return "".join(key_map.get(char, char) for char in plaintext.upper())

def monoalphabetic_decrypt(ciphertext, reverse_key_map):
    return "".join(reverse_key_map.get(char, char) for char in ciphertext.upper())

def playfair_encrypt(plaintext, matrix):
    def find_position(matrix, letter):
        for i, row in enumerate(matrix):
            if letter in row:
                return i, row.index(letter)
    
    plaintext = plaintext.upper().replace("J", "I").replace(" ", "")
    if len(plaintext) % 2 != 0:
        plaintext += "X"

    ciphertext = ""
    for i in range(0, len(plaintext), 2):
        a, b = plaintext[i], plaintext[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:
            ciphertext += matrix[row1][(col1+1) % 5] + matrix[row2][(col2+1) % 5]
        elif col1 == col2:
            ciphertext += matrix[(row1+1) % 5][col1] + matrix[(row2+1) % 5][col2]
        else:
            ciphertext += matrix[row1][col2] + matrix[row2][col1]
    
    return ciphertext

def playfair_decrypt(ciphertext, matrix):
    def find_position(matrix, letter):
        for i, row in enumerate(matrix):
            if letter in row:
                return i, row.index(letter)
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:
            plaintext += matrix[row1][(col1-1) % 5] + matrix[row2][(col2-1) % 5]
        elif col1 == col2:
            plaintext += matrix[(row1-1) % 5][col1] + matrix[(row2-1) % 5][col2]
        else:
            plaintext += matrix[row1][col2] + matrix[row2][col1]

    return plaintext

def hill_cipher_encrypt(plaintext, key_matrix):
    n = len(key_matrix)
    text_vector = [ord(char) - ord('A') for char in plaintext.upper()]
    cipher_vector = [(sum(text_vector[j] * key_matrix[i][j] for j in range(n)) % 26) for i in range(n)]
    return "".join(chr(c + ord('A')) for c in cipher_vector)

def hill_cipher_decrypt(ciphertext, inv_key_matrix):
    n = len(inv_key_matrix)
    cipher_vector = [ord(char) - ord('A') for char in ciphertext.upper()]
    text_vector = [(sum(cipher_vector[j] * inv_key_matrix[i][j] for j in range(n)) % 26) for i in range(n)]
    return "".join(chr(c + ord('A')) for c in text_vector)


def vigenere_cipher_encrypt(plaintext, key):
    key = key.upper()
    key_repeated = (key * ((len(plaintext) // len(key)) + 1))[:len(plaintext)]
    ciphertext = ""
    for p, k in zip(plaintext.upper(), key_repeated):
        shift = ord(k) - ord('A')
        ciphertext += chr((ord(p) - ord('A') + shift) % 26 + ord('A'))
    return ciphertext

def vigenere_cipher_decrypt(ciphertext, key):
    key = key.upper()
    key_repeated = (key * ((len(ciphertext) // len(key)) + 1))[:len(ciphertext)]
    plaintext = ""

    for c, k in zip(ciphertext.upper(), key_repeated):
        shift = ord(k) - ord('A')
        plaintext += chr((ord(c) - ord('A') - shift) % 26 + ord('A'))

    return plaintext

def one_time_pad_encrypt(plaintext, key):
    return "".join(chr((ord(p) ^ ord(k)) % 256) for p, k in zip(plaintext, key))

def one_time_pad_decrypt(ciphertext, key):
    return "".join(chr((ord(c) ^ ord(k)) % 256) for c, k in zip(ciphertext, key))

def rail_fence_encrypt(plaintext, rails):
    fence = [[] for _ in range(rails)]
    row, step = 0, 1
    for char in plaintext:
        fence[row].append(char)
        row += step
        if row == 0 or row == rails - 1:
            step = -step
    return "".join("".join(rail) for rail in fence)

def rail_fence_decrypt(ciphertext, rails):
    fence = [[] for _ in range(rails)]
    positions = sorted(range(len(ciphertext)), key=lambda i: (i % (2 * (rails - 1))) if (i % (2 * (rails - 1))) < rails else (2 * (rails - 1)) - (i % (2 * (rails - 1))))

    for pos, char in zip(positions, ciphertext):
        fence[pos].append(char)

    return "".join(c for row in fence for c in row)