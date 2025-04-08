import time
import random
import string

# Simplified SHA-128-like hash function (educational only)
def sha128_custom(message: str) -> str:
    hash_val = 0x12345678
    for char in message:
        hash_val = ((hash_val << 7) ^ (hash_val >> 3)) + ord(char)
        hash_val = hash_val & 0xFFFFFFFF
    return hex(hash_val)[2:].zfill(8)

# Simplified SHA-256-like hash function (educational only)
def sha256_custom(message: str) -> str:
    hash_val = 0xabcdef01
    for char in message:
        hash_val = ((hash_val << 13) ^ (hash_val >> 5)) + ord(char)
        hash_val = hash_val & 0xFFFFFFFF
    return hex(hash_val)[2:].zfill(8)

# Manual HMAC implementation using custom hash
def hmac_custom(key: str, message: str, hash_func, block_size=64) -> str:
    if len(key) > block_size:
        key = hash_func(key)
    key = key.ljust(block_size, '\x00')

    o_key_pad = ''.join(chr(ord(c) ^ 0x5c) for c in key)
    i_key_pad = ''.join(chr(ord(c) ^ 0x36) for c in key)

    return hash_func(o_key_pad + hash_func(i_key_pad + message))

# Generate a random alphanumeric message of given length
def generate_random_message(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Performance and result test
def test_hmac_performance():
    key = "secret_key"
    sizes = [10, 100, 1000, 5000, 10000]

    print(f"{'Size':<8} | {'SHA-128 HMAC':<15} | {'Time (ms)':<10} | {'SHA-256 HMAC':<15} | {'Time (ms)':<10}")
    print("-" * 70)

    for size in sizes:
        message = generate_random_message(size)

        # SHA-128
        start = time.time()
        hmac_sha128 = hmac_custom(key, message, sha128_custom)
        sha128_time = (time.time() - start) * 1000

        # SHA-256
        start = time.time()
        hmac_sha256 = hmac_custom(key, message, sha256_custom)
        sha256_time = (time.time() - start) * 1000

        print(f"{size:<8} | {hmac_sha128:<15} | {sha128_time:<10.3f} | {hmac_sha256:<15} | {sha256_time:<10.3f}")

if __name__ == "__main__":
    test_hmac_performance()
