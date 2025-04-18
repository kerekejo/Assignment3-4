def read_ints_from_file(filename):
    with open(filename, 'r') as file:  
        content = file.read().strip()  
        return int(content)

def read_ints_from_file_split(filename):
    with open(filename, 'r') as file:  
        content = file.read().strip()  
        content = content.split(",")
        content = [int(x) for x in content]
    return content

def readCiphertext(filename):
    with open(filename, 'r') as file:
        list = []
        fileList = file.readlines()
        for line in fileList:
            line = line.split()
            list.append([int(line[0]), int(line[1]), int(line[2]), int(line[3])])
        return list

def ec_add(P, Q, a, p):
    """Elliptic curve point addition: P + Q"""
    if P is None:  # P is point at infinity
        return Q
    if Q is None:  # Q is point at infinity
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and y1 == (-y2 % p):  # P = -Q
        return None  # Point at infinity
    
    if P == Q:  # Point doubling
        if y1 == 0:  # Point at infinity
            return None
        # Slope for doubling: m = (3x^2 + a) / (2y)
        m = ((3 * x1 * x1 + a) * pow(2 * y1, -1, p)) % p
    else:
        # Slope for addition: m = (y2 - y1) / (x2 - x1)
        if x2 == x1:  # Points are vertically aligned
            return None
        m = ((y2 - y1) * pow(x2 - x1, -1, p)) % p
    
    # x3 = m^2 - x1 - x2
    x3 = (m * m - x1 - x2) % p
    # y3 = m(x1 - x3) - y1
    y3 = (m * (x1 - x3) - y1) % p
    
    return (x3, y3)

def ec_subtract(P, Q, a, p):
    """Elliptic curve point subtraction: P - Q"""
    if Q is None:  # Q is point at infinity
        return P
    if P is None:  # P is point at infinity
        return (Q[0], -Q[1] % p)  # Return -Q
    # Subtraction: P - Q = P + (-Q)
    Q_neg = (Q[0], -Q[1] % p)  # Negate y-coordinate
    return ec_add(P, Q_neg, a, p)

def ec_multiply(P, k, a, p):
    """Elliptic curve scalar multiplication: k * P"""
    if k == 0 or P is None:
        return None  # Point at infinity
    if k < 0:
        P = (P[0], -P[1] % p)  # Negate point
        k = -k
    
    # Double-and-add algorithm
    result = None
    temp = P
    while k:
        if k & 1:  # If k is odd, add temp to result
            result = ec_add(result, temp, a, p)
        temp = ec_add(temp, temp, a, p)  # Double temp
        k >>= 1
    
    return result

def decryptCipherText(cipherText, a, b, bigP, G, n, p):
    """Decrypt EC ElGamal ciphertext using private key n"""
    decrypted = []
    for c1, c2, c3, c4 in cipherText:
        # Ciphertext format: (c1, c2, c3, c4) = (x1, y1, x2, y2)
        # (x1, y1) = kG (ephemeral key), (x2, y2) = M + kP (message + mask)
        # Private key n, public key P = nG
        # Compute kP = n * (x1, y1)
        kP = ec_multiply((c3, c4), n, a, p)
        # Recover message M = (x1, y2) - kP
        M = ec_subtract((c1, c2), kP, a, p)
        if M is not None:
            # Convert x-coordinate to ASCII (assuming message is encoded in x-coordinate)
            decrypted.append(chr(M[0] % 256))  # Mod 256 to map to ASCII
        else:
            decrypted.append('?')  # Handle invalid points
    return ''.join(decrypted)

# Read parameters
A = read_ints_from_file(r"C:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment4\A.txt")
B = read_ints_from_file(r"C:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment4\B.txt")
bigP = read_ints_from_file_split(r"C:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment4\bigP.txt")
G = read_ints_from_file_split(r"C:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment4\G.txt")
N = read_ints_from_file(r"C:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment4\N.txt")
p = read_ints_from_file(r"C:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment4\p.txt")
cipherText = readCiphertext(r"C:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment4\cipherTextH.txt")

# Decrypt and print result
print(decryptCipherText(cipherText, A, B, bigP, G, N, p))
    
