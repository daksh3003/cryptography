import random
import math

# A set will store prime numbers, from which we will select random primes p and q.
prime = set()
public_key = None
private_key = None
n = None

def get_keys():
    return public_key, n

# Function to populate the prime number set using the Sieve of Eratosthenes.
def prime_filler():
    sieve = [True] * 250
    sieve[0] = sieve[1] = False  # 0 and 1 are not prime

    for i in range(2, 250):
        if sieve[i]:
            for j in range(i * 2, 250, i):
                sieve[j] = False

    # Filling the prime set with prime numbers
    for i in range(len(sieve)):
        if sieve[i]:
            prime.add(i)

# Function to pick a random prime and remove it from the set
def pick_random_prime():
    global prime
    k = random.randint(0, len(prime) - 1)
    it = iter(prime)
    for _ in range(k):
        next(it)
    ret = next(it)
    prime.remove(ret)
    return ret

# Function to generate public and private keys
def set_keys():
    global public_key, private_key, n
    prime1 = pick_random_prime()  # First prime number
    prime2 = pick_random_prime()  # Second prime number
    n = prime1 * prime2
    phi = (prime1 - 1) * (prime2 - 1)

    # Choosing public exponent e such that 1 < e < phi and gcd(e, phi) = 1
    e = 2
    while math.gcd(e, phi) != 1:
        e += 1
    public_key = e

    # Computing private key d such that (d * e) % phi = 1
    d = 2
    while (d * e) % phi != 1:
        d += 1
    private_key = d

# Function to encrypt a message
def encrypt(message, public_key, n):
    e = public_key
    encrypted_text = 1
    while e > 0:
        encrypted_text *= message
        encrypted_text %= n
        e -= 1
    return encrypted_text

# Function to decrypt an encrypted message
def decrypt(encrypted_text):
    global private_key, n
    d = private_key
    decrypted = 1
    while d > 0:
        decrypted *= encrypted_text
        decrypted %= n
        d -= 1
    return decrypted

# Function to encode a message (convert characters to ASCII and encrypt them)
def encoder(message, num1, num2):
    encoded = []
    for letter in message:
        encoded.append(encrypt(ord(letter), num1, num2))
    return encoded

# Function to decode an encoded message (decrypt numbers and convert back to characters)
def decoder(encoded):
    s = ""
    for num in encoded:
        s += chr(decrypt(num))
    return s
