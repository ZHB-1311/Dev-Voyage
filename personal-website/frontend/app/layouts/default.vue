<template>
  <div class="layout">
    <NavBar />
    <main class="main">
      <slot />
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import AppFooter from '~/components/AppFooter.vue'
import NavBar from '~/components/NavBar.vue'

const { initAuth } = useAuth()

onMounted(() => {
  initAuth()
})
</script>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main {
  flex: 1;
  max-width: 1280px;
  margin: 0 auto;
  padding: var(--space-8);
  width: 100%;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .main {
    padding: var(--space-4);
  }
}
</style>