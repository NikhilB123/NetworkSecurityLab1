import sqlite3
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sys
import base64
from itertools import product
from string import ascii_lowercase
def main():	
	numArguments = len(sys.argv)
	foundPassword = False
	if numArguments == 2:
		passwordData = sys.argv[1].split('$')
		if int(passwordData[1]) != 1:
			print("Cannot brute-force password in time.")
		else:
			decodedPassword = base64.b64decode(passwordData[3])
			for iteration in range(1, 5):
				for i in product(ascii_lowercase, repeat = iteration):
					word = ''.join(i)
					hashedPass = passwordHash(word, passwordData[2], int(passwordData[1]))
					if hashedPass == decodedPassword:
						print('Password cracked: ' + word)
						foundPassword = True
			if not foundPassword:
				print('Password not cracked.')

	else:
		db = sqlite3.connect('db.sqlite3')
		cursor = db.cursor()
		cursor.execute("SELECT * from auth_user")
		passwordData = cursor.fetchall()
		commonPasswords = [
        "123456",
        "123456789",
        "qwerty",
        "password",
        "1234567",
        "12345678",
        "12345",
        "iloveyou",
        "111111",
        "123123",
        "abc123",
        "qwerty123",
        "1q2w3e4r",
        "admin",
        "qwertyuiop",
        "654321",
        "555555",
        "lovely",
        "7777777",
        "welcome",
        "888888",
        "princess",
        "dragon",
        "password1",
        "123qwe"]

		for x in commonPasswords:
			for password in passwordData:
				user = password[4]
				passInfo = password[1].split('$')
				hashedPass = passwordHash(x, passInfo[2], int(passInfo[1]))
				if hashedPass == base64.b64decode(passInfo[3]):
					print(user + "," + x)	

def passwordHash(password, passSalt, iters):
	saltInBytes = bytes(passSalt, 'ascii')
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=saltInBytes,
		iterations=iters,
	)
	key = kdf.derive(bytes(password, 'ascii'))
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=saltInBytes,
		iterations=iters,
	)
	kdf.verify(bytes(password, 'ascii'), key)
	return key



if __name__ == "__main__":
	main()