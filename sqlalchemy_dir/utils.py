from passlib.context import CryptContext
password_context = CryptContext(schemes=["bcrypt"])

def hashpass(password: str):
    return password_context.hash(password)

    #using the hashing algorithm specified as bcrypt, hash the user pass