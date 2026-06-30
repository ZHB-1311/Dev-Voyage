# backend/src/backend/schemas.py
from pydantic import BaseModel, Field
from typing import Optional,Literal


class ArticleCreate(BaseModel):
    """创建文章的请求模型"""
    title: str = Field(..., min_length=1, max_length=200, description="文章标题")
    summary: Optional[str] = Field(default="", max_length=500, description="文章摘要")
    content: str = Field(..., min_length=1, description="文章内容")
    tags: Optional[str] = Field(default="", description="标签，逗号分隔")
    is_draft: bool = Field(default=False, description="是否为草稿")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "我的新文章",
                "summary": "这是文章摘要",
                "content": "# 标题\n\n这是文章正文...",
                "tags": "Python,学习笔记",
                "is_draft": False
            }
        }


class ArticleResponse(BaseModel):
    """文章响应模型"""
    id: int
    title: str
    summary: str
    content: str
    author: str
    created_at: str
    tags: list[str]


class UserCreate(BaseModel):
    """用户注册模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: str = Field(..., description="邮箱")
    password: str = Field(..., min_length=6, description="密码")


class UserLogin(BaseModel):
    """用户登录模型"""
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")
    remember_me: bool = Field(default=False, description="记住我")


class UserResponse(BaseModel):
    """用户信息响应"""
    id: int
    username: str
    email: str
    created_at: str
    avatar: str
    is_verified: bool = Field(default=False, description="邮箱是否已验证")
    role: str  # 新增

class TokenResponse(BaseModel):
    """登录成功响应"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ChangePassword(BaseModel):
    """修改密码请求模型"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, description="新密码")


class EmailVerifyRequest(BaseModel):
    """邮箱验证请求"""
    token: str = Field(..., description="验证令牌")

class RoleUpdateRequest(BaseModel):
    """角色更新请求"""
    role: Literal["reader", "author"]


class CommentCreate(BaseModel):
    """创建评论"""
    content: str = Field(..., min_length=1, max_length=1000, description="评论内容")


class CommentResponse(BaseModel):
    """评论响应"""
    id: int
    content: str
    created_at: str
    article_id: int
    user: dict