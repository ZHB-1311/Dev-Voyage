<template>
  <div>
    <div class="page-header">
      <h1 class="text-3xl font-bold text-gray-800">
        📝 博客文章
      </h1>
      <NuxtLink to="/blog/create" class="write-btn">
        ✍️ 写文章
      </NuxtLink>
    </div>
    <p class="text-gray-500 mb-8">
      共 {{ filteredArticles.length }} 篇文章
    </p>

    <div v-if="!pending && !error" class="search-bar">
      <input
        v-model="searchKeyword"
        type="text"
        placeholder="搜索文章标题..."
        class="search-input"
      />
    </div>

    <div v-if="!pending && !error" class="filter-bar">
      <label for="category-select" class="filter-label">按分类筛选：</label>
      <select id="category-select" v-model="selectedCategory" class="filter-select">
        <option v-for="category in allCategories" :key="category" :value="category">
          {{ category }}
        </option>
      </select>
      <label for="tag-select" class="filter-label">按标签筛选：</label>
      <select id="tag-select" v-model="selectedTag" class="filter-select">
        <option v-for="tag in allTags" :key="tag" :value="tag">
          {{ tag }}
        </option>
      </select>
    </div>

    <div v-if="!pending && !error" class="popular-section">
      <h2 class="popular-title">🔥 热门文章</h2>
      <NuxtLink
        v-for="(article, index) in popularArticles"
        :key="article.id"
        :to="`/blog/${article.id}`"
        class="popular-item"
      >
        <span class="popular-rank">{{ index + 1 }}</span>
        <span class="popular-name">{{ article.title }}</span>
        <span class="popular-count">❤️ {{ article.like_count }}</span>
      </NuxtLink>
    </div>

    <div v-if="pending" class="article-grid">
      <SkeletonCard v-for="i in 6" :key="i" />
    </div>

    <div v-else-if="error" class="text-center py-12">
      <p class="text-red-500">❌ 加载失败：{{ error.message }}</p>
      <button
        @click="refresh"
        class="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
      >
        重试
      </button>
    </div>

    <div v-else class="article-grid">
      <ArticleCard
        v-for="article in filteredArticles"
        :key="article.id"
        :article="article"
      />
    </div>

    <div v-if="!pending && !error && filteredArticles.length === 0" class="text-center py-12">
      <p class="text-gray-500">📭 当前分类下暂无文章</p>
    </div>
  </div>
</template>

<script setup>
import SkeletonCard from '~/components/SkeletonCard.vue'

const searchKeyword = ref('')
const selectedCategory = ref('全部')
const selectedTag = ref('全部')

const requestUrl = computed(() => {
  if (searchKeyword.value.trim()) {
    return 'http://localhost:8000/api/articles/search'
  }
  return 'http://localhost:8000/api/articles'
})

const requestQuery = computed(() => {
  const query = {}
  if (searchKeyword.value.trim()) {
    query.keyword = searchKeyword.value.trim()
  }
  if (selectedCategory.value !== '全部') {
    query.category = selectedCategory.value
  }
  return query
})

const { data, pending, error, refresh } = await useFetch(requestUrl, {
  query: requestQuery,
  watch: [searchKeyword, selectedCategory],
})

const { data: popularData } = await useFetch('http://localhost:8000/api/articles/popular?limit=5')
const popularArticles = computed(() => popularData.value?.articles || [])

const allCategories = computed(() => {
  const articles = data.value?.articles || []
  const categorySet = new Set()
  for (const article of articles) {
    if (article.category) {
      categorySet.add(article.category)
    }
  }
  return ['全部', ...Array.from(categorySet)]
})

const allTags = computed(() => {
  const articles = data.value?.articles || []
  const tagSet = new Set()
  for (const article of articles) {
    for (const tag of article.tags) {
      tagSet.add(tag)
    }
  }
  return ['全部', ...Array.from(tagSet)]
})

const filteredArticles = computed(() => {
  let articles = data.value?.articles || []
  if (selectedTag.value !== '全部') {
    articles = articles.filter(article => article.tags.includes(selectedTag.value))
  }
  return articles
})
</script>

<style scoped>
.article-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-6);
}

@media (min-width: 768px) {
  .article-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .article-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.search-bar {
  margin-bottom: 1rem;
}

.search-input {
  width: 100%;
  max-width: 320px;
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  outline: none;
  font-size: 0.95rem;
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
}

.search-input:focus {
  border-color: var(--color-primary);
}

.filter-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 2rem;
}

.filter-label {
  font-weight: 600;
  color: var(--color-text-secondary);
}

.filter-select {
  padding: 0.6rem 0.9rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
  font-size: 0.95rem;
  outline: none;
}

.filter-select:focus {
  border-color: var(--color-primary);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.write-btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
}

.write-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.popular-section {
  background: #fff7ed;
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  margin-bottom: 1.5rem;
}

.popular-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #c2410c;
  margin-bottom: 0.75rem;
}

.popular-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0.75rem;
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: background 0.2s;
}

.popular-item:hover {
  background: rgba(255, 255, 255, 0.6);
}

.popular-rank {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fdba74;
  color: white;
  font-weight: 700;
  font-size: 0.8rem;
  border-radius: 50%;
  flex-shrink: 0;
}

.popular-name {
  flex: 1;
  color: var(--color-text-primary);
  font-size: 0.9rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.popular-count {
  font-size: 0.8rem;
  color: #dc2626;
  flex-shrink: 0;
}
</style>