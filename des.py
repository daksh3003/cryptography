# Function to convert hex to binary
def hex2bin(s):
    mp = {'0': "0000", '1': "0001", '2': "0010", '3': "0011",
          '4': "0100", '5': "0101", '6': "0110", '7': "0111",
          '8': "1000", '9': "1001", 'A': "1010", 'B': "1011",
          'C': "1100", 'D': "1101", 'E': "1110", 'F': "1111"}
    bin_str = ""
    for char in s.upper():  # Added .upper() to handle lowercase hex
        bin_str += mp[char]
    return bin_str

# Function to convert binary to hex
def bin2hex(s):
    mp = {"0000": '0', "0001": '1', "0010": '2', "0011": '3',
          "0100": '4', "0101": '5', "0110": '6', "0111": '7',
          "1000": '8', "1001": '9', "1010": 'A', "1011": 'B',
          "1100": 'C', "1101": 'D', "1110": 'E', "1111": 'F'}
    hex_str = ""
    for i in range(0, len(s), 4):
        chunk = s[i:i + 4]
        if len(chunk) == 4:  # Ensure we have a full 4-bit chunk
            hex_str += mp[chunk]
    return hex_str

# Function to permute bits - FIXED to handle index errors
def permute(k, arr, n):
    permutation = ""
    for i in range(n):
        if arr[i] - 1 < len(k):  # Added check to prevent index errors
            permutation += k[arr[i] - 1]
        else:
            # If index is out of range, add a padding bit (0)
            permutation += "0"
    return permutation

# Function to perform left shift
def shift_left(k, nth_shifts):
    return k[nth_shifts:] + k[:nth_shifts]

# Function to XOR two strings
def xor(a, b):
    return "".join(['0' if i == j else '1' for i, j in zip(a, b)])

# S-boxes
sbox = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

# Function to generate keys
def generate_keys(key):
    key = hex2bin(key)
    
    # Ensure key is 64 bits (16 hex characters)
    if len(key) < 64:
        key = key.zfill(64)
    elif len(key) > 64:
        key = key[:64]
    
    # Permuted Choice 1 (PC-1)
    pc1 = [57, 49, 41, 33, 25, 17, 9,
           1, 58, 50, 42, 34, 26, 18,
           10, 2, 59, 51, 43, 35, 27,
           19, 11, 3, 60, 52, 44, 36,
           63, 55, 47, 39, 31, 23, 15,
           7, 62, 54, 46, 38, 30, 22,
           14, 6, 61, 53, 45, 37, 29,
           21, 13, 5, 28, 20, 12, 4]
    
    # Permuted Choice 2 (PC-2)
    pc2 = [14, 17, 11, 24, 1, 5,
           3, 28, 15, 6, 21, 10,
           23, 19, 12, 4, 26, 8,
           16, 7, 27, 20, 13, 2,
           41, 52, 31, 37, 47, 55,
           30, 40, 51, 45, 33, 48,
           44, 49, 39, 56, 34, 53,
           46, 42, 50, 36, 29, 32]
    
    # Key schedule shift table
    shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    
    # Perform PC-1
    key = permute(key, pc1, 56)
    
    # Split the key into left and right halves
    left = key[:28]
    right = key[28:]
    
    round_keys = []
    for i in range(16):
        # Perform left shifts
        left = shift_left(left, shift_table[i])
        right = shift_left(right, shift_table[i])
        
        # Combine halves and apply PC-2 to generate each round key
        combined = left + right
        round_keys.append(permute(combined, pc2, 48))
    
    return round_keys

# Encryption function
def encrypt(pt, rkb):
    # Initial Permutation (IP)
    ip = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]
    
    # Final Permutation (FP)
    fp = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]
    
    # Expansion Table
    exp_d = [32, 1, 2, 3, 4, 5, 4, 5,
             6, 7, 8, 9, 8, 9, 10, 11,
             12, 13, 12, 13, 14, 15, 16, 17,
             16, 17, 18, 19, 20, 21, 20, 21,
             22, 23, 24, 25, 24, 25, 26, 27,
             28, 29, 28, 29, 30, 31, 32, 1]
    
    # Straight Permutation Table
    per = [16, 7, 20, 21, 29, 12, 28, 17,
           1, 15, 23, 26, 5, 18, 31, 10,
           2, 8, 24, 14, 32, 27, 3, 9,
           19, 13, 30, 6, 22, 11, 4, 25]
    
    # Convert plaintext to binary and ensure it's 64 bits
    pt = hex2bin(pt)
    if len(pt) < 64:
        pt = pt.zfill(64)
    elif len(pt) > 64:
        pt = pt[:64]
        
    # Perform initial permutation
    pt = permute(pt, ip, 64)
    
    # Split plaintext into left and right halves
    left = pt[:32]
    right = pt[32:]
    
    print(f"Initial L0: {bin2hex(left)}, R0: {bin2hex(right)}")
    
    # Perform 16 rounds
    for i in range(16):
        # Expand the right half using expansion table
        right_expanded = permute(right, exp_d, 48)
        
        # XOR with round key
        x = xor(right_expanded, rkb[i])
        
        # S-box substitution
        sbox_str = ""
        for j in range(8):
            row = int(x[j * 6] + x[j * 6 + 5], 2)
            col = int(x[j * 6 + 1:j * 6 + 5], 2)
            val = sbox[j][row][col]
            sbox_str += bin(val)[2:].zfill(4)
        
        # Straight permutation
        sbox_str = permute(sbox_str, per, 32)
        
        # XOR with left half and swap
        result = xor(left, sbox_str)
        left = right
        right = result
        
        print(f"Round {i + 1}: L{i + 1}: {bin2hex(left)}, R{i + 1}: {bin2hex(right)}")
    
    # Combine halves and apply FP
    combined = right + left
    cipher_text = permute(combined, fp, 64)
    
    return bin2hex(cipher_text)

# Main DES function
def des_encrypt(plaintext, key):
    # Generate round keys
    round_keys = generate_keys(key)
    
    # Encrypt the plaintext
    cipher_text = encrypt(plaintext, round_keys)
    
    return cipher_text

# Function to decrypt using DES
def decrypt(ct, rkb):
    # Initial Permutation (IP)
    ip = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]
    
    # Final Permutation (FP)
    fp = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]
    
    # Expansion Table
    exp_d = [32, 1, 2, 3, 4, 5, 4, 5,
             6, 7, 8, 9, 8, 9, 10, 11,
             12, 13, 12, 13, 14, 15, 16, 17,
             16, 17, 18, 19, 20, 21, 20, 21,
             22, 23, 24, 25, 24, 25, 26, 27,
             28, 29, 28, 29, 30, 31, 32, 1]
    
    # Straight Permutation Table
    per = [16, 7, 20, 21, 29, 12, 28, 17,
           1, 15, 23, 26, 5, 18, 31, 10,
           2, 8, 24, 14, 32, 27, 3, 9,
           19, 13, 30, 6, 22, 11, 4, 25]
    
    # Convert ciphertext to binary and ensure it's 64 bits
    ct = hex2bin(ct)
    if len(ct) < 64:
        ct = ct.zfill(64)
    elif len(ct) > 64:
        ct = ct[:64]
        
    # Perform initial permutation
    ct = permute(ct, ip, 64)
    
    # Split ciphertext into left and right halves
    left = ct[:32]
    right = ct[32:]
    
    print(f"Initial L0: {bin2hex(left)}, R0: {bin2hex(right)}")
    
    # Perform 16 rounds in reverse order
    for i in range(16):
        # Expand the right half using expansion table
        right_expanded = permute(right, exp_d, 48)
        
        # XOR with round key (in reverse order)
        x = xor(right_expanded, rkb[15 - i])
        
        # S-box substitution
        sbox_str = ""
        for j in range(8):
            row = int(x[j * 6] + x[j * 6 + 5], 2)
            col = int(x[j * 6 + 1:j * 6 + 5], 2)
            val = sbox[j][row][col]
            sbox_str += bin(val)[2:].zfill(4)
        
        # Straight permutation
        sbox_str = permute(sbox_str, per, 32)
        
        # XOR with left half and swap
        result = xor(left, sbox_str)
        left = right
        right = result
        
        print(f"Round {i + 1}: L{i + 1}: {bin2hex(left)}, R{i + 1}: {bin2hex(right)}")
    
    # Combine halves and apply FP
    combined = right + left
    plain_text = permute(combined, fp, 64)
    
    return bin2hex(plain_text)

# Main DES decryption function
def des_decrypt(ciphertext, key):
    # Generate round keys
    round_keys = generate_keys(key)
    
    # Decrypt the ciphertext
    plain_text = decrypt(ciphertext, round_keys)
    
    return plain_text

# Example usage
# key = "AABB09182736CCDD"  # Example key (16 hex characters)
# plaintext = "123456ABCD132536"  # Example plaintext (16 hex characters)
# cipher = des_encrypt(plaintext, key)
# print("Cipher Text: ", cipher)
# decrypted_text = des_decrypt(cipher, key)
# print("Decrypted Text: ", decrypted_text)