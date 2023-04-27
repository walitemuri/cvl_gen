from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pwd(passwd: str):
    return  pwd_context.hash(passwd)

def verify_pwd(passwd, hashed_password):
    return pwd_context.verify(passwd, hashed_password)