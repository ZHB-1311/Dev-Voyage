<template>
  <section class="text-center py-16">
    <!-- 头像 -->
    <div class="mb-6"> 
      <img
        :src="avatar"
        :alt="name"
        class="w-32 h-32 rounded-full mx-auto shadow-lg border-4 border-white"
      /> 
    </div> 

    <!-- 名字和标题 -->
    <h1 class="text-4xl font-bold text-gray-800 mb-2"> 
      {{ name }} 
    </h1>
    <p class="text-xl text-indigo-600 font-medium mb-4"> 
      {{ title }} 
    </p> 

    <!-- 简介 -->
    <p class="text-gray-600 max-w-2xl mx-auto leading-relaxed"> 
      {{ description }} 
    </p> 

    <!-- 社交链接 -->
    <div class="flex justify-center gap-4 mt-8"> 
      <a
        v-for="link in socialLinks"
        :key="link.name"
        :href="link.url"
        target="_blank"
        class="p-3 bg-white rounded-full shadow-md hover:shadow-lg hover:-translate-y-1 transition-all duration-300"
      > 
        <span class="text-2xl">{{ link.icon }}</span> 
      </a> 
    </div> 
  </section> 
</template>

<script setup>
defineProps({ 
  name: { 
    type: String, 
    default: '你的名字' 
  }, 
  title: { 
    type: String, 
    default: '全栈开发者' 
  }, 
  avatar: { 
    type: String, 
    default: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Felix' 
  }, 
  description: { 
    type: String, 
    default: '热爱编程，热爱生活。正在学习全栈开发，希望能用技术改变世界。' 
  }, 
  socialLinks: { 
    type: Array, 
    default: () => [ 
      { name: 'GitHub', icon: '🐙', url: 'https://github.com' }, 
      { name: 'Twitter', icon: '🐦', url: 'https://twitter.com' }, 
      { name: 'Email', icon: '📧', url: 'mailto:hello@example.com' }, 
    ] 
  } 
}) 
</script>