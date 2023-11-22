import hashlib

def MD5_hash(password):
    return str(hashlib.md5(password.encode()).digest())