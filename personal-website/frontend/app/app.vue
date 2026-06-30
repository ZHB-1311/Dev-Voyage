<template>
  <NuxtLayout>
    <NuxtPage
      :transition="{
        name: 'page',
        mode: 'out-in'
      }"
    />
  </NuxtLayout>
</template>

<script setup>
const { initTheme } = useTheme()
const { loadFeatures } = useFeature()
const { initAuth } = useAuth()

onMounted(() => {
  initTheme()
  loadFeatures()
  initAuth()
})
</script>

<style>
.page-enter-active,
.page-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

html {
  scroll-behavior: smooth;
}
</style>