<!-- frontend/app/pages/blog/edit/[id].vue -->
<template>
  <div class="edit-page">
    <h1>✏️ 编辑文章</h1>
    
    <div v-if="pending" class="loading">加载中...</div>
    
    <form v-else @submit.prevent="handleSubmit" class="edit-form">
      <div class="form-group">
        <label for="title">文章标题</label>
        <input
          id="title"
          v-model="form.title"
          type="text"
          placeholder="给你的文章起个标题"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="content">文章内容（支持 Markdown）</label>
        <textarea
          id="content"
          v-model="form.content"
          placeholder="开始写作..."
          rows="15"
          required
        ></textarea>
      </div>
      
      <div class="form-group">
        <label for="tags">标签（用逗号分隔）</label>
        <input
          id="tags"
          v-model="form.tags"
          type="text"
          placeholder="Vue,前端,教程"
        />
      </div>
      
      <div class="form-actions">
        <NuxtLink to="/user/articles" class="btn-cancel">取消</NuxtLink>
        <button type="submit" class="btn-submit" :disabled="isSubmitting">
          {{ isSubmitting ? '保存中...' : '保存修改' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: ['author']
})

const route = useRoute()
const { token } = useAuth()

const articleId = route.params.id

// 获取文章详情
const { data, pending } = await useFetch(`http://localhost:8000/api/articles/${articleId}`)

// 表单数据
const form = reactive({
  title: '',
  content: '',
  tags: ''
})

// 填充表单
watch(data, (newData) => {
  if (newData) {
    form.title = newData.title
    form.content = newData.content
    form.tags = newData.tags?.join(',') || ''
  }
}, { immediate: true })

const isSubmitting = ref(false)

async function handleSubmit() {
  isSubmitting.value = true
  
  try {
    await $fetch(`http://localhost:8000/api/articles/${articleId}`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${token.value}`
      },
      body: {
        title: form.title,
        content: form.content,
        tags: form.tags
      }
    })
    
    navigateTo(`/blog/${articleId}`)
  } catch (error) {
    alert('保存失败：' + (error.data?.detail || '未知错误'))
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.edit-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
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

.form-group input,
.form-group textarea {
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
}

.form-group textarea {
  resize: vertical;
  font-family: 'Monaco', 'Menlo', monospace;
  line-height: 1.6;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  background: #e5e7eb;
  color: #374151;
  text-decoration: none;
  border-radius: 0.5rem;
}

.btn-submit {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>