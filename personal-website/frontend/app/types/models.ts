export interface User {
  id: number
  username: string
  email: string
  created_at: string
  avatar: string
  is_verified: boolean
  role: 'reader' | 'author'
}

export interface Article {
  id: number
  title: string
  summary: string
  content: string
  author: string
  created_at: string
  tags: string[]
  category?: string
  view_count: number
  like_count: number
  is_liked?: boolean
}

export interface Comment {
  id: number
  content: string
  created_at: string
  article_id: number
  user: {
    id: number
    username: string
    avatar: string
  }
}

export interface LikeItem {
  user_id: number
  username: string
  avatar: string
}