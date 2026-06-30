<!-- frontend/app/pages/user/index.vue -->
<template>
  <div class="user-center">
    <div class="profile-header">
      <div class="avatar-section">
        <div class="avatar">
          {{ user?.username?.charAt(0).toUpperCase() }}
        </div>
        <div class="user-info">
          <h1 class="username">{{ user?.username }}</h1>
          <span class="role-badge" :class="user?.role">
            {{ roleLabel }}
          </span>
        </div>
      </div>
      
      <div class="user-meta">
        <p>📧 {{ user?.email }}</p>
        <p>📅 注册于 {{ user?.created_at }}</p>
      </div>
    </div>
    
    <!-- 提示消息 -->
    <div v-if="needAuthorMessage" class="tip-banner warning">
      ⚠️ 你需要成为作者才能发布文章。
      <button @click="becomeAuthor" class="btn-small">立即成为作者</button>
    </div>
    
    <!-- 功能入口 -->
    <div class="feature-cards">
      <NuxtLink to="/user/articles" class="feature-card">
        <span class="icon">📝</span>
        <span class="title">我的文章</span>
        <span class="desc">查看和管理你发布的文章</span>
      </NuxtLink>
      
      <div 
        v-if="!isAuthor" 
        class="feature-card action"
        @click="becomeAuthor"
      >
        <span class="icon">✨</span>
        <span class="title">成为作者</span>
        <span class="desc">获得发布文章的权限</span>
      </div>
      
      <NuxtLink 
        v-if="canPublish" 
        to="/blog/publish" 
        class="feature-card"
      >
        <span class="icon">🚀</span>
        <span class="title">发布文章</span>
        <span class="desc">分享你的想法和知识</span>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: ['auth']  // 需要登录
})

const route = useRoute()
const { user, token } = useAuth()
const { canPublish, isAuthor } = usePermission()

// 检查是否有提示消息
const needAuthorMessage = computed(() => route.query.message === 'need-author')

// 角色标签
const roleLabel = computed(() => {
  const labels = {
    reader: '📖 读者',
    author: '✍️ 作者',
  }
  return labels[user.value?.role] || '用户'
})

// 成为作者
async function becomeAuthor() {
  try {
    const response = await $fetch('http://localhost:8000/api/users/become-author', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    
    // 更新本地用户信息
    if (user.value) {
      user.value.role = 'author'
      localStorage.setItem('user', JSON.stringify(user.value))
    }
    
    alert('🎉 ' + response.message)
  } catch (error) {
    alert('操作失败：' + (error.data?.detail || '未知错误'))
  }
}
</script>

<style scoped>
.user-center {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.profile-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 1rem;
  padding: 2rem;
  color: white;
  margin-bottom: 2rem;
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.avatar {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
}

.username {
  font-size: 1.75rem;
  margin: 0 0 0.5rem 0;
}

.role-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  background: rgba(255, 255, 255, 0.2);
}

.role-badge.author {
  background: rgba(255, 215, 0, 0.3);
}

.user-meta {
  opacity: 0.9;
  font-size: 0.9rem;
}

.user-meta p {
  margin: 0.25rem 0;
}

.tip-banner {
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.tip-banner.warning {
  background: #fef3cd;
  color: #856404;
}

.btn-small {
  padding: 0.5rem 1rem;
  background: #856404;
  color: white;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
}

.feature-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.feature-card {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 1rem;
  padding: 1.5rem;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  transition: all 0.2s;
}

.feature-card:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.feature-card.action {
  cursor: pointer;
  border-style: dashed;
}

.feature-card .icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.feature-card .title {
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
}

.feature-card .desc {
  font-size: 0.875rem;
  color: #6b7280;
}
</style>