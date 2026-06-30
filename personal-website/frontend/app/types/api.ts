import type { User, Article, Comment, LikeItem } from './models'

export interface ArticleListResponse {
  articles: Article[]
  total: number
}

export interface PopularResponse {
  articles: Article[]
  total: number
}

export interface LikeToggleResponse {
  liked: boolean
  like_count: number
}

export interface LikeListResponse {
  likes: LikeItem[]
  total: number
}

export interface CommentListResponse {
  comments: Comment[]
  total: number
  enabled: boolean
  article_allow_comment: boolean
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}