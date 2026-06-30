<!-- frontend/app/pages/blog/create.vue -->
<template>
  <div class="create-page">
    <h1 class="page-title">
      {{ isEditMode ? '编辑文章' : '写文章' }}
    </h1>

    <form @submit.prevent="handleSubmit" class="article-form">
      <!-- 标题 -->
      <div class="form-group">
        <label for="title" class="form-label">
          文章标题 <span class="required">*</span>
        </label>
        <input
          id="title"
          v-model="form.title"
          type="text"
          class="form-input"
          placeholder="起一个吸引人的标题..."
          maxlength="200"
        />
        <p class="char-count">{{ form.title.length }}/200</p>
      </div>

      <!-- 摘要 -->
      <div class="form-group">
        <label for="summary" class="form-label">
          文章摘要
        </label>
        <textarea
          id="summary"
          v-model="form.summary"
          class="form-textarea"
          placeholder="简短描述文章内容（不填则自动截取正文）"
          rows="2"
          maxlength="500"
        ></textarea>
        <p class="char-count">{{ form.summary.length }}/500</p>
      </div>

      <!-- 标签 -->
      <div class="form-group">
        <label for="tags" class="form-label">
          标签
        </label>
        <input
          id="tags"
          v-model="form.tags"
          type="text"
          class="form-input"
          placeholder="多个标签用逗号分隔，如：Vue,学习笔记"
        />
      </div>


      <!-- 正文 -->
    <div class="form-group">
    <label class="form-label">
        文章正文 <span class="required">*</span>
    </label>
    <p class="form-hint">支持 Markdown 格式，右侧实时预览</p>
    
    <div class="editor-container">
        <!-- 编辑区 -->
        <div class="editor-pane">
        <textarea
            v-model="form.content"
            class="form-textarea content-editor"
            placeholder="在这里写下你的想法..."
            rows="20"
        ></textarea>

        <p class="word-count">
            当前字数：{{ wordCount }} 字
        </p>
        </div>
        
        <!-- 预览区 -->
        <div class="preview-pane">
        <div class="preview-label">预览</div>
        <div class="preview-content prose" v-html="previewContent"></div>
        </div>
    </div>
    </div>

    <div class="form-group">
         <label class="form-label">
            <input v-model="form.is_draft" type="checkbox" />
              保存为草稿
        </label>
     </div>

      <!-- 提交按钮 -->
      <div class="form-actions">
        <NuxtLink to="/blog" class="btn-cancel">
          取消
        </NuxtLink>
        <button 
          type="submit" 
          class="btn-submit"
          :disabled="isSubmitting || !isFormValid"
        >
          {{ isSubmitting ? '保存中...' : isEditMode ? '保存修改' : '发布文章' }}
        </button>
      </div>

      <!-- 错误提示 -->
      <div v-if="errorMessage" class="error-message">
        ❌ {{ errorMessage }}
      </div>
    </form>
  </div>
</template>

<script setup>
// 表单数据
import MarkdownIt from 'markdown-it'

const md = new MarkdownIt()
const route = useRoute()
const editId = route.query.edit
const isEditMode = computed(() => Boolean(editId))
const { token } = useAuth()

const form = reactive({
  title: '',
  summary: '',
  content: '',
  tags: '',
  is_draft: false
})

const previewContent = computed(() => {
  if (!form.content) return '<p class="placeholder">预览区域...</p>'
  return md.render(form.content)
})

const wordCount = computed(() => {
  return form.content.trim().length
})

if (isEditMode.value) {
  const article = await $fetch(`http://localhost:8000/api/articles/${editId}`)

  form.title = article.title || ''
  form.summary = article.summary || ''
  form.content = article.content || ''
  form.tags = Array.isArray(article.tags) ? article.tags.join(',') : ''
  form.is_draft = article.is_draft || false
}
// 状态
const isSubmitting = ref(false)
const errorMessage = ref('')

// 表单验证
const isFormValid = computed(() => {
  return form.title.trim().length > 0 && form.content.trim().length > 0
})

// 提交表单
async function handleSubmit() {
  // 清除之前的错误
  errorMessage.value = ''
  
  // 验证表单
  if (!form.title.trim()) {
    errorMessage.value = '请输入文章标题'
    return
  }
  if (!form.content.trim()) {
    errorMessage.value = '请输入文章内容'
    return
  }
  
  // 开始提交
  isSubmitting.value = true
  
  try {
    const url = isEditMode.value
      ? `http://localhost:8000/api/articles/${editId}`
      : 'http://localhost:8000/api/articles'

    const method = isEditMode.value ? 'PUT' : 'POST'

    const response = await $fetch(url, {
      method,
      headers: {
    Authorization: `Bearer ${token.value}`
  },
      body: {
        title: form.title.trim(),
        summary: form.summary.trim(),
        content: form.content,
        tags: form.tags.trim(),
        is_draft: form.is_draft
      }
    })
    
    // 发布成功，跳转到文章详情页
    if (response.article?.id) {
      navigateTo(`/blog/${response.article.id}`)
    } else {
      navigateTo('/blog')
    }
  } catch (error) {
    console.error('发布失败:', error)
    errorMessage.value = error.data?.detail || '发布失败，请稍后重试'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.create-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a202c;
  margin-bottom: 2rem;
}

.article-form {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.required {
  color: #e53e3e;
}

.form-hint {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 1rem;
  resize: vertical;
  font-family: inherit;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.content-editor {
  font-family: 'Fira Code', 'Consolas', monospace;
  line-height: 1.6;
}

.char-count {
  text-align: right;
  font-size: 0.75rem;
  color: #9ca3af;
  margin-top: 0.25rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  color: #6b7280;
  text-decoration: none;
  border-radius: 0.5rem;
  transition: background 0.2s;
}

.btn-cancel:hover {
  background: #f3f4f6;
}

.btn-submit {
  padding: 0.75rem 2rem;
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

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  background: #fef2f2;
  color: #dc2626;
  border-radius: 0.5rem;
  text-align: center;
}
.editor-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  min-height: 400px;
}

.editor-pane .content-editor {
  height: 100%;
  min-height: 400px;
}

.preview-pane {
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  background: #f9fafb;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.preview-label {
  padding: 0.5rem 1rem;
  background: #e5e7eb;
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

.preview-content {
  padding: 1rem;
  overflow-y: auto;
  flex: 1;
}

.preview-content .placeholder {
  color: #9ca3af;
  font-style: italic;
}

/* 响应式：小屏幕时上下布局 */
@media (max-width: 768px) {
  .editor-container {
    grid-template-columns: 1fr;
  }
}
.word-count {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #6b7280;
  text-align: right;
}
.draft-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background: #fef3c7;
  color: #92400e;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}
</style>
