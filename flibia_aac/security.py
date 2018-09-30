import hashlib

def generate_hash_password(password):
    return hashlib.sha1(password.encode('ascii')).hexdigest()


def check_password(pwhash, password):
    # Very weak =/ (compatibility with forgottenserver password)
    return pwhash == generate_hash_password(password)