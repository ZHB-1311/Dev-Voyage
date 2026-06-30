<template>
  <article class="article-card">
    <!-- 封面图 -->
    <img
      :src="article.cover || `https://picsum.photos/seed/${article.id}/800/400`"
      :alt="article.title"
      class="card-cover"
    />

    <div class="card-body">
      <div class="card-top-row">
        <span class="category-badge">{{ article.category || '未分类' }}</span>
        <span class="view-count">👀 {{ article.view_count || 0 }}</span>
        <span class="like-count">❤️ {{ article.like_count || 0 }}</span>
      </div>

      <!-- 文章标题 -->
      <h2 class="card-title">
        <NuxtLink :to="`/blog/${article.id}`">
          {{ article.title }}
        </NuxtLink>
      </h2>

      <!-- 文章摘要 -->
      <p class="card-summary">
        {{ article.summary }}
      </p>

      <!-- 文章元信息 -->
      <div class="card-meta">
        <div class="meta-left">
          <span class="meta-item">👤 {{ article.author }}</span>
          <span class="meta-item">📅 {{ article.created_at }}</span>
          <span class="meta-item">⏱️ {{ readingTime }}</span>
        </div>

        <div class="tags">
          <span
            v-for="tag in article.tags"
            :key="tag"
            class="tag"
          >
            {{ tag }}
          </span>
        </div>
      </div>
    </div>
  </article>
</template>

<script setup>
const props = defineProps({
  article: {
    type: Object,
    required: true
  }
})

const readingTime = computed(() => {
  const text = props.article.content || `${props.article.title} ${props.article.summary}`
  const textLength = text.length

  const minutes = Math.max(1, Math.ceil(textLength / 120))
  return `${minutes} 分钟阅读`
})
</script>

<style scoped>
.article-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 20px -6px rgb(0 0 0 / 0.15);
}

.card-cover {
  width: 100%;
  height: 220px;
  object-fit: cover;
  display: block;
}

.card-body {
  padding: 1.5rem;
}

.card-top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.9rem;
}

.category-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  background: #ecfeff;
  color: #0f766e;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.view-count {
  font-size: 0.8rem;
  color: #64748b;
}

.card-title {
  font-size: 1.25rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.card-summary {
  color: #4b5563;
  margin-bottom: 1rem;
  line-height: 1.7;
}

.card-meta {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.meta-left {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  padding: 0.25rem 0.5rem;
  background: #eef2ff;
  color: #4338ca;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}
</style>
