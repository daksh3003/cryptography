import time
import hmac
import hashlib
import random
import string

def compute_hmac(message, key, algorithm='sha256'):
    """
    Compute HMAC for a given message and key using the specified algorithm.
    For algorithm 'sha256', it uses SHA-256.
    For algorithm 'sha128', we use MD5 (which produces a 128-bit digest) as a proxy.
    """
    key_bytes = key.encode()
    message_bytes = message.encode()

    if algorithm.lower() == 'sha256':
        h = hmac.new(key_bytes, message_bytes, hashlib.sha256)
    elif algorithm.lower() == 'sha128':
        # MD5 produces a 128-bit digest; note that MD5 is not part of the SHA family.
        h = hmac.new(key_bytes, message_bytes, hashlib.md5)
    else:
        raise ValueError("Unsupported algorithm. Use 'sha256' or 'sha128'.")

    return h.hexdigest()

def measure_time(message_size, algorithm='sha256', iterations=100):
    """
    Measures the average time taken to compute the HMAC for a randomly
    generated message of a given size.
    Repeats the computation 'iterations' times and returns the average duration.
    """
    key = "secretkey"
    total_time = 0.0

    for _ in range(iterations):
        # Generate a random message of length message_size
        message = ''.join(random.choices(string.ascii_letters + string.digits, k=message_size))
        
        start_time = time.perf_counter()
        compute_hmac(message, key, algorithm)
        end_time = time.perf_counter()
        
        total_time += (end_time - start_time)

    avg_time = total_time / iterations
    return avg_time

def main():
    message_sizes = [10, 100, 1000, 10000, 100000]
    algorithms = ['sha128', 'sha256']

    print("HMAC Time Measurements (average over 100 iterations):\n")

    for algo in algorithms:
        print(f"Algorithm: {algo.upper()}")
        for size in message_sizes:
            avg_duration = measure_time(size, algorithm=algo)
            print(f" Message size: {size:6d} bytes -> Average time: {avg_duration * 1e6:.2f} microseconds")
        print()

    # Example: Compute and display HMAC for a sample message.
    sample_message = "Hello, this is a test message."
    key = "secretkey"

    hmac_sha128 = compute_hmac(sample_message, key, 'sha128')
    hmac_sha256 = compute_hmac(sample_message, key, 'sha256')

    print("Sample HMAC Computation:")
    print(f"Message: {sample_message}")
    print(f"HMAC (SHA-128 using MD5): {hmac_sha128}")
    print(f"HMAC (SHA-256): {hmac_sha256}")

if __name__ == '__main__':
    main()
