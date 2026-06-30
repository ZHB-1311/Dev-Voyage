<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1 class="auth-title">🎉 注册</h1>
      <p class="auth-subtitle">加入我们，开始你的博客之旅</p>

      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            placeholder="3-50 个字符"
            minlength="3"
            maxlength="50"
            required
          />
        </div>

        <div class="form-group">
          <label for="email">邮箱</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="your@email.com"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="至少 6 个字符"
            minlength="6"
            required
          />
        </div>

        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            placeholder="再次输入密码"
            required
          />
        </div>

        <div v-if="errorMessage" class="error-message">
          ❌ {{ errorMessage }}
        </div>

        <button type="submit" class="btn-submit" :disabled="isLoading">
          {{ isLoading ? '注册中...' : '注册' }}
        </button>
      </form>

      <p class="auth-link">
        已有账号？
        <NuxtLink to="/auth/login">立即登录</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
const { register } = useAuth()

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const isLoading = ref(false)
const errorMessage = ref('')

async function handleRegister() {
  errorMessage.value = ''

  // 验证两次密码是否一致
  if (form.password !== form.confirmPassword) {
    errorMessage.value = '两次输入的密码不一致'
    return
  }

  isLoading.value = true

  try {
    await register(form.username, form.email, form.password)
    navigateTo('/blog')
  } catch (error) {
    errorMessage.value = error.data?.detail || '注册失败，请稍后重试'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* 样式与登录页面相同 */
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
</style>