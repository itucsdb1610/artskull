import hashlib
import random

class User:
    def __init__(self, username, passwd, email, name, surname, profpic):
        self.username = username
        self.salt = createSalt()
        self.hash = createHash(self.salt, passwd)
        self.email = email
        self.name = name
        self.surname = surname
        self.genres = genres
        self.profpic = profpic

def createSalt():
    ABECE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for i in range(16):
        chars.append(random.choice(ABECE))

    real_salt = "".join(chars)
    return real_salt

def createHash(salt, passwd):
    salted_password = passwd.join(salt)
    h = hashlib.md5(salted_password.encode())
    #print(h.hexdigest())
    return h.hexdigest()