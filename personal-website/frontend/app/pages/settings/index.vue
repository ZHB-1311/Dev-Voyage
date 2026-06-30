<template>
  <div class="settings-page">
    <div class="settings-card">
      <h1 class="settings-title">⚙️ 账号设置</h1>

      <!-- 头像上传 -->
      <section class="section">
        <h2>头像</h2>
        <div class="avatar-section">
          <img :src="user?.avatar ? `http://localhost:8000${user.avatar}` : '/default-avatar.png'" class="avatar-preview" />
          <div class="avatar-actions">
            <input type="file" ref="fileInput" accept="image/*" @change="handleFileSelect" hidden />
            <button class="btn" @click="fileInput?.click()" :disabled="avatarLoading">
              {{ avatarLoading ? '上传中...' : '选择图片' }}
            </button>
            <p v-if="avatarMessage" :class="avatarMessageType">{{ avatarMessage }}</p>
          </div>
        </div>
      </section>

      <!-- 邮箱验证 -->
      <section class="section">
        <h2>邮箱 <span v-if="user?.is_verified" class="badge verified">已验证</span><span v-else class="badge unverified">未验证</span></h2>
        <p class="email-text">{{ user?.email }}</p>
        <button v-if="!user?.is_verified" class="btn" @click="handleSendVerification" :disabled="verifyLoading">
          {{ verifyLoading ? '发送中...' : '发送验证邮件' }}
        </button>
        <p v-if="verifyMessage" :class="verifyMessageType">{{ verifyMessage }}</p>
      </section>

      <!-- 修改密码 -->
      <section class="section">
        <h2>修改密码</h2>
        <form @submit.prevent="handleChangePassword" class="password-form">
          <div class="form-group">
            <label>旧密码</label>
            <input v-model="passwordForm.oldPassword" type="password" placeholder="输入旧密码" required />
          </div>
          <div class="form-group">
            <label>新密码</label>
            <input v-model="passwordForm.newPassword" type="password" placeholder="至少 6 个字符" minlength="6" required />
          </div>
          <div class="form-group">
            <label>确认新密码</label>
            <input v-model="passwordForm.confirmPassword" type="password" placeholder="再次输入新密码" required />
          </div>
          <p v-if="passwordMessage" :class="passwordMessageType">{{ passwordMessage }}</p>
          <button type="submit" class="btn btn-primary" :disabled="passwordLoading">
            {{ passwordLoading ? '修改中...' : '修改密码' }}
          </button>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
const { user, uploadAvatar, sendVerification, changePassword } = useAuth()

const fileInput = ref(null)
const avatarLoading = ref(false)
const avatarMessage = ref('')
const avatarMessageType = ref('')

const verifyLoading = ref(false)
const verifyMessage = ref('')
const verifyMessageType = ref('')

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const passwordLoading = ref(false)
const passwordMessage = ref('')
const passwordMessageType = ref('')

async function handleFileSelect(e) {
  const file = e.target.files?.[0]
  if (!file) return

  avatarLoading.value = true
  avatarMessage.value = ''
  try {
    const res = await uploadAvatar(file)
    user.value.avatar = res.avatar
    if (process.client) {
      localStorage.setItem('user', JSON.stringify(user.value))
    }
    avatarMessage.value = '头像上传成功'
    avatarMessageType.value = 'success'
  } catch (err) {
    avatarMessage.value = err.data?.detail || '上传失败'
    avatarMessageType.value = 'error'
  } finally {
    avatarLoading.value = false
  }
}

async function handleSendVerification() {
  verifyLoading.value = true
  verifyMessage.value = ''
  try {
    const res = await sendVerification()
    verifyMessage.value = '验证邮件已发送，请检查邮箱'
    verifyMessageType.value = 'success'
    console.log('验证链接:', res.verify_url)
  } catch (err) {
    verifyMessage.value = err.data?.detail || '发送失败'
    verifyMessageType.value = 'error'
  } finally {
    verifyLoading.value = false
  }
}

async function handleChangePassword() {
  passwordMessage.value = ''

  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    passwordMessage.value = '两次密码不一致'
    passwordMessageType.value = 'error'
    return
  }

  passwordLoading.value = true
  try {
    await changePassword(passwordForm.oldPassword, passwordForm.newPassword)
    passwordMessage.value = '密码修改成功'
    passwordMessageType.value = 'success'
    passwordForm.oldPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
  } catch (err) {
    passwordMessage.value = err.data?.detail || '修改失败'
    passwordMessageType.value = 'error'
  } finally {
    passwordLoading.value = false
  }
}
</script>

<style scoped>
.settings-page {
  max-width: 600px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.settings-card {
  background: white;
  border-radius: 1rem;
  padding: 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.settings-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a202c;
  margin-bottom: 2rem;
}

.section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.section h2 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1rem;
}

.badge {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  vertical-align: middle;
}

.badge.verified {
  background: #d1fae5;
  color: #065f46;
}

.badge.unverified {
  background: #fef3c7;
  color: #92400e;
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.avatar-preview {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #e5e7eb;
}

.avatar-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.email-text {
  color: #6b7280;
  margin-bottom: 0.75rem;
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  font-weight: 500;
  color: #374151;
  font-size: 0.9rem;
}

.form-group input {
  padding: 0.7rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.btn {
  padding: 0.7rem 1.5rem;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
  display: inline-block;
  width: fit-content;
}

.btn:hover:not(:disabled) {
  background: #e5e7eb;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.success {
  color: #065f46;
  background: #d1fae5;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.85rem;
}

.error {
  color: #dc2626;
  background: #fef2f2;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.85rem;
}
</style>
