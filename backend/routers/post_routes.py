from backend.database import get_db
from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.responses import JSONResponse
from fastapi_jwt import JwtAuthorizationCredentials
from backend.models import Post, Comment
from backend.schemas import PostCreate, CommandHandler, CommentHandler
from sqlalchemy import text
from backend.security.jwt_handler import access_security

router = APIRouter()

@router.get('/items')
async def get_items(db = Depends(get_db)):
    try:
        items = []
        user = 1
        data = db.query(Post).all()
        
        for item in data:
            items.append(item.to_dict())

        return JSONResponse(content={'data': items, 'user' : user})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка вывода постов {e}')


@router.post('/postCreate')
async def catch_post(post: PostCreate,
            db = Depends(get_db),
            credentials: JwtAuthorizationCredentials = Security(access_security)):
    
    try:
        db.add(Post(content = post.content, author = credentials['login'],
                    likes = 0, dislikes = 0))
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка создания поста {e}')


@router.post('/postDelete')
async def delete_data(command: CommandHandler, db = Depends(get_db)):
    try:
        db.execute(text("DELETE FROM Posts"))
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка удаления БД {e}')


@router.get('/addDislike/{id}')
async def addDislike(id : int,
                      db = Depends(get_db),
                      credentials: JwtAuthorizationCredentials = Security(access_security)):
    try:
        post = db.query(Post).filter(Post.id == id).first()
        
        if post is None:
            post.dislikes = 1

        post.dislikes = post.dislikes + 1
        db.commit()
    except:
        print('ошибка дизлайка')


@router.get('/addLike/{id}')
async def addLike(id : int,
                  db = Depends(get_db),
                  credentials: JwtAuthorizationCredentials = Security(access_security)):
    try:
        post = db.query(Post).filter(Post.id == id).first()
        
        if post is None:
            post.likes = 1

        post.likes = post.likes + 1
        db.commit()
    except:
        print('ошибка лайка')


@router.get('/authors')
def get_authors(db = Depends(get_db)):
    try:
        data = db.execute(text('SELECT author FROM Posts')).fetchall()
        authors = list(row[0] for row in data)
        return {'data': authors}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка вывода авторов {e}')


@router.get('/comments/{post_id}')
def get_comments(post_id:int, db = Depends(get_db)):
    try:
        data = db.query(Comment).filter(Comment.post_id == post_id).all()
        return {'data':data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка вывода комментариев {e}')


@router.post('/comments/{post_id}')
def add_comment(post_id:int, data: CommentHandler,  db = Depends(get_db),
                 credentials: JwtAuthorizationCredentials = Security(access_security)):
    try:
        db.add(Comment(post_id = post_id, content = data.comment, author = credentials.subject['login']))
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка создания комментариев {e}')
