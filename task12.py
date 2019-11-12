#Chase Richards
#CS3780
#Project 2: Task 1 and Task 2

#https://cryptography.io/en/latest/random-numbers/ for random-numbers generation
import os
#https://cryptography.io/en/latest/ for hashing passwords
from cryptography.hazmat.backends import openssl
from cryptography.hazmat.primitives import hashes

def createAccount():
	#file will be determined by the number the user entered and opened for append/update
	fileChoice = passwordFileSelection()
	fileName = open(fileChoice, "a+")
	#initialize username and password to empty strings
	username = ""
	password = ""
	
	while True:
		#Have the user enter a username/password and check if it exists/isvalid
		username = input("Please enter a username - retricted to 8 alphanumeric characters: ")

		def checkIfAcctExists():
			with open(fileChoice) as f:
				data = f.readlines()
			for line in data:
				if username in line.split():
					return True
			return False
			
		if checkIfAcctExists():
			print("Username already exists")
		else:
			if len(username) <= 8 and len(username) and username.isalnum():
				print("Success")
				break
			else:
				print("Please enter a username that is retricted to 8 alphanumeric characters")
			
	while True:
		#Have the user enter a password and check if it isvalid
		password = input("Please enter a password - restricted to 3 to 8 lowercase letters: ")
		if len(password) >= 1 and len(password) <= 8 and password.islower() and password.isalpha():
			print("Success")
			break
		else:
			print("Please enter a password that is 3 to 8 lowercase letters")
	
	if fileChoice == "plaintextpsswrd.txt":
		fileName.write(username + " " + password + "\n")
		print("Added account to plaintextpsswrd.txt file")
	elif fileChoice == "hashedpsswrd.txt":
		passwordasBytes = password.encode("ascii")
		digest = hashes.Hash(hashes.SHA3_256(), backend = openssl.backend)
		digest.update(passwordasBytes)
		hashedpsswrd = digest.finalize()
		hashedpsswrd = hashedpsswrd.hex()
		fileName.write(username + " " + hashedpsswrd + "\n")
		print("Added account to hashedpsswrd.txt")
	elif fileChoice == "salthashedpsswrd.txt":
		salt = int.from_bytes(os.urandom(1), byteorder="big")
		salt = salt % (122 - 97 + 1) + 97
		newSalt = chr(salt)
		saltyPassword = password + newSalt
		saltpasswrdasBytes = saltyPassword.encode("ascii")
		digest = hashes.Hash(hashes.SHA3_256(), backend = openssl.backend)
		digest.update(saltpasswrdasBytes)
		salthashedpsswrd = digest.finalize()
		salthashedpsswrd = salthashedpsswrd.hex()
		fileName.write(username + " " + salthashedpsswrd + " " + newSalt + "\n")
		print("Added account to salthashedpsswrd.txt")
		
def login():
	fileChoice = passwordFileSelection()
	fileName = open(fileChoice, "r")
	print("Enter your login credentials below: \n")
	username = input("Username: ")
	password = input("Password: ")
	
	with open(fileChoice) as f:
		data = f.readlines()
	for line in data:
		if username in line.split():
			print("Username found in file: " + fileChoice)
			
			if fileChoice == "plaintextpsswrd.txt":
				userPassword = line.split(" ", 1)[1]
				passwordwithNewLine = password + '\n'
				if userPassword == passwordwithNewLine:
					print("Successful Login")
				else:
					print("Failed Login")
				return
			elif fileChoice == "hashedpsswrd.txt":
				passwordasBytes = password.encode("ascii")
				digest = hashes.Hash(hashes.SHA3_256(), backend = openssl.backend)
				digest.update(passwordasBytes)
				hashedpsswrd = digest.finalize()
				hashedpsswrd = hashedpsswrd.hex()
				userPassword = line.split(" ", 1)[1]
				passwordwithNewLine = hashedpsswrd + '\n'
				if userPassword == passwordwithNewLine:
					print("Successful Login")
				else:
					print("Failed Login")
				return
			elif fileChoice == "salthashedpsswrd.txt":
				userSalt = line.split(" ", 2)[2]
				saltwithNewLine = userSalt + '\n'
				saltyPassword = password + saltwithNewLine
				saltypasswordasBytes = saltyPassword.encode("ascii")
				digest = hashes.Hash(hashes.SHA3_256(), backend = openssl.backend)
				digest.update(saltypasswordasBytes)
				salthashedpsswrd = digest.finalize()
				salthashedpsswrd = salthashedpsswrd.hex()
				userPassword = line.split(" ", 2)[1]
				if userPassword == userPassword:
					print("Successful Login")
				else:
					print("Failed Login")
				
		else:
			print("Username does not exist in this file")
			
def accountGeneration():
	numberofAccounts = int(input("Enter the number of accounts to generate: "))
	minLength = int(input("Enter the minimum password length: "))
	maxLength = int(input("Enter the maximum password length: "))
	
	if numberofAccounts < 0 or numberofAccounts > 1000:
		print("Please enter number of accounts between 1 and 1000 - including 1000")
	elif minLength <= 0 or minLength > maxLength:
		print("Please enter min password length greater than 0 and less than max password length")
	elif maxLength <= 0 or maxLength > 64:
		print("Please enter a max password length greater than 0 and less than or equal to 64")
	else:
		#Open the password files for writing or create them if they have not already been created
		plaintextpsswrdFile = open("plaintextpsswrd.txt", "w")
		hashedpsswrdFile = open("hashedpsswrd.txt", "w")
		salthashedpsswrdFile = open("salthashedpsswrd.txt", "w")
		#Generate the users for i in range of 0 to numberofAccounts
		for i in range(numberofAccounts):
			username = "user" + str(i)
			#create password using a random string of random lower case letters
			ranPsswrdString = ""
			ranPsswrdStringLength = int.from_bytes(os.urandom(1), byteorder="big")
			ranPsswrdStringLength = ranPsswrdStringLength % (maxLength - minLength + 1) + minLength
			for i in range(ranPsswrdStringLength):
				randlowercase = int.from_bytes(os.urandom(1), byteorder="big")
				randlowercase = randlowercase % (122 - 97 + 1) + 97
				randlowercase = chr(randlowercase)
				ranPsswrdString += randlowercase		
			
			#Hash the password without using a salt
			passwordasBytes = ranPsswrdString.encode("ascii")	
			digest1 = hashes.Hash(hashes.SHA3_256(), backend = openssl.backend)
			digest1.update(passwordasBytes)
			hashedpsswrd = digest1.finalize()
			hashedpsswrd = hashedpsswrd.hex()
			print("Hashed Password: " + hashedpsswrd)
			
			#Generate random salt
			salt = int.from_bytes(os.urandom(1), byteorder="big")
			salt = salt % (122 - 97 + 1) + 97
			salt = chr(salt)
			print(username)
			print(salt)
			print(ranPsswrdString)
			saltyPassword = ranPsswrdString + salt
			
			#Password hash using the generated salt
			saltypasswordasBytes = saltyPassword.encode("ascii")
			digest1 = hashes.Hash(hashes.SHA3_256(), backend = openssl.backend)
			digest1.update(saltypasswordasBytes)
			salthashedpsswrd = digest1.finalize()
			salthashedpsswrd = salthashedpsswrd.hex()
			print("Salt Hashed Password: " + salthashedpsswrd)
			
			plaintextpsswrdFile.write(username + " " + ranPsswrdString + "\n")
			hashedpsswrdFile.write(username + " " + hashedpsswrd + "\n")
			salthashedpsswrdFile.write(username + " " + salthashedpsswrd + " " + salt + "\n")
		
def passwordFileSelection():
	while True:
		selection = input("Please enter the number for the username/password file you would like to authenticate through: \n 1.Plaintext username password pair \n 2.Username and a hashed password \n 3.Username, a salt and the result of the hashed(password+salt)\n")
		if selection == "1":
			return "plaintextpsswrd.txt"
		elif selection == "2":
			return "hashedpsswrd.txt"
		elif selection == "3":
			return "salthashedpsswrd.txt"
		elif selection == "exit":
			break
		else:
			print("Please enter 1, 2, or 3")

while True:
	selection = input("\nPlease enter the number of whether you would like to create an account or login: \n 1.Create Account \n 2.Login \n 3.Generate Random Accounts\n")
	if selection == "1":
		createAccount()
	elif selection == "2":
		login()
	elif selection == "3":
		accountGeneration()
	elif selection == "exit":
		break
	else:
		print("Please enter 1 or 2")