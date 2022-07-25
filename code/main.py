from fastapi import Depends, FastAPI, HTTPException, status, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import pyrebase
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class UserIN(BaseModel):
    email : str
    password : str

origins = [
    "https://8080-nataly2102-31firebaseyf-qeufg3x96vw.ws-us54.gitpod.io/",
    "https://8000-nataly2102-31firebaseyf-qeufg3x96vw.ws-us54.gitpod.io/",
    "*",  
            
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/',
summary="Api-Rest")
async def get():
    return "API-REST 2.0"

firebaseConfig = {
    'apiKey': "AIzaSyC6UDpFIBmgveN0BQq1tK6WZH60hnOOn0E",
    'authDomain': "fir-api-70f5c.firebaseapp.com",
    'databaseURL': "https://fir-api-70f5c-default-rtdb.firebaseio.com",
    'projectId': "fir-api-70f5c",
    'storageBucket': "fir-api-70f5c.appspot.com",
    'messagingSenderId': "141856431030",
    'appId': "1:141856431030:web:2e796328394b9afd07bf17"
}

firebase = pyrebase.initialize_app(firebaseConfig)
securityBasic = HTTPBasic()
securityBearer = HTTPBearer()

@app.post("/user/token",
         status_code =status.HTTP_202_ACCEPTED,
         summary     ="Get a token a user",
         description ="Get a token for a user",
         tags=["auth"])

def post_token(credentials: HTTPBasicCredentials = Depends(securityBasic)):
    try:

        email = credentials.username
        password = credentials.password
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(email, password)
        
        response = {
            "token": user["idToken"]
        }

        return response
    except Exception as error:
        print(f"Error : {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.get("/users/",
         status_code=status.HTTP_202_ACCEPTED,
         summary     ="Get a  user",
         description ="Get a user",
         tags=["auth"])

async def get_user(credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId']

        db = firebase.database()
        user_data = db.child("users").child(uid).get().val()

        response = {
            'user_data': user_data
        }
        return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.post(  "/users/",  
    status_code=status.HTTP_202_ACCEPTED, 
    summary="agregar usuario",
    description="agregar usuario", 
    tags=["auth"]
)

async def create_user(usuario: UserIN ):
    try:
        auth = firebase.auth()
        db=firebase.database()
        user = auth.create_user_with_email_and_password(usuario.email, usuario.password)
        uid = user["localId"]
        db.child("user").child(uid).set({"email": usuario.email, "level": 1 })
        
        response = {"Usuario Agregado"}
        return response
    except Exception as error:
        print(f"Error: {error}")