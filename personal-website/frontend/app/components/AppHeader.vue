<template>
  <header class="header">
    <div class="header-content">
      <NuxtLink to="/" class="logo">🚀 我的博客</NuxtLink>

      <nav class="nav desktop-nav">
        <NuxtLink to="/" class="nav-link">首页</NuxtLink>
        <NuxtLink to="/about" class="nav-link">关于</NuxtLink>
        <NuxtLink to="/blog" class="nav-link">博客</NuxtLink>
        <template v-if="isLoggedIn">
          <span class="nav-user">👤 {{ user?.username }}</span>
          <NuxtLink to="/settings" class="nav-link">设置</NuxtLink>
          <button @click="handleLogout" class="nav-link logout-btn">退出</button>
        </template>
        <template v-else>
          <NuxtLink to="/auth/login" class="nav-link">登录</NuxtLink>
          <NuxtLink to="/auth/register" class="nav-link nav-register">注册</NuxtLink>
        </template>
      </nav>

      <button class="menu-btn" @click="isMenuOpen = !isMenuOpen">
        {{ isMenuOpen ? '✕' : '☰' }}
      </button>
    </div>

    <nav v-if="isMenuOpen" class="mobile-menu">
      <NuxtLink to="/" class="mobile-link" @click="isMenuOpen = false">首页</NuxtLink>
      <NuxtLink to="/about" class="mobile-link" @click="isMenuOpen = false">关于</NuxtLink>
      <NuxtLink to="/blog" class="mobile-link" @click="isMenuOpen = false">博客</NuxtLink>
      <template v-if="isLoggedIn">
        <span class="mobile-link nav-user">👤 {{ user?.username }}</span>
        <NuxtLink to="/settings" class="mobile-link" @click="isMenuOpen = false">设置</NuxtLink>
        <button @click="handleLogout(); isMenuOpen = false" class="mobile-link logout-btn">退出</button>
      </template>
      <template v-else>
        <NuxtLink to="/auth/login" class="mobile-link" @click="isMenuOpen = false">登录</NuxtLink>
        <NuxtLink to="/auth/register" class="mobile-link" @click="isMenuOpen = false">注册</NuxtLink>
      </template>
    </nav>
  </header>
</template>

<script setup>
const isMenuOpen = ref(false)
const { user, isLoggedIn, logout, initAuth } = useAuth()

onMounted(() => {
  initAuth()
})

function handleLogout() {
  logout()
  navigateTo('/')
}
</script>

<style scoped>
.nav-user {
  display: inline-flex;
  align-items: center;
  line-height: 1.5; /* 确保行高与父级一致 */
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.nav {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: background 0.2s;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
}

.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.2);
}

.menu-btn {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 1.8rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
}

.mobile-menu {
  display: none;
  background: rgba(255, 255, 255, 0.08);
}


.mobile-link {
  display: block;
  color: white;
  text-decoration: none;
  padding: 1rem 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.15);
}

.mobile-link:hover {
  background: rgba(255, 255, 255, 0.1);
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 1rem;
  }

  .desktop-nav {
    display: none;
  }

  .menu-btn {
    display: block;
  }

  .mobile-menu {
    display: block;
  }
}
</style>