import datetime
from fastapi_mail import FastMail, MessageSchema
from passlib.context import CryptContext
from jose import jwt
from . import schemas
from app.config import settings, EmailSettings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pwd(passwd: str):
    return  pwd_context.hash(passwd)

def verify_pwd(passwd, hashed_password):
    return pwd_context.verify(passwd, hashed_password)

def generate_email_token(user_id: int, email: str):
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    return jwt.encode(payload, settings.secret_key, settings.algorithm)

# async def send_verification_email(user: schemas.UserOut):
#     token = generate_email_token(user.id, user.email)
#     verification_link = f""
#     email = MessageSchema(
#         subject="Email verification",
#         recipients=[user.email],
#         body=f"Please verify your email address by clicking the following link {verification_link}"
#     )
#     fm = FastMail(EmailSettings)
#     await fm.send_message(email)