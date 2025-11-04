from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials
from fastapi import HTTPException, Security
from dotenv import load_dotenv
import os

load_dotenv()

access_security = JwtAccessBearer(secret_key=os.getenv('SECRET_KEY'))

def create_token(data : dict):
    try:
        token = access_security.create_access_token(subject=data)
        print(token)
        return token
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка создания токена {e}')


def get_subject(credentials: JwtAuthorizationCredentials = Security(access_security)):
    return credentials.subject