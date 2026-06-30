<template>
  <div>
    <!-- Hero 区域 -->
    <HeroSection
      name="你的名字"
      title="全栈开发学习者"
      description="正在学习 Nuxt + FastAPI 全栈开发。热爱编程，热爱开源。希望通过这个博客记录自己的成长历程。"
    />

    <!-- 分割线 -->
    <hr class="border-gray-200 my-8" />

    <!-- 技能展示 -->
    <SkillsSection />

    <!-- 分割线 -->
    <hr class="border-gray-200 my-8" />

    <!-- 项目展示 -->
    <ProjectsSection />

    <!-- 分割线 -->
    <hr class="border-gray-200 my-8" />

    <!-- 最新文章 -->
    <section class="py-12">
      <h2 class="text-2xl font-bold text-gray-800 text-center mb-8">
        📝 最新文章
      </h2>

      <div v-if="articlesPending" class="text-center">
        <p class="text-gray-500">加载中...</p>
      </div>

      <div v-else class="space-y-4">
        <ArticleCard
          v-for="article in latestArticles"
          :key="article.id"
          :article="article"
        />
      </div>

      <div class="text-center mt-8">
        <NuxtLink
          to="/blog"
          class="inline-block px-6 py-2 border-2 border-indigo-600 text-indigo-600 rounded-lg hover:bg-indigo-600 hover:text-white transition"
        >
          查看全部文章 →
        </NuxtLink>
      </div>
    </section>

    <!-- 联系区域 -->
    <section class="py-12 text-center">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">
        📬 联系我
      </h2>
      <p class="text-gray-600 mb-6">
        有任何问题或合作意向，欢迎随时联系我！
      </p>
      <a
        href="mailto:hello@example.com"
        class="inline-block px-8 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition"
      >
        发送邮件
      </a>
    </section>
  </div>
</template>
<script setup>
// ... 其他代码 ...

// 获取最新文章（只取前 3 篇） // [!code ++]
const { data: articlesData, pending: articlesPending } = await useFetch('http://localhost:8000/api/articles') // [!code ++]
const latestArticles = computed(() => articlesData.value?.articles?.slice(0, 3) || []) // [!code ++]
</script>