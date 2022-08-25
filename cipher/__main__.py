import os
import time

from . import ui
from .utilities import get_input, encrypt, write_private_key, write_public_key, decrypt, check_for_keys

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

def main():
	print('Pls wait while a few program checks are being carried out')
	keys = check_for_keys()
	start = time.perf_counter()
	priv_key_generated = False
	if not keys:
		private_key = rsa.generate_private_key(
			public_exponent=65537,
			key_size=9216,
			backend=default_backend()
		)
		priv_key_generated = True
	end = time.perf_counter()
	total = end-start
	os.system('cls' if os.name == "nt" else 'clear')
	ui.initialise_cipher(total, priv_key_generated)
	encryptOrDecrypt = get_input('Do you wanna encrypt or decrypt: ', ['encrypt', 'decrypt'])
	if encryptOrDecrypt.lower() == "encrypt":
		filename = get_input('Enter the filename to encrypt(with the extension): ')
		write_private_key(private_key)
		write_public_key()
		encrypt(filename=filename)

	elif encryptOrDecrypt.lower() == "decrypt":
		print('Pls make sure you have the correct public and private keys in this folder(coz otherwise it wont work)')
		filename = get_input('Enter the filename to decrypt(with the extension): ')        
		decrypt(filename=filename)

main()
