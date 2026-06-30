# backend/src/backend/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
import enum


class Article(Base):
    """文章模型（更新版）"""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    summary = Column(Text)
    content = Column(Text)
    author = Column(String(100), default="博主")
    created_at = Column(String(20))
    tags = Column(String(200))
    category = Column(String(100), default="未分类")
    view_count = Column(Integer, default=0)
    is_draft = Column(Integer, default=0)
    
    # 新增：关联用户
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="articles")

    comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")
    allow_comment = Column(Integer, default=1)  # 是否允许评论：1=允许，0=禁止

    like_count = Column(Integer, default=0)
    likes = relationship("Like", back_populates="article", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "content": self.content,
            "author": self.user.username if self.user else self.author,
            "created_at": self.created_at,
            "tags": self.tags.split(",") if self.tags else [],
            "category": self.category,
            "view_count": self.view_count,
            "like_count": self.like_count
        }

class UserRole(str, enum.Enum):
    """用户角色枚举"""
    reader = "reader"   # 读者（默认）
    author = "author"   # 作者
class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(200), nullable=False)
    created_at = Column(String(20))
    avatar = Column(String(500), default="")
    is_verified = Column(Integer, default=0, comment="邮箱是否已验证：0=未验证，1=已验证")
    # 新增：用户角色
    role = Column(String(20), default=UserRole.reader.value)
    # 关联：一个用户可以有多篇文章
    articles = relationship("Article", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "avatar": self.avatar,
            "is_verified": bool(self.is_verified),
            "role": self.role
        }

    def has_permission(self, required_role: str) -> bool:
        """检查用户是否有某个角色的权限"""
        role_levels = {
            "reader": 1,
            "author": 2,
        }
        return role_levels.get(self.role, 0) >= role_levels.get(required_role, 0)


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint("user_id", "article_id", name="uq_user_article_like"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    created_at = Column(String(20))

    user = relationship("User", back_populates="likes")
    article = relationship("Article", back_populates="likes")

class Comment(Base):
    """评论模型"""
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(String(20))
    
    # 外键关联
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 关系
    article = relationship("Article", back_populates="comments")
    user = relationship("User", back_populates="comments")

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at,
            "article_id": self.article_id,
            "user": {
                "id": self.user.id,
                "username": self.user.username,
                "avatar": self.user.avatar
            } if self.user else None
        }

