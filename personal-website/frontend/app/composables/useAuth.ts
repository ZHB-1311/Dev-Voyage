// frontend/app/composables/useAuth.ts
interface User {
  id: number
  username: string
  email: string
  created_at: string
  avatar: string
  is_verified?: boolean
}

interface AuthState {
  user: User | null
  token: string | null
}

export const useAuth = () => {
  const user = useState<User | null>('auth_user', () => null)
  const token = useState<string | null>('auth_token', () => null)

  const getHeaders = () => {
    const t = token.value
    if (!t) return {}
    return { Authorization: `Bearer ${t}` }
  }

  // 初始化：从 localStorage 恢复登录状态
  const initAuth = () => {
    if (process.client) {
      const savedToken = localStorage.getItem('token')
      const savedUser = localStorage.getItem('user')
      if (savedToken && savedUser) {
        token.value = savedToken
        user.value = JSON.parse(savedUser)
      }
    }
  }

  // 登录
  const login = async (username: string, password: string, rememberMe: boolean = false) => {
    const response = await $fetch<{
      access_token: string
      user: User
    }>('http://localhost:8000/api/auth/login', {
      method: 'POST',
      body: { username, password, remember_me: rememberMe }
    })

    token.value = response.access_token
    user.value = response.user

    if (process.client) {
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))
    }

    return response
  }

  // 注册
  const register = async (username: string, email: string, password: string) => {
    const response = await $fetch<{
      access_token: string
      user: User
    }>('http://localhost:8000/api/auth/register', {
      method: 'POST',
      body: { username, email, password }
    })

    token.value = response.access_token
    user.value = response.user

    if (process.client) {
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))
    }

    return response
  }

  // 退出登录
  const logout = () => {
    token.value = null
    user.value = null

    if (process.client) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }

  // 修改密码
  const changePassword = async (oldPassword: string, newPassword: string) => {
    return $fetch('http://localhost:8000/api/auth/password', {
      method: 'PUT',
      headers: getHeaders(),
      body: { old_password: oldPassword, new_password: newPassword }
    })
  }

  // 上传头像
  const uploadAvatar = async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)

    return $fetch<{ avatar: string }>('http://localhost:8000/api/auth/avatar', {
      method: 'POST',
      headers: getHeaders(),
      body: formData
    })
  }

  // 发送邮箱验证
  const sendVerification = async () => {
    return $fetch('http://localhost:8000/api/auth/send-verification', {
      method: 'POST',
      headers: getHeaders()
    })
  }

  // 验证邮箱
  const verifyEmail = async (token: string) => {
    return $fetch('http://localhost:8000/api/auth/verify-email', {
      method: 'POST',
      headers: getHeaders(),
      body: { token }
    })
  }

  // 是否已登录
  const isLoggedIn = computed(() => !!token.value && !!user.value)

  return {
    user,
    token,
    isLoggedIn,
    initAuth,
    login,
    register,
    logout,
    changePassword,
    uploadAvatar,
    sendVerification,
    verifyEmail
  }
}