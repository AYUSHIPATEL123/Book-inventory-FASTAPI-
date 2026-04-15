from passlib.context import CryptContext

pass_context = CryptContext(schemes=["argon2"],deprecated="auto")

def hash_pass(password:str):
    return pass_context.hash(password)

def verify_pass(password:str,hashed_pass:str) -> bool:
    return pass_context.verify(password,hashed_pass)

