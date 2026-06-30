<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-links">
        <a href="https://github.com" target="_blank" class="footer-link">GitHub</a>
        <span class="divider">•</span>
        <a href="mailto:hello@example.com" class="footer-link">联系我</a>
      </div>
      <p class="copyright">
        © {{ currentYear }} 我的博客 | 用 ❤️ 和 Nuxt + FastAPI 构建
      </p>
    </div>
  </footer>
</template>

<script setup>
const currentYear = new Date().getFullYear()
</script>

<style scoped>
.footer {
  background: var(--color-bg-tertiary);
  color: var(--color-text-secondary);
  padding: 2rem;
  margin-top: auto;
}

.footer-content {
  max-width: 1280px;
  margin: 0 auto;
  text-align: center;
}

.footer-links {
  margin-bottom: 1rem;
}

.footer-link {
  color: var(--color-primary);
  text-decoration: none;
  transition: color 0.2s;
}

.footer-link:hover {
  opacity: 0.8;
}

.divider {
  margin: 0 1rem;
  color: var(--color-text-muted);
}

.copyright {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}
</style>