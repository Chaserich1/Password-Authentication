#Chase Richards
#CS3780
#Project 2: Task 3

import itertools
import string
import os
import time
from cryptography.hazmat.backends import openssl
from cryptography.hazmat.primitives import hashes

def crackHashPassword(userPassword):	
    passwordasBytes = string.ascii_lowercase
    numOfPasswordcurrentPasswordGuesses = 0
    passwordLength = 0
    for passwordLength in range(1, 8):
        for currentPasswordGuess in itertools.product(passwordasBytes, repeat = passwordLength):
            numOfPasswordcurrentPasswordGuesses += 1
            currentPasswordGuess = ''.join(currentPasswordGuess)
            def passwordEncrypt(hashedString):
                passwordasBytes = hashedString.encode("ascii")
                digest = hashes.Hash(hashes.SHA3_256(), backend = openssl.backend)
                digest.update(passwordasBytes)
                hashedpsswrd = digest.finalize()
                hashedpsswrd = hashedpsswrd.hex()
                hashpasswordwithNewLine = hashedpsswrd + '\n'
                return hashpasswordwithNewLine
            hashedString = currentPasswordGuess
            hashedpsswrd = passwordEncrypt(hashedString)
            print(hashedpsswrd)
            userPassword = line.split(" ", 1)[1]
            if hashedpsswrd == userPassword:
                return 'It took {} guesses to crack the Hash password: {}'.format(numOfPasswordcurrentPasswordGuesses,currentPasswordGuess)
            print (currentPasswordGuess,numOfPasswordcurrentPasswordGuesses)

def crackSaltHashPassword(userSaltedPassword):	
    saltypasswordasBytes = string.ascii_lowercase
    saltnumOfPasswordcurrentPasswordGuesses = 0
    passwordLength = 0
    for passwordLength in range(1, 8):
        for currentPasswordGuess in itertools.product(saltypasswordasBytes, repeat = passwordLength):
            saltnumOfPasswordcurrentPasswordGuesses += 1
            currentPasswordGuess = ''.join(currentPasswordGuess)
            def passwordEncrypt(hashedString):
                saltypasswordasBytes = hashedString.encode("ascii")
                digest = hashes.Hash(hashes.SHA3_256(), backend = openssl.backend)
                digest.update(saltypasswordasBytes)
                salthashedpsswrd = digest.finalize()
                salthashedpsswrd = salthashedpsswrd.hex()
                saltpasswordwithNewLine = salthashedpsswrd
                return saltpasswordwithNewLine
            hashedString = currentPasswordGuess + salt
            salthashedpsswrd = passwordEncrypt(hashedString)
            print(salthashedpsswrd)
            userSaltedPassword = line.split(" ", 2)[1]
            if salthashedpsswrd == userSaltedPassword:
                return 'It took {} guesses to crack the Hash + Salt password: {}'.format(saltnumOfPasswordcurrentPasswordGuesses,currentPasswordGuess)
            print (currentPasswordGuess,saltnumOfPasswordcurrentPasswordGuesses)

while True:
    selection = input("Please choose which password you would like to crack: \n1.Hash \n2.Hash + Salt \n")
    if selection == "1":
        start = time.time()
        with open('hashedpsswrd.txt') as f:
            line = f.readline()
        hashLine = line.rpartition(' ')[1]
        hashLine = hashLine.replace('\n','')
        print(crackHashPassword(hashLine))
        end = time.time()
        print(end - start)
    elif selection == "2":
        start = time.time()
        with open('salthashedpsswrd.txt') as f:
            line = f.readline()
        hashSaltLine = line.rpartition(' ')[2]
        salt = line.rpartition(' ')[2]
        salt = salt.replace('\n','')
        line = line.rpartition(' ')[0]
        hashSaltLine = line.rpartition(' ')[2]
        hashSaltLine = hashSaltLine.replace('\n','')
        print(crackSaltHashPassword(hashSaltLine))
        end = time.time()
        print(end - start)
    elif selection == "exit":
        break
    else:
        print("Please enter 1, 2 or exit")

