from os.path import isfile
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

public_key = None

def check_for_keys():
    if isfile('private.pem') and isfile('public.pem'):
        return True
    return False

def write_private_key(private_key : rsa.RSAPrivateKeyWithSerialization):
    global public_key
    pk = private_key.public_key()
    public_key = pk
    with open('private.pem', 'wb') as f:
        f.truncate()
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

def write_public_key():
    with open('public.pem', 'wb') as f:
        f.truncate()
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
        
def get_input(prompt, options : list = None):
    while 1:
        text = input(prompt)
        if not text or options and text not in options:
            print('Invalid input, try again')
            continue
        
        return text

def write(filename, content):
    if not isfile(filename):
        print('No file found ._.')

    with open(filename, 'wb') as f:
        f.write(content)

def load_private_key() -> rsa.RSAPrivateKeyWithSerialization:
    if not isfile('private.pem'):
        print('No private key found, cannot decrypt')
    with open('private.pem', 'rb') as f:
        private_key = serialization.load_pem_private_key(
            data=f.read(),
            password=None,
            backend=default_backend()
        )

    return private_key

def load_public_key() -> rsa.RSAPublicKeyWithSerialization:
    if not isfile('public.pem'):
        print('No public key found, cannot decrypt')
    with open('public.pem', 'rb') as f:
        public_key = serialization.load_pem_public_key(
            data=f.read(),
            backend=default_backend()
        )

    return public_key

def encrypt(filename):
    if not isfile(filename):
        print('No file found ._.')
    pk = load_public_key()
    with open(filename, 'r') as f:
        data = f.read().encode()
        data = pk.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )

    write(filename, data)

def decrypt(filename):
    if not isfile(filename):
        print('No file found ._.')

    pk = load_private_key()
    with open(filename, 'rb') as f:
        plaintext = pk.decrypt(
            f.read(),
            padding.OAEP(
                padding.MGF1(hashes.SHA1()),
                hashes.SHA1(),
                label=None
            )
        )
    write(filename, plaintext)