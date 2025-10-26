from fastapi import FastAPI, Depends, Response, Header, Security, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models import Base, Post, PostCreate, CommandHandler, CommentHandler, Comment, RegistrationHandler, nameHandler, User, AuthorisationHandler
from database import engine, SessionLocal
from sqlalchemy import text, select
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials

app = FastAPI()

access_security = JwtAccessBearer(secret_key='very_secret_key')

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f'Ошибка при создании таблиц {e}')

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


def create_token(data : dict):
    token = access_security.create_access_token(subject=data)
    return token


def get_subject(credentials: JwtAuthorizationCredentials = Security(access_security)):
    return credentials.subject


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/getName')
def get_name(credentials: JwtAuthorizationCredentials = Security(access_security)):
    data = credentials.subject
    return Response(data['login'])


@app.post('/auth')
def authorisation(data : AuthorisationHandler, db = Depends(get_db)):
    data = dict(data)
    data = db.query(User).filter(User.login == data['login'], User.password == data['password']).first()
    db.commit()
    if data:
        data = {'login':data.login, 'password':data.password}
        token = access_security.create_access_token(subject=data)
        return token
    else:
        return HTTPException(status_code=404, detail='Пользователь не найден')


@app.post('/reg')
def registration(data: RegistrationHandler, db = Depends(get_db)):
    data = dict(data)
    check = db.query(User).filter(User.login == data['login']).first()
    print(check)
    if check == None:
        db.add(User(age = data['age'], login = data['login'], password = data['password']))
        db.commit()
        token = create_token(data=dict(data))
        return {'token':token}


@app.get('/items')
async def get_items(db = Depends(get_db)):
    try:
        items = []
        user = 1
        data = db.query(Post).all()
        for item in data:
            items.append(item.to_dict())

        return JSONResponse(content={'data': items, 'user' : user})
    except Exception as e:
        print(f'ошибка вывода постов {e}')


@app.post('/postCreate')
async def catch_post(post: PostCreate,
                      db = Depends(get_db),
                        credentials: JwtAuthorizationCredentials = Security(access_security)):
    try:
        db.add(Post(content = post.content, author = credentials['login'],
                    likes = 0, dislikes = 0))
        db.commit()
    except:
        print('ошибка создания поста')


@app.post('/postDelete')
async def delete_data(command: CommandHandler, db = Depends(get_db)):
    try:
        db.execute(text("DELETE FROM Posts"))
        db.commit()
    except:
        print('ошибка удаления базы данных')


@app.get('/addDislike/{id}')
async def addDislike(id : int, db = Depends(get_db)):
    try:
        post = db.query(Post).filter(Post.id == id).first()
        
        if post is None:
            post.dislikes = 1

        post.dislikes = post.dislikes + 1
        db.commit()
    except:
        print('ошибка дизлайка')


@app.get('/addLike/{id}')
async def addLike(id : int, db = Depends(get_db)):
    try:
        post = db.query(Post).filter(Post.id == id).first()
        
        if post is None:
            post.likes = 1

        post.likes = post.likes + 1
        db.commit()
    except:
        print('ошибка лайка')


@app.get('/authors')
def get_authors(db = Depends(get_db)):
    try:
        data = db.execute(text('SELECT author FROM Posts')).fetchall()
        authors = list(row[0] for row in data)
        return {'data': authors}

    except:
        print('ошибка вывода авторов')


@app.get('/comments/{post_id}')
def get_comments(post_id:int, db = Depends(get_db)):
    data = db.query(Comment).filter(Comment.post_id == post_id).all()
    return {'data':data}


@app.post('/comments/{post_id}')
def add_comment(post_id:int, data: CommentHandler,  db = Depends(get_db)):
    db.add(Comment(post_id = post_id, content = data.comment))
    db.commit()