import argparse
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def encrypt(file, passcode):
    # Generate a key from the passcode using PBKDF2
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    key = base64.urlsafe_b64encode(kdf.derive(passcode.encode()))

    # Read the file and encrypt its contents
    with open(file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    # Write the encrypted data to the same file
    with open(file, 'wb') as f:
        f.write(salt + encrypted_data)

def decrypt(file, passcode):
    # Read the file and retrieve the salt and encrypted data
    with open(file, 'rb') as f:
        data = f.read()
    salt = data[:16]
    encrypted_data = data[16:]

    # Generate the key from the passcode using the salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    key = base64.urlsafe_b64encode(kdf.derive(passcode.encode()))

    # Decrypt the data using the key
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)

    # Write the decrypted data to the same file
    with open(file, 'wb') as f:
        f.write(decrypted_data)

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--encrypt', dest='action', action='store_const', const=encrypt)
    parser.add_argument('--decrypt', dest='action', action='store_const', const=decrypt)
    parser.add_argument('file')
    parser.add_argument('--code', required=True)
    args = parser.parse_args()

    # Perform the specified action (encrypt or decrypt) on the file
    args.action(args.file, args.code)
