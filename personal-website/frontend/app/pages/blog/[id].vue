<!-- frontend/app/pages/blog/[id].vue -->
<template>
  <div class="article-page">
    <!-- 加载状态 -->
    <div v-if="pending" class="loading-state">
      <div class="loading-spinner"></div>
      <p>正在加载文章...</p>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="error-state">
      <p class="error-icon">😵</p>
      <p class="error-message">{{ error.message || '加载失败' }}</p>
      <button @click="refresh" class="retry-btn">
        🔄 重试
      </button>
    </div>

    <!-- 文章不存在 -->
    <div v-else-if="!article" class="not-found">
      <p class="not-found-icon">📭</p>
      <p>文章不存在或已被删除</p>
      <NuxtLink to="/blog" class="back-link">
        ← 返回文章列表
      </NuxtLink>
    </div>

    <!-- 文章详情 -->
    <article v-else class="article-detail">
      <!-- 返回按钮 -->
      <div class="article-actions">
        <NuxtLink to="/blog" class="back-btn">
          ← 返回文章列表
        </NuxtLink>

        <div class="action-buttons">
          <NuxtLink :to="`/blog/create?edit=${article.id}`" class="edit-btn">
            编辑
          </NuxtLink>

          <button @click="handleDelete" class="delete-btn">
            删除
          </button>
        </div>
      </div>

      <!-- 文章标题 -->
      <h1 class="article-title">{{ article.title }}</h1>

      <!-- 文章元信息 -->
      <div class="article-meta">
        <span class="meta-item">
          <span class="meta-icon">👤</span>
          {{ article.author }}
        </span>
        <span class="meta-item">
          <span class="meta-icon">📅</span>
          {{ article.created_at }}
        </span>
        <span class="meta-item">
          <span class="meta-icon">👀</span>
          {{ article.view_count || 0 }} 次阅读
        </span>
      </div>

      <!-- 文章元信息 -->

      <!-- 点赞 -->
      <div class="article-likes">
        <LikeButton :article-id="articleId" :initial-liked="article.is_liked" :initial-count="article.like_count || 0" />
      </div>

      <div class="article-category">
        分类：{{ article.category || '未分类' }}
      </div>

      <!-- 标签 -->
      <div class="article-tags">
        <span
          v-for="tag in article.tags"
          :key="tag"
          class="tag"
        >
          {{ tag }}
        </span>
      </div>

      <!-- 文章内容 -->
      <div class="article-content prose" v-html="renderedContent"></div>
    </article>

        <!-- 点赞列表 -->
    <LikeList :article-id="articleId" />
        <!-- 评论区 -->
    <CommentSection :article-id="articleId" />
  </div>
</template>

<script setup>
import MarkdownIt from 'markdown-it'
import markdownItHighlightjs from 'markdown-it-highlightjs'
import 'highlight.js/styles/github.css'
import LikeButton from '~/components/like/LikeButton.vue'
import LikeList from '~/components/like/LikeList.vue'


const route = useRoute()
const articleId = Number(route.params.id)


// 获取文章详情
const { data: article, pending, error, refresh } = await useFetch(
  `http://localhost:8000/api/articles/${articleId}`
)

// 创建 Markdown 渲染器
const md = new MarkdownIt({
  html: true,        // 允许 HTML 标签
  linkify: true,     // 自动转换链接
  typographer: true  // 智能引号等排版优化
}).use(markdownItHighlightjs)

// 渲染 Markdown 内容
const renderedContent = computed(() => {
  if (!article.value?.content) return ''
  return md.render(article.value.content)
})

async function handleDelete() {
  const confirmed = confirm('确定要删除这篇文章吗？删除后不能恢复。')

  if (!confirmed) {
    return
  }

  try {
    await $fetch(`http://localhost:8000/api/articles/${articleId}`, {
      method: 'DELETE'
    })

    navigateTo('/blog')
  } catch (error) {
    console.error('删除失败:', error)
    alert('删除失败，请稍后重试')
  }
}
</script>

<style scoped>
.article-page {
  max-width: 100%;
  margin: 0 auto;
  padding: var(--space-4);
}

@media (min-width: 768px) {
  .article-page {
    max-width: 800px;
    padding: var(--space-8);
  }
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  color: var(--color-text-muted);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  text-align: center;
  padding: 3rem;
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.error-message {
  color: var(--color-error);
  margin-bottom: 1.5rem;
}

.retry-btn {
  padding: 0.75rem 1.5rem;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.2s;
}

.retry-btn:hover {
  background: var(--color-primary-dark);
}

.not-found {
  text-align: center;
  padding: 3rem;
  color: var(--color-text-muted);
}

.not-found-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.back-link {
  display: inline-block;
  margin-top: 1.5rem;
  color: var(--color-primary);
  text-decoration: none;
}

.back-link:hover {
  text-decoration: underline;
}

.article-detail {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.article-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.back-btn:hover {
  color: var(--color-primary-dark);
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
}

.edit-btn,
.delete-btn {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-md);
  text-decoration: none;
  border: none;
  cursor: pointer;
  font-size: 0.95rem;
}

.edit-btn {
  background: var(--color-primary);
  color: white;
}

.delete-btn {
  background: var(--color-error);
  color: white;
}

.article-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--color-text-primary);
  margin-bottom: 1rem;
  line-height: 1.2;
}

@media (min-width: 768px) {
  .article-title {
    font-size: 2.5rem;
  }
}

.article-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  color: var(--color-text-muted);
  margin-bottom: 1rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.meta-icon {
  font-size: 1rem;
}

.article-likes {
  display: flex;
  align-items: center;
  margin-bottom: 1.25rem;
}

.article-category {
  display: inline-flex;
  align-items: center;
  padding: 0.35rem 0.85rem;
  background: #ecfeff;
  color: #0f766e;
  border-radius: var(--radius-full);
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 1.25rem;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.tag {
  padding: 0.25rem 0.75rem;
  background: var(--color-bg-tertiary);
  color: var(--color-text-secondary);
  border-radius: var(--radius-full);
  font-size: 0.875rem;
}

.article-content {
  color: var(--color-text-primary);
  line-height: 1.8;
  font-size: 1.1rem;
}

.article-content :deep(h1) {
  font-size: 2rem;
  font-weight: 700;
  margin-top: 2.5rem;
  margin-bottom: 1rem;
  color: var(--color-text-primary);
}

.article-content :deep(h2) {
  font-size: 1.5rem;
  font-weight: 600;
  margin-top: 2rem;
  margin-bottom: 0.75rem;
  color: var(--color-text-primary);
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 0.5rem;
}

.article-content :deep(h3) {
  font-size: 1.25rem;
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--color-text-primary);
}

.article-content :deep(p) {
  margin-bottom: 1.25rem;
}

.article-content :deep(ul),
.article-content :deep(ol) {
  margin-bottom: 1.25rem;
  padding-left: 1.5rem;
}

.article-content :deep(li) {
  margin-bottom: 0.5rem;
}

.article-content :deep(code) {
  background: var(--color-bg-tertiary);
  padding: 0.125rem 0.375rem;
  border-radius: var(--radius-sm);
  font-size: 0.9em;
  font-family: 'Fira Code', 'Consolas', monospace;
}

.article-content :deep(pre) {
  background: #1e293b;
  color: #e2e8f0;
  padding: var(--space-4);
  border-radius: var(--radius-md);
  overflow-x: auto;
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
}

@media (min-width: 768px) {
  .article-content :deep(pre) {
    font-size: 1rem;
  }
}

.article-content :deep(pre code) {
  background: transparent;
  padding: 0;
  font-size: 0.9rem;
  color: inherit;
}

.article-content :deep(blockquote) {
  border-left: 4px solid var(--color-primary);
  padding-left: 1rem;
  margin: 1.5rem 0;
  color: var(--color-text-secondary);
  font-style: italic;
}

.article-content :deep(a) {
  color: var(--color-primary);
  text-decoration: none;
}

.article-content :deep(a:hover) {
  text-decoration: underline;
}

.article-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: var(--radius-md);
  margin: 1.5rem 0;
}

.article-content :deep(hr) {
  border: none;
  border-top: 1px solid var(--color-border);
  margin: 2rem 0;
}
</style>
