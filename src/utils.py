import random
import string
import hashlib


def get_random_char_id(n=14):
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(n))


def hash_password(password):
    return hashlib.sha256(bytes(password, "utf8")).hexdigest()


