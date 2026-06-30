<!-- frontend/app/components/NavBar.vue -->
<template>
  <nav class="navbar">
    <div class="nav-container">
      <!-- Logo -->
      <NuxtLink to="/" class="nav-logo">
        📝 我的博客
      </NuxtLink>
      
      <!-- 桌面端导航 -->
      <div class="nav-links hide-mobile">
        <NuxtLink to="/blog" class="nav-link">文章</NuxtLink>
        <NuxtLink v-if="isLoggedIn" to="/user" class="nav-link">个人中心</NuxtLink>
        <NuxtLink v-if="canPublish" to="/blog/publish" class="nav-link">写文章</NuxtLink>
        
        <template v-if="isLoggedIn">
          <span class="nav-user">{{ user?.username }}</span>
          <button @click="logout" class="nav-btn-text">退出</button>
        </template>
        <template v-else>
          <NuxtLink to="/auth/login" class="nav-btn">登录</NuxtLink>
        </template>
        
        <ThemeToggle />
      </div>
      
      <!-- 移动端菜单按钮 -->
      <button class="menu-btn hide-desktop" @click="isMenuOpen = !isMenuOpen">
        {{ isMenuOpen ? '✕' : '☰' }}
      </button>
    </div>
    
    <!-- 移动端下拉菜单 -->
    <div v-if="isMenuOpen" class="mobile-menu hide-desktop">
      <NuxtLink to="/blog" class="mobile-link" @click="isMenuOpen = false">
        📄 文章列表
      </NuxtLink>
      <NuxtLink v-if="isLoggedIn" to="/user" class="mobile-link" @click="isMenuOpen = false">
        👤 个人中心
      </NuxtLink>
      <NuxtLink v-if="canPublish" to="/blog/publish" class="mobile-link" @click="isMenuOpen = false">
        ✍️ 写文章
      </NuxtLink>
      
      <div class="mobile-divider"></div>
      
      <template v-if="isLoggedIn">
        <span class="mobile-user">👋 {{ user?.username }}</span>
        <button @click="handleLogout" class="mobile-link">🚪 退出登录</button>
      </template>
      <NuxtLink v-else to="/auth/login" class="mobile-link" @click="isMenuOpen = false">
        🔐 登录
      </NuxtLink>
      
      <div class="mobile-divider"></div>
      
      <div class="mobile-theme">
        <span>主题</span>
        <ThemeToggle />
      </div>
    </div>
  </nav>
</template>

<script setup>
const { user, isLoggedIn, logout } = useAuth()
const { canPublish } = usePermission()

const isMenuOpen = ref(false)

function handleLogout() {
  logout()
  isMenuOpen.value = false
  navigateTo('/')
}

// 路由变化时关闭菜单
const route = useRoute()
watch(() => route.path, () => {
  isMenuOpen.value = false
})
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--color-bg-primary);
  border-bottom: 1px solid var(--color-border);
}

.nav-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4);
  max-width: 1280px;
  margin: 0 auto;
}

.nav-logo {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text-primary);
  text-decoration: none;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: var(--space-6);
}

.nav-link {
  color: var(--color-text-secondary);
  text-decoration: none;
  font-weight: 500;
  transition: color var(--transition-fast);
}

.nav-link:hover {
  color: var(--color-primary);
}

.nav-user {
  color: var(--color-text-muted);
}

.nav-btn {
  padding: var(--space-2) var(--space-4);
  background: var(--color-primary);
  color: white;
  border-radius: var(--radius-md);
  text-decoration: none;
  font-weight: 500;
}

.nav-btn-text {
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
}

.menu-btn {
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--space-2);
}

/* 移动端菜单 */
.mobile-menu {
  padding: var(--space-4);
  border-top: 1px solid var(--color-border);
  background: var(--color-bg-secondary);
}

.mobile-link {
  display: block;
  padding: var(--space-3) 0;
  color: var(--color-text-primary);
  text-decoration: none;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  font-size: 1rem;
  cursor: pointer;
}

.mobile-user {
  display: block;
  padding: var(--space-3) 0;
  color: var(--color-text-muted);
}

.mobile-divider {
  height: 1px;
  background: var(--color-border);
  margin: var(--space-2) 0;
}

.mobile-theme {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) 0;
}

/* 响应式显示/隐藏 */
.hide-mobile { display: none; }
.hide-desktop { display: flex; }

@media (min-width: 768px) {
  .hide-mobile { display: flex; }
  .hide-desktop { display: none; }
}
</style>