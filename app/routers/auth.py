from fastapi import APIRouter, Depends, HTTPException, Header, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import oauth2
from .. import database, models, schemas, utils, oauth2
from sqlalchemy.orm import Session
router = APIRouter(tags=["Authentication Requests"])


@router.post("/login", response_model=schemas.Token)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username
    ).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify_pwd(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    access_token = oauth2.create_access_token(user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

# @router.post("/verify-email", response_model=schemas.UserOut)
# async def verify_email(verify_email_data: schemas.VerifyEmail, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_user)):
#     try:
#         payload = jwt.decode(verify_email_data.token, settings.secret_key, settings.algorithm)
#         user_id = payload["user_id"]
#         user = db.query(models.User).filter(models.User.id == user_id).first()

#         if not user:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

#         user.is_verified = True
#         db.commit()
#         db.refresh(user)
#         return user
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Verification token expired.")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid verification token.")

@router.post("/login/token/verify/", status_code=status.HTTP_202_ACCEPTED)
async def verify_token(authorization: str = Header(None)):
    token = authorization.split(' ')[1] if authorization else None

    if not token:
        return {"valid": False}

    try:
        oauth2.verify_access_token(token, HTTPException(status_code = status.HTTP_401_UNAUTHORIZED))
        return {"valid": True}
    except HTTPException:
        return {"valid": False}
