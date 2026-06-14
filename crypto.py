import hashlib as hash
import bcrypt as cry

def SenHash(senha):
    senhaBytes = senha.encode('utf-8')
    salzin = cry.gensalt()
    senhahash = cry.hashpw(senhaBytes, salzin)
    return senhahash

def Confia(SenhaDig, HashCerto):
    senhaByte = SenhaDig.encode('utf-8')
    HashCerto = HashCerto.encode('utf-8')
    if cry.checkpw(senhaByte, HashCerto):
        return True
    else:
        return False



