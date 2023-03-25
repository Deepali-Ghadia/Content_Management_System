# #The user requests a password reset by providing their email address.
# The system generates a secure, random token or code and associates it with the user's account.
# The system sends an email to the user's registered email address, containing a link or a code to reset their password. The link or code usually includes the generated token or code.
# #The user clicks the link or enters the code from the email, and is directed to a password reset page on the system.
# The system verifies the token or code, typically by checking it against the associated user account, and allows the user to enter a new password.
# The user enters a new password and submits it.
# The system saves the new password and logs the user in automatically, or redirects the user to a login page.

from fastapi import APIRouter, HTTPException, status, Depends
from database import db
import smtplib
from email.mime.text import MIMEText
import schemas, models
from routers.authentication import create_access_token
from jose import jwt, JWTError
from routers.register import password_context

router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f71ab9f6f0f4caa6cf63b88e8d3e7" # used for encoding the data | Third part of the token
ALGORITHM = "HS256" # first part of the token
ACCESS_TOKEN_EXPIRE_MINUTES = 10


def verify_the_generated_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Email Address")
        # token_data = schemas.ResetPassword(email=email)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Email Address") 

    return email


# API for reset password

@router.post("/reset-password")
def request_reset_password(email: schemas.ResetPassword):
    user = db.query(models.User).filter(models.User.email_id == email.email_id).first()
    if not user:
        return {"message": "User not found"}


    # generate access token
    reset_token = create_access_token(data ={"sub": user.email_id})
    print(reset_token)

    # send email with password reset link
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login('deepali.ghadia.stpl.2023@gmail.com', 'xbzwjqzdxexjznjn')
    message = f'Subject: Password Reset\n\nClick this link to reset your password: http://localhost:8000/reset-password/?token={reset_token}'
    smtp_server.sendmail('your_email', email.email_id, message)
    smtp_server.quit()

    print("Password reset email sent ✅✅")

    return user.email_id



@router.put("/reset-password/{token}")
def reset_password(token: str, update_details: schemas.UpdatePassword, to_validate: str = Depends(request_reset_password)):
    # print(to_validate)
    
    # verify the access token
    email_from_token = verify_the_generated_token(token)
    
    if email_from_token != to_validate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Token")



    updated_hashed_password = password_context.hash(update_details.password)
    
    user = db.query(models.User).filter(models.User.email_id == email_from_token).first()
    user.password = updated_hashed_password
    
    db.commit()
    db.refresh(user)

    return {"message": "Password reset is successful"}