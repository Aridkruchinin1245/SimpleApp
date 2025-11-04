from fastapi_jwt import JwtAuthorizationCredentials
from fastapi import Depends, Security, HTTPException, Response, APIRouter
from backend.models import User, AuthorisationHandler, RegistrationHandler
from backend.security.jwt_handler import access_security, get_subject, create_token
from backend.database import get_db

router = APIRouter()

@router.post('/getName')
def get_name(credentials: JwtAuthorizationCredentials = Security(access_security)):
    try:
        data = credentials.subject
        return Response(data['login'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка получения credentials.subject {e}')


@router.post('/auth')
def authorisation(data : AuthorisationHandler, db = Depends(get_db)):
    data = dict(data)
    data = db.query(User).filter(User.login == data['login'], User.password == data['password']).first()
    db.commit()
    
    if data:
        data = {'login':data.login, 'password':data.password}
        token = access_security.create_access_token(subject=data)
        return token
    else:
        raise HTTPException(status_code=404, detail='Пользователь не найден')


@router.post('/reg')
def registration(data: RegistrationHandler, db = Depends(get_db)):
    data = dict(data)
    check = db.query(User).filter(User.login == data['login']).first()
    
    if check == None:
        db.add(User(age = data['age'], login = data['login'], password = data['password']))
        db.commit()
        token = create_token(data=dict(data))
        
        return {'token' : token}
    
    else: 
        return {'error' : check}