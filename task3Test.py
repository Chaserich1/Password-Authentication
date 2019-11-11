import itertools
import string
import hashlib
from cryptography.hazmat.backends import openssl
from cryptography.hazmat.primitives import hashes
import os
import time
def guess_passwordHash(returnline):
	userPassword = line.split(":", 1)[1]
	chars = userPassword.encode("ascii")
	attempts = 0
	password_length = 0
	for password_length in range(3, 8):
		for guess in itertools.product(chars, repeat=password_length):
			attempts += 1
			guess = ''.join(guess)
			def encrypt_string(hash_string):
				digest = hashes.Hash(hashes.SHA3_256(), backend = openssl.backend)
				digest.update(chars)
				hashedpsswrd = digest.finalize()
				hashedpsswrd = hashedpsswrd.hex()
				return hashedpsswrd
			hash_string = guess
			hashedpsswrd = encrypt_string(hash_string)
			if hashedpsswrd == returnline:
				return 'password is {}. found in {} guesses.'.format(guess, attempts)
			print (guess,attempts)


def guess_passwordHashSalt(returnline):
    saltyPassword = line.split(":", 1)[1]
    chars = saltyPassword.encode("ascii")
    attempts = 0
    for password_length in range(3, 8):
        for guess in itertools.product(chars, repeat=password_length):
            attempts += 1
            guess = ''.join(guess)
            def encrypt_string(hash_string):
                digest = hashes.Hash(hashes.SHA3_256(), backend = openssl.backend)
                digest.update(chars)
                salthashedpsswrd = digest.finalize()
                salthashedpsswrd = salthashedpsswrd.hex()
                return sha_signature
            hash_string = guess + salt
            salthashedpsswrd = encrypt_string(hash_string)
            print(salthashedpsswrd)
            if salthashedpsswrd == returnline:
                return 'password is {}. found in {} guesses.'.format(guess, attempts)
            print (guess,attempts)

print("1.Hash \n")
print("2.Hash with salt\n")
user = input("Please pick an option 1 or 2: \n")
if user == "1":
    start = time.time()
    with open('hashedpsswrd.txt') as f:
        firstline = f.readline()
    returnline = firstline.rpartition(':')[2]
    returnline = returnline.replace('\n','')
    print(returnline)
    print(guess_passwordHash(returnline))
    end = time.time()
    print(end - start)
if user == "2":
    start = time.time()
    with open('salthashedpsswrd.txt') as f:
        firstline = f.readline()
    salt = firstline.rpartition(':')[2]
    salt = salt.replace('\n','')
    print(salt)
    firstline = firstline.rpartition(':')[0]
    returnline = firstline.rpartition(':')[2]
    returnline = returnline.replace('\n','')
    print(returnline)
    print(guess_passwordHashSalt(returnline))
    end = time.time()
    print(end - start)

