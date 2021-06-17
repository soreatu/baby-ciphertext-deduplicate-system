import os

from internel.utils.aes import AES
from internel.utils.sha1 import SHA1

def key_gen(length):
    return os.urandom(length)

def save_key(password, key):
    aes = AES(SHA1(password.encode()).digest()[:16])
    cipher = aes.encrypt(key)
    with open("../key", "wb") as f:
        f.write(cipher)


def test():
    encrypt_key = key_gen(16)
    print(f"encrypt_key: {encrypt_key}")
    save_key("soreatu", encrypt_key)


if __name__ == "__main__":
    test()