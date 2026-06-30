<!-- frontend/app/pages/auth/login.vue -->
<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1 class="auth-title">🔐 登录</h1>
      <p class="auth-subtitle">欢迎回来！</p>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label for="username">用户名 / 邮箱</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            placeholder="请输入用户名或邮箱"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            required
          />
        </div>

        <div v-if="errorMessage" class="error-message">
          ❌ {{ errorMessage }}
        </div>

        <div class="form-group checkbox-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="form.rememberMe" />
            <span>记住我</span>
          </label>
        </div>

        <button type="submit" class="btn-submit" :disabled="isLoading">
          {{ isLoading ? '登录中...' : '登录' }}
        </button>
      </form>

      <p class="auth-link">
        还没有账号？
        <NuxtLink to="/auth/register">立即注册</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
const { login } = useAuth()

const form = reactive({
  username: '',
  password: '',
  rememberMe: false
})

const isLoading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  errorMessage.value = ''
  isLoading.value = true

  try {
    await login(form.username, form.password, form.rememberMe)
    navigateTo('/blog')
  } catch (error) {
    errorMessage.value = error.data?.detail || '登录失败，请检查用户名和密码'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.auth-card {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: 1rem;
  padding: 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.auth-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a202c;
  margin-bottom: 0.5rem;
  text-align: center;
}

.auth-subtitle {
  color: #6b7280;
  text-align: center;
  margin-bottom: 2rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #374151;
}

.form-group input {
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.error-message {
  padding: 0.75rem;
  background: #fef2f2;
  color: #dc2626;
  border-radius: 0.5rem;
  text-align: center;
  font-size: 0.875rem;
}

.btn-submit {
  padding: 0.875rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #6b7280;
}

.auth-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.auth-link a:hover {
  text-decoration: underline;
}

.checkbox-group {
  flex-direction: row;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  color: #6b7280;
  font-size: 0.9rem;
}

.checkbox-label input[type="checkbox"] {
  width: 1rem;
  height: 1rem;
  cursor: pointer;
}
</style>