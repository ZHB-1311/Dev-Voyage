<!-- frontend/app/pages/user/articles.vue -->
<template>
  <div class="my-articles">
    <div class="page-header">
      <h1>📝 我的文章</h1>
      <NuxtLink v-if="canPublish" to="/blog/publish" class="btn-publish">
        ✍️ 写新文章
      </NuxtLink>
    </div>
    
    <!-- 加载中 -->
    <div v-if="pending" class="loading">
      加载中...
    </div>
    
    <!-- 文章列表 -->
    <div v-else-if="articles.length > 0" class="article-list">
      <div 
        v-for="article in articles" 
        :key="article.id" 
        class="article-item"
      >
        <div class="article-info">
          <NuxtLink :to="`/blog/${article.id}`" class="article-title">
            {{ article.title }}
          </NuxtLink>
          <p class="article-meta">
            发布于 {{ article.created_at }}
          </p>
        </div>
        
        <div class="article-actions">
          <NuxtLink :to="`/blog/edit/${article.id}`" class="btn-edit">
            ✏️ 编辑
          </NuxtLink>
          <button @click="confirmDelete(article)" class="btn-delete">
            🗑️ 删除
          </button>
        </div>
      </div>
    </div>
    
    <!-- 空状态 -->
    <div v-else class="empty-state">
      <p class="empty-icon">📭</p>
      <p class="empty-text">你还没有发布过文章</p>
      <NuxtLink v-if="canPublish" to="/blog/publish" class="btn-publish">
        发布第一篇文章
      </NuxtLink>
      <button v-else @click="becomeAuthor" class="btn-publish">
        成为作者，开始创作
      </button>
    </div>
    
    <!-- 删除确认弹窗 -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal-content" @click.stop>
        <h3>确认删除</h3>
        <p>确定要删除文章「{{ articleToDelete?.title }}」吗？</p>
        <p class="warning-text">⚠️ 此操作不可撤销！</p>
        <div class="modal-actions">
          <button @click="showDeleteModal = false" class="btn-cancel">取消</button>
          <button @click="deleteArticle" class="btn-confirm-delete">确认删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: ['auth']
})

const { token, user } = useAuth()
const { canPublish } = usePermission()

// 获取文章列表
const { data, pending, refresh } = await useFetch('http://localhost:8000/api/users/me/articles', {
  headers: {
    Authorization: `Bearer ${token.value}`
  }
})

const articles = computed(() => data.value?.articles || [])

// 删除相关
const showDeleteModal = ref(false)
const articleToDelete = ref(null)

function confirmDelete(article) {
  articleToDelete.value = article
  showDeleteModal.value = true
}

async function deleteArticle() {
  if (!articleToDelete.value) return
  
  try {
    await $fetch(`http://localhost:8000/api/articles/${articleToDelete.value.id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    
    showDeleteModal.value = false
    articleToDelete.value = null
    refresh()  // 刷新列表
  } catch (error) {
    alert('删除失败：' + (error.data?.detail || '未知错误'))
  }
}

// 成为作者
async function becomeAuthor() {
  try {
    await $fetch('http://localhost:8000/api/users/become-author', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    
    if (user.value) {
      user.value.role = 'author'
      localStorage.setItem('user', JSON.stringify(user.value))
    }
    
    alert('🎉 你现在是作者了！')
  } catch (error) {
    alert('操作失败')
  }
}
</script>

<style scoped>
.my-articles {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  margin: 0;
}

.btn-publish {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
  font-weight: 500;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.article-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  transition: box-shadow 0.2s;
}

.article-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.article-title {
  font-weight: 600;
  color: #1a202c;
  text-decoration: none;
  font-size: 1.1rem;
}

.article-title:hover {
  color: #667eea;
}

.article-meta {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.article-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit,
.btn-delete {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  cursor: pointer;
  border: none;
  text-decoration: none;
}

.btn-edit {
  background: #e5e7eb;
  color: #374151;
}

.btn-delete {
  background: #fee2e2;
  color: #dc2626;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-text {
  color: #6b7280;
  margin-bottom: 1.5rem;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  max-width: 400px;
  width: 90%;
}

.modal-content h3 {
  margin-top: 0;
}

.warning-text {
  color: #dc2626;
  font-size: 0.875rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-cancel {
  flex: 1;
  padding: 0.75rem;
  background: #e5e7eb;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
}

.btn-confirm-delete {
  flex: 1;
  padding: 0.75rem;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
}
</style>