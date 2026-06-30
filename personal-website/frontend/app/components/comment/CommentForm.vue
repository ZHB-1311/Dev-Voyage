<!-- frontend/app/components/comment/CommentForm.vue -->
<template>
  <div class="comment-form">
    <!-- 已登录：显示输入框 -->
    <div v-if="isLoggedIn" class="form-wrapper">
      <div class="user-avatar">
        {{ user?.username?.charAt(0).toUpperCase() }}
      </div>
      <div class="input-wrapper">
        <textarea
          v-model="content"
          placeholder="写下你的评论..."
          rows="3"
          :disabled="isSubmitting"
        ></textarea>
        <div class="form-actions">
          <span class="char-count" :class="{ warning: content.length > 900 }">
            {{ content.length }}/1000
          </span>
          <button 
            @click="submitComment" 
            :disabled="!content.trim() || isSubmitting"
            class="btn-submit"
          >
            {{ isSubmitting ? '发送中...' : '发表评论' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- 未登录：提示登录 -->
    <div v-else class="login-prompt">
      <p>💡 登录后即可发表评论</p>
      <NuxtLink to="/auth/login" class="btn-login">去登录</NuxtLink>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  articleId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['comment-added'])

const { user, token, isLoggedIn } = useAuth()

const content = ref('')
const isSubmitting = ref(false)

async function submitComment() {
  if (!content.value.trim()) return
  
  isSubmitting.value = true
  
  try {
    await $fetch(`http://localhost:8000/api/articles/${props.articleId}/comments`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token.value}`
      },
      body: {
        content: content.value.trim()
      }
    })
    
    content.value = ''
    emit('comment-added')
  } catch (error) {
    alert('评论失败：' + (error.data?.detail || '未知错误'))
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.comment-form {
  margin-bottom: 2rem;
}

.form-wrapper {
  display: flex;
  gap: 1rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.input-wrapper {
  flex: 1;
}

.input-wrapper textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  resize: vertical;
  font-size: 0.95rem;
  line-height: 1.5;
  transition: border-color 0.2s;
}

.input-wrapper textarea:focus {
  outline: none;
  border-color: #667eea;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
}

.char-count {
  font-size: 0.875rem;
  color: #9ca3af;
}

.char-count.warning {
  color: #f59e0b;
}

.btn-submit {
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  transition: opacity 0.2s;
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.login-prompt {
  text-align: center;
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 0.5rem;
}

.login-prompt p {
  margin-bottom: 1rem;
  color: #6b7280;
}

.btn-login {
  padding: 0.5rem 1.5rem;
  background: #667eea;
  color: white;
  text-decoration: none;
  border-radius: 0.375rem;
}
</style>