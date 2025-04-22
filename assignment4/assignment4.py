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
    if P is None:  
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and y1 == (-y2 % p):  # P = -Q
        return None 
    
    if P == Q:
        if y1 == 0:  
            return None
        m = ((3 * x1 * x1 + a) * pow(2 * y1, -1, p)) % p
    else:
        if x2 == x1:
            return None
        m = ((y2 - y1) * pow(x2 - x1, -1, p)) % p
    

    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    
    return (x3, y3)

def ec_subtract(P, Q, a, p):
    if Q is None: 
        return P
    if P is None:  
        return (Q[0], -Q[1] % p)  

    Q_neg = (Q[0], -Q[1] % p) 
    return ec_add(P, Q_neg, a, p)

def ec_multiply(P, k, a, p):
    if k == 0 or P is None:
        return None  
    if k < 0:
        P = (P[0], -P[1] % p)  
        k = -k
    
  
    result = None
    temp = P
    while k:
        if k & 1:  
            result = ec_add(result, temp, a, p)
        temp = ec_add(temp, temp, a, p) 
        k >>= 1
    
    return result

def decryptCipherText(cipherText, a, b, bigP, G, n, p):
    decrypted = []
    for c1, c2, c3, c4 in cipherText:
        kP = ec_multiply((c3, c4), n, a, p)
        M = ec_subtract((c1, c2), kP, a, p)
        if M is not None:
            decrypted.append(chr(M[0] % 256)) 
        else:
            decrypted.append('?')  
    return ''.join(decrypted)

A = read_ints_from_file(r"C:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment4\A.txt")
B = read_ints_from_file(r"C:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment4\B.txt")
bigP = read_ints_from_file_split(r"C:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment4\bigP.txt")
G = read_ints_from_file_split(r"C:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment4\G.txt")
N = read_ints_from_file(r"C:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment4\N.txt")
p = read_ints_from_file(r"C:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment4\p.txt")
cipherText = readCiphertext(r"C:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment4\cipherTextH.txt")

print(decryptCipherText(cipherText, A, B, bigP, G, N, p))
    
