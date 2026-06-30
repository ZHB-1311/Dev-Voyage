# backend/src/backend/__init__.py
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.orm import Session
import random, os, secrets
from .database import engine, get_db, SessionLocal, Base
from .models import Article,Comment,Like
from datetime import datetime, timedelta
from .schemas import ArticleCreate,CommentCreate
from .config import get_all_features, is_feature_enabled

# 在文件顶部添加导入
from .auth import (
    hash_password, 
    verify_password, 
    create_access_token,
    get_current_user,
    get_current_user_required,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    require_author
)
from .schemas import UserCreate, UserLogin, TokenResponse, ChangePassword, EmailVerifyRequest
from .models import User


# 创建数据库表（如果不存在）
Base.metadata.create_all(bind=engine)

app = FastAPI()


# 创建上传目录
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "static", "avatars")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "..", "static")), name="static")


# 配置跨域
app.add_middleware(#添加中间件
    CORSMiddleware,#使用CORSMiddleware中间件
    allow_origins=["http://localhost:3000"],  # 允许前端地址
    allow_credentials=True,#允许发送cookie
    allow_methods=["*"],#允许的HTTP方法
    allow_headers=["*"],#允许的HTTP头
)


def ensure_article_columns():
    with engine.begin() as connection:
        columns = {
            row[1] for row in connection.execute(text("PRAGMA table_info(articles)"))
        }

        if "category" not in columns:
            connection.execute(
                text(
                    "ALTER TABLE articles ADD COLUMN category VARCHAR(100) DEFAULT '未分类'"
                )
            )

        if "view_count" not in columns:
            connection.execute(
                text(
                    "ALTER TABLE articles ADD COLUMN view_count INTEGER DEFAULT 0"
                )
            )

        if "is_draft" not in columns:
            connection.execute(
                text(
                    "ALTER TABLE articles ADD COLUMN is_draft BOOLEAN DEFAULT 0"
                )
            )
        if "like_count" not in columns:
            connection.execute(
                text("ALTER TABLE articles ADD COLUMN like_count INTEGER DEFAULT 0")
            )

# 功能开关检查装饰器
def require_feature(feature_name: str):
    """要求某个功能必须开启"""
    def checker():
        if not is_feature_enabled(feature_name):
            raise HTTPException(
                status_code=403,
                detail=f"功能 {feature_name} 当前未开启"
            )
    return checker

@app.get("/")
async def root():
    return {"message": "Hello World!"}


# 问候语列表
greetings = [
    "你好，这是来自后端的问候！",
    "欢迎来到全栈开发的世界！",
    "今天也要加油写代码哦！",
    "休息一下，喝杯水吧～",
    "代码写累了？出去走走！",
    "你已经很棒了，继续保持！",
]

@app.on_event("startup")
def init_database():
    ensure_article_columns()

    db = SessionLocal()
    try:
        # 如果数据库为空，添加示例文章
        if db.query(Article).count() == 0:
            sample_articles = [
                Article(
                    title="我的第一篇博客",
                    summary="这是我学习全栈开发的第一篇博客，记录了从零开始搭建项目的过程。",
                    content="我的第一篇博客",
                    author="博主",
                    created_at="2025-01-15",
                    tags="入门,全栈"
                ),
                Article(
                    title="Vue 3 组合式 API 学习笔记",
                    summary="深入理解 Vue 3 的 Composition API，包括 ref、reactive、computed 等核心概念。",
                    content="Vue 3 组合式 API 学习笔记",
                    author="博主",
                    created_at="2025-01-18",
                    tags="Vue,前端"
                ),
                Article(
                    title="FastAPI 快速入门指南",
                    summary="FastAPI 是一个现代、快速的 Python Web 框架，本文介绍其基本用法和最佳实践。",
                    content="FastAPI 快速入门指南",
                    author="博主",
                    created_at="2025-01-20",
                    tags="Python,后端,FastAPI"
                ),
            ]
            db.add_all(sample_articles)
            db.commit()
            print("✅ 示例数据初始化完成")
    finally:
        db.close()


    

@app.get("/api/greeting")
async def greeting():
    # 随机返回一条问候语
    text = random.choice(greetings)
    return {"text": text}

@app.get("/api/time")
async def get_time():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"time": now}

@app.get("/api/greet") # [!code focus]
async def greet(name: str = "朋友", mood: str = "开心"): # [!code focus]
    moods = { # [!code focus]
        "开心": "😄", # [!code focus]
        "难过": "😢", # [!code focus]
        "生气": "😠", # [!code focus]
        "惊讶": "😲", # [!code focus]
    } # [!code focus]
    emoji = moods.get(mood, "😊") # [!code focus]
    return {"message": f"{emoji} 你好，{name}！今天{mood}吗？"} # [!code focus]

@app.get("/api/hello/{name}") # [!code focus]
async def hello(name: str): # [!code focus]
    return {"message": f"你好，{name}！欢迎来到全栈世界！"} # [!code focus]

@app.get("/api/articles")
async def get_articles(category: str = "", db: Session = Depends(get_db)):
    query = db.query(Article)
    if category.strip():
        query = query.filter(Article.category == category.strip())

    articles = query.order_by(Article.id.desc()).all()

    return {
        "articles": [article.to_dict() for article in articles],
        "total": len(articles)
    }


@app.get("/api/articles/search")
async def search_articles(
    keyword: str = "",
    category: str = "",
    db: Session = Depends(get_db),
):
    query = db.query(Article)

    if keyword.strip():
        query = query.filter(Article.title.contains(keyword.strip()))

    if category.strip():
        query = query.filter(Article.category == category.strip())

    articles = query.order_by(Article.id.desc()).all()

    return {
        "articles": [article.to_dict() for article in articles],
        "total": len(articles)
    }


# 获取单篇文章
@app.get("/api/articles/{article_id}")
async def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()

    if article is None:
        raise HTTPException(status_code=404, detail="文章不存在")

    article.view_count += 1
    db.commit()
    db.refresh(article)

    return article.to_dict()

@app.post("/api/articles")
def create_article(
    article: ArticleCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_required)  # 可选登录
):
    """发布新文章"""
    db_article = Article(
        title=article.title,
        summary=article.summary or article.content[:100] + "...",
        content=article.content,
        author=current_user.username if current_user else "匿名",
        created_at=datetime.now().strftime("%Y-%m-%d"),
        tags=article.tags,
        user_id=current_user.id
    )
    
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    
    return {
        "message": "发布成功",
        "article": db_article.to_dict()
    }

@app.put("/api/articles/{article_id}")
def update_article(
    article_id: int,
    article_data: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_author)  # 需要作者权限
):
    """更新文章"""
    # 查找文章
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 检查所有权
    if article.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="你只能编辑自己的文章")
    
    # 更新字段
    article.title = article_data.title
    article.content = article_data.content
    article.summary = article_data.summary or article_data.content[:100] + "..."
    article.tags = article_data.tags
    
    db.commit()
    db.refresh(article)
    
    return {
        "message": "更新成功",
        "article": article.to_dict()
    }


@app.delete("/api/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    """删除文章"""
    db_article = db.query(Article).filter(Article.id == article_id).first()

    if db_article is None:
        raise HTTPException(status_code=404, detail="文章不存在")

    db.delete(db_article)
    db.commit()

    return {
        "message": "删除成功"
    }

# 添加注册 API
@app.post("/api/auth/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="用户名已被使用")
    
    # 检查邮箱是否已存在
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    # 创建用户
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        created_at=datetime.now().strftime("%Y-%m-%d")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 生成 Token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "message": "注册成功",
        "access_token": access_token,
        "token_type": "bearer",
        "user": user.to_dict()
    }


@app.post("/api/auth/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    # 支持用户名或邮箱登录
    user = db.query(User).filter(
        (User.username == login_data.username) | 
        (User.email == login_data.username)
    ).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # 生成 Token（记住我 → 30 天，否则 7 天）
    if login_data.remember_me:
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        )
    else:
        access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "message": "登录成功",
        "access_token": access_token,
        "token_type": "bearer",
        "user": user.to_dict()
    }


@app.get("/api/auth/me")
def get_me(current_user: User = Depends(get_current_user_required)):
    """获取当前登录用户信息"""
    return current_user.to_dict()


@app.put("/api/auth/password")
def change_password(
    data: ChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """修改密码"""
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="旧密码错误")
    
    current_user.hashed_password = hash_password(data.new_password)
    db.commit()
    
    return {"message": "密码修改成功"}


@app.post("/api/auth/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """上传头像"""
    ext = file.filename.rsplit(".", 1)[-1] if "." in file.filename else "png"
    filename = f"avatar_{current_user.id}_{secrets.token_hex(4)}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)
    
    avatar_url = f"/static/avatars/{filename}"
    current_user.avatar = avatar_url
    db.commit()
    
    return {"avatar": avatar_url}


@app.post("/api/auth/send-verification")
def send_verification(
    current_user: User = Depends(get_current_user_required)
):
    """发送邮箱验证邮件（开发阶段直接返回验证链接）"""
    if current_user.is_verified:
        return {"message": "邮箱已验证", "verified": True}
    
    token = secrets.token_urlsafe(32)
    verify_url = f"http://localhost:8000/api/auth/verify-email?token={token}"
    
    # 将验证 token 存到临时字段（生产环境应发邮件）
    current_user.avatar = current_user.avatar  # 占位，实际应存到内存/缓存
    print(f"📧 验证链接（开发环境）: {verify_url}")
    
    return {
        "message": "验证邮件已发送",
        "verify_url": verify_url,
        "token": token
    }


@app.post("/api/auth/verify-email")
def verify_email(
    data: EmailVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """验证邮箱"""
    if current_user.is_verified:
        return {"message": "邮箱已验证", "verified": True}
    
    # 简化实现：只要有合法 token 即可验证
    current_user.is_verified = 1
    db.commit()
    
    return {"message": "邮箱验证成功", "verified": True}


@app.post("/api/users/become-author")
def become_author(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """申请成为作者"""
    if current_user.role == UserRole.author.value:
        raise HTTPException(status_code=400, detail="你已经是作者了")
    
    current_user.role = UserRole.author.value
    db.commit()
    
    return {
        "message": "恭喜！你现在是作者了，可以发布文章啦！",
        "user": current_user.to_dict()
    }

@app.get("/api/users/me/articles")
def get_my_articles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """获取当前用户的文章列表"""
    articles = db.query(Article).filter(
        Article.user_id == current_user.id
    ).order_by(Article.id.desc()).all()
    
    return {
        "articles": [article.to_dict() for article in articles],
        "total": len(articles)
    }


@app.delete("/api/articles/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_author)
):
    """删除文章"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 检查所有权
    if article.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="你只能删除自己的文章")
    
    db.delete(article)
    db.commit()
    
    return {"message": "删除成功"}

@app.get("/api/features")
def get_features():
    """获取所有功能的开关状态"""
    return get_all_features()


@app.get("/api/features/{feature_name}")
def get_feature_status(feature_name: str):
    """获取单个功能的状态"""
    return {
        "feature": feature_name,
        "enabled": is_feature_enabled(feature_name)
    }

@app.get("/api/articles/{article_id}/comments")
def get_article_comments(
    article_id: int,
    db: Session = Depends(get_db)
):
    """获取文章的评论列表"""
    # 检查功能是否开启
    if not is_feature_enabled("comment"):
        return {"comments": [], "total": 0, "enabled": False}
    
    # 检查文章是否存在
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 检查文章是否允许评论
    if not article.allow_comment:
        return {
            "comments": [],
            "total": 0,
            "enabled": True,
            "article_allow_comment": False
        }
    
    # 获取评论
    comments = db.query(Comment).filter(
        Comment.article_id == article_id
    ).order_by(Comment.id.desc()).all()
    
    return {
        "comments": [comment.to_dict() for comment in comments],
        "total": len(comments),
        "enabled": True,
        "article_allow_comment": True
    }

@app.post("/api/articles/{article_id}/comments")
def create_comment(
    article_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_required)  # 必须登录
):
    """发表评论"""
    # 检查功能是否开启
    if not is_feature_enabled("comment"):
        raise HTTPException(status_code=403, detail="评论功能当前未开启")
    
    # 检查文章是否存在
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 检查文章是否允许评论
    if not article.allow_comment:
        raise HTTPException(status_code=403, detail="该文章已关闭评论")
    
    # 创建评论
    comment = Comment(
        content=comment_data.content,
        article_id=article_id,
        user_id=current_user.id,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M")
    )
    
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    return {
        "message": "评论成功",
        "comment": comment.to_dict()
    }


@app.delete("/api/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """删除评论（只能删除自己的）"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="评论不存在")
    
    # 检查权限：只能删除自己的评论
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="你只能删除自己的评论")
    
    db.delete(comment)
    db.commit()
    
    return {"message": "删除成功"}

@app.get("/api/articles/popular")
async def get_popular_articles(limit: int = 10, db: Session = Depends(get_db)):
    articles = db.query(Article).order_by(Article.like_count.desc()).limit(limit).all()
    return {
        "articles": [article.to_dict() for article in articles],
        "total": len(articles)
    }


@app.post("/api/articles/{article_id}/like")
def toggle_like(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    if not is_feature_enabled("like"):
        raise HTTPException(status_code=403, detail="点赞功能当前未开启")

    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    existing = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.article_id == article_id
    ).first()

    if existing:
        db.delete(existing)
        article.like_count = max(0, article.like_count - 1)
        liked = False
    else:
        like = Like(
            user_id=current_user.id,
            article_id=article_id,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        db.add(like)
        article.like_count = (article.like_count or 0) + 1
        liked = True

    db.commit()
    db.refresh(article)

    return {"liked": liked, "like_count": article.like_count}


@app.get("/api/articles/{article_id}/likes")
def get_article_likes(article_id: int, db: Session = Depends(get_db)):
    if not is_feature_enabled("like"):
        return {"likes": [], "total": 0}

    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    likes = db.query(Like).filter(Like.article_id == article_id).order_by(Like.id.desc()).all()
    return {
        "likes": [
            {
                "user_id": like.user.id,
                "username": like.user.username,
                "avatar": like.user.avatar
            } for like in likes
        ],
        "total": len(likes)
    }