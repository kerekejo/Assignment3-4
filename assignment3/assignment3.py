def read_ints_from_file(filename):
    with open(filename, 'r') as file:  
        content = file.read().strip()  
        return int(content)
    

def read_halfmaskcipher(filename):
    with open(filename, 'r') as file:  
        lineList  = []
        for line in file:
            line = line.strip()
            line = line.split(',')
            lineList.append((line[0],line[1]))
        return lineList
    
def decryptElGamal(halfMaskAndCipherList, a):
    decryptedString = ''
    for halfMask, cipher in halfMaskAndCipherList:
        halfMask = int(halfMask)
        cipher = int(cipher)
        decrypted = (cipher * pow(halfMask, -a, p)) % p
        decryptedString += chr(decrypted)
    return decryptedString

generator = read_ints_from_file(r'c:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment3\generator.txt')
p = read_ints_from_file(r'c:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment3\p.txt')
a = read_ints_from_file(r'c:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment3\a.txt')
mask = read_ints_from_file(r'c:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment3\mask.txt')
halfAndCipher = read_halfmaskcipher(r'c:\Users\Joe\OneDrive\Pictures\Desktop\CryptographyHomeworkII\assignment3\halfmask_cipher.txt')

print(decryptElGamal(halfAndCipher, a))