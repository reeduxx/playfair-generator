import numpy as np
from collections import OrderedDict
import argparse

def main():
    parser = argparse.ArgumentParser(description = "A command line tool to generate ciphertext using a Playfair matrix.")
    parser.add_argument("key", help = "Key used for the generation of the Playfair matrix.")
    parser.add_argument("phrase", help = "Word or phrase to encrypt with the Playfair cipher.")
    parser.add_argument("-m", "--Matrix", action="store_true", help = "Output Playfair matrix.")
    args = parser.parse_args()
    keyword = ''.join(OrderedDict.fromkeys(args.key.upper()))
    alphabet = sorted(set([chr(i) for i in range (65, 91) if chr(i) != 'J']) - set(keyword))
    matrix = np.array(list(keyword + ''.join(alphabet))).reshape(5, 5)
    
    if args.Matrix:
        for i in matrix:
            print(i)
    
    plaintext = expand_plaintext(args.phrase.upper())
    segments = [plaintext[i:i + 2] for i in range(0, len(plaintext), 2)]
    ciphertext = ''
    
    for segment in segments:
        encrypted_segment = encrypt_pair(segment, matrix)
        ciphertext += encrypted_segment
    
    print(ciphertext.translate({ord(i): None for i in "[']"}))

def expand_plaintext(plaintext):
    plaintext = ''.join(char for char in plaintext if char.isalpha())
    expanded_plaintext = ''
    prev_char = None
    
    for char in plaintext:
        if char == prev_char:
            expanded_plaintext += 'X'
        expanded_plaintext += char
        prev_char = char
    
    if len(expanded_plaintext) % 2 != 0:
        expanded_plaintext += 'X'
        
    return expanded_plaintext

def encrypt_pair(segment, matrix):
    row1, col1 = np.where(matrix == segment[0])
    row2, col2 = np.where(matrix == segment[1])
    encrypted_pair = ''
    
    if row1 == row2:
        encrypted_pair = str(matrix[row1, (col1 + 1) % 5]) + str(matrix[row2, (col2 + 1) % 5])
    elif col1 == col2:
        encrypted_pair = str(matrix[(row1 + 1) % 5, col1]) + str(matrix[(row2 + 1) % 5, col2])
    else:
        encrypted_pair = str(matrix[row1, col2]) + str(matrix[row2, col1])
    
    return encrypted_pair

if __name__ == '__main__':
    main()