def gcd(a,b):
    while b!=0:
        a,b = b,a%b
    return a
def modinv(a,m):
    m0,x0,x1 = m,0,1
    if m==1:
        return 0
    while a>1:
        q = a//m
        a,m = m,a%m
        x0,x1 = x1-q*x0,x0
    return x1 + m0 if x1<0 else x1

def isPrime(n):
    if n<=1: return False
    for i in range(2,n):
        if n%i ==0:
            return False
    return True

def generateKeypair(p,q):
    if not (isPrime(p) and isPrime(q)):
        return ValueError("Both numbers should be prime")
    n = p*q
    phi = (p-1) * (q-1)
    e = 3
    while gcd(e,phi) !=1:
        e+=2
    d = modinv(e,phi)
    return ((e,n),(d,n))

def encrypt(pk,plaintext):
    key,n = pk
    return [pow(ord(char),key,n) for char in plaintext]

def decrypt(pk,ciphertext):
    key,n = pk
    return ''.join([chr(pow(char,key,n)) for char in ciphertext])
    
    