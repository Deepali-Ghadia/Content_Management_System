from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import db
import schemas, models
from routers.register import password_context
from datetime import datetime, timedelta
from jose import jwt, JWTError
router = APIRouter()

# We can take any random string as a secret key
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f71ab9f6f0f4caa6cf63b88e8d3e7" # used for encoding the data | Third part of the token
ALGORITHM = "HS256" # first part of the token
ACCESS_TOKEN_EXPIRE_MINUTES = 10

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "login") # tokenUrl parameter to specify the URL where the client can obtain an access token.

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def check_password(hashed_password, plain_password):
    return password_context.verify(plain_password, hashed_password)
   
   

def verify_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to validate credentials")
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to validate credentials") 

    user = db.query(models.User).filter(models.User.username == username).first()
    user_id = user.id
    return user_id
    

def get_current_user(token: str = Depends(oauth2_scheme)):
    print(verify_token(token))
    # returns user id
    return verify_token(token)
  
    

    

@router.post('/login')
def login(login: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.username == login.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username does not exist")
    
    
    if not check_password(user.password, login.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password")
    
    
    # If the user exists, then generate access token
    # Here the key of the dicionary should be sub and since we are using username for authentication purpose therefore we have passed the username to sub
    # in the data variable you can pass other details as well if required --> data={"sub": user.username, "name": user.name, ...}
    # Since I am authenticating based on username and I don't need other info along with it ===> passed only username to the function that generates access token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# The Bearer token type indicates that the token being sent is a bearer token, meaning that it grants the bearer (i.e. the client) access to a resource. The access token is usually a string of characters that the server can use to verify the client's identity and authorize access to the requested resource.


# First part i.e before the first dot -> contains algorithm related info (HEADER)
# second part contains payload i.e. actual data