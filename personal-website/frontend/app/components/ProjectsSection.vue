<template>
  <section class="py-12"> 
    <h2 class="text-2xl font-bold text-gray-800 text-center mb-8">
      🚀 项目展示 
    </h2> 

    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6"> 
      <div
        v-for="project in projects"
        :key="project.name"
        class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300"
      > 
        <!-- 项目图片 -->
        <div class="h-48 bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center"> 
          <span class="text-6xl">{{ project.icon }}</span> 
        </div> 

        <!-- 项目信息 -->
        <div class="p-6"> 
          <h3 class="text-lg font-bold text-gray-800 mb-2"> 
            {{ project.name }} 
          </h3> 
          <p class="text-gray-600 text-sm mb-4"> 
            {{ project.description }} 
          </p> 

          <!-- 技术标签 -->
          <div class="flex flex-wrap gap-2 mb-4"> 
            <span
              v-for="tech in project.techs"
              :key="tech"
              class="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded"
            > 
              {{ tech }} 
            </span> 
          </div> 

          <!-- 链接 -->
          <div class="flex gap-4"> 
            <a
              v-if="project.github"
              :href="project.github"
              target="_blank"
              class="text-gray-600 hover:text-gray-800 text-sm"
            > 
              📦 源码 
            </a> 
            <a
              v-if="project.demo"
              :href="project.demo"
              target="_blank"
              class="text-indigo-600 hover:text-indigo-800 text-sm font-medium"
            > 
              🔗 演示 
            </a> 
          </div> 
        </div> 
      </div> 
    </div> 
  </section> 
</template>

<script setup>
defineProps({ 
  projects: { 
    type: Array, 
    default: () => [ 
      { 
        name: '个人博客', 
        icon: '📝', 
        description: '使用 Nuxt + FastAPI 构建的全栈博客系统，支持 Markdown 写作。', 
        techs: ['Nuxt', 'FastAPI', 'SQLite'], 
        github: 'https://github.com', 
        demo: 'https://example.com' 
      }, 
      { 
        name: 'Todo 应用', 
        icon: '✅', 
        description: '一个简洁的待办事项应用，支持拖拽排序和数据持久化。', 
        techs: ['Vue 3', 'Pinia', 'LocalStorage'], 
        github: 'https://github.com', 
        demo: null 
      }, 
      { 
        name: '天气查询', 
        icon: '🌤️', 
        description: '调用第三方 API 的天气查询应用，支持城市搜索和未来预报。', 
        techs: ['Vue 3', 'Axios', 'OpenWeather API'], 
        github: 'https://github.com', 
        demo: 'https://example.com' 
      }, 
    ] 
  } 
}) 
</script>