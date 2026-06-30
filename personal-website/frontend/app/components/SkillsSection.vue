<template>
  <section class="py-12"> 
    <h2 class="text-2xl font-bold text-gray-800 text-center mb-8"> 
      🛠️ 技能栈 
    </h2> 

    <div class="flex flex-wrap justify-center gap-3"> 
      <span
        v-for="skill in skills"
        :key="skill.name"
        class="px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 hover:scale-105"
        :class="skillClass(skill.category)"
      > 
        {{ skill.icon }} {{ skill.name }} 
      </span> 
    </div> 
  </section> 
</template>

<script setup>
defineProps({
  skills: { 
    type: Array, 
    default: () => [ 
      { name: 'Vue.js', icon: '💚', category: 'frontend' }, 
      { name: 'Nuxt', icon: '💎', category: 'frontend' }, 
      { name: 'TypeScript', icon: '📘', category: 'frontend' }, 
      { name: 'Tailwind CSS', icon: '🎨', category: 'frontend' }, 
      { name: 'Python', icon: '🐍', category: 'backend' }, 
      { name: 'FastAPI', icon: '⚡', category: 'backend' }, 
      { name: 'PostgreSQL', icon: '🐘', category: 'backend' }, 
      { name: 'Docker', icon: '🐳', category: 'devops' }, 
      { name: 'Git', icon: '📦', category: 'devops' }, 
    ] 
  } 
}) 

const skillClass = (category) => { 
  const classes = { 
    frontend: 'bg-green-100 text-green-700 hover:bg-green-200', 
    backend: 'bg-blue-100 text-blue-700 hover:bg-blue-200', 
    devops: 'bg-purple-100 text-purple-700 hover:bg-purple-200', 
  } 
  return classes[category] || 'bg-gray-100 text-gray-700' 
} 
</script>