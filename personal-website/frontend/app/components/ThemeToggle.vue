<template>
  <button 
    @click="toggleTheme" 
    class="theme-toggle"
    :title="isDark ? '切换到亮色模式' : '切换到暗色模式'"
  >
    <span class="icon">{{ isDark ? '🌙' : '☀️' }}</span>
  </button>
</template>

<script setup>
const { isDark, toggleTheme } = useTheme()
</script>

<style scoped>
.theme-toggle {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  border: 2px solid var(--color-border);
  background: var(--color-bg-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-normal);
}

.theme-toggle:hover {
  border-color: var(--color-primary);
  transform: rotate(15deg);
}

.icon {
  font-size: 1.25rem;
}
</style>