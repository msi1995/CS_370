import os
import cryptography
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends.openssl.backend import backend
import binascii



def find_key():
    f1 = open('plaintext.txt', 'r')
    f2 = open ('ciphertext.txt', 'r')
    plaintext = f1.read()
    known_ciphertext = f2.read()

    if len(plaintext) != 21:
        plaintext.rstrip()

    plaintext = plaintext.encode("utf-8")
    plaintext = plaintext + b'\x0b' * 11
    iv = b'\x00' * 16

    with open('words.txt') as dictionary:
        for word in dictionary:
            word = word.rstrip()
            if len(word) < 16:
                padAmount = 16 - len(word)
                padding = ' ' * padAmount
                key = word + padding
                cipher = Cipher(algorithms.AES(key.encode("utf-8")), modes.CBC(iv), backend)
                encryptor = cipher.encryptor()
                ciphertext = encryptor.update(plaintext)
                # print("text before .hex(): ", ciphertext)
                # print('Hexadecimal: ', binascii.hexlify(ciphertext).decode("utf-8"))
                ciphertext_hex = binascii.hexlify(ciphertext).decode("utf-8")
                # ciphertext_hex = ciphertext.hex()
                print("Checking " + ciphertext_hex + "...")
                if ciphertext_hex == known_ciphertext:
                    return word

    print("\nNo key was found. Exiting.")
    exit(0)

if __name__ == '__main__':
    the_key = find_key()
    print("\n\nKEY FOUND!\nKEY: " + the_key)


