<!-- frontend/app/components/comment/CommentSection.vue -->
<template>
  <div class="comment-section">
    <h3 class="section-title">
      💬 评论 
      <span v-if="total > 0" class="comment-count">({{ total }})</span>
    </h3>
    
    <!-- 功能关闭提示 -->
    <div v-if="!featureEnabled" class="feature-disabled">
      <p>😴 评论功能当前未开启</p>
    </div>
    
    <!-- 文章关闭评论提示 -->
    <div v-else-if="!articleAllowComment" class="feature-disabled">
      <p>🔒 作者已关闭该文章的评论</p>
    </div>
    
    <!-- 正常显示评论区 -->
    <template v-else>
      <!-- 评论输入框 -->
      <CommentForm 
        :article-id="articleId"
        @comment-added="handleCommentAdded"
      />
      
      <!-- 评论列表 -->
      <CommentList
        :comments="comments"
        :loading="loading"
        @comment-deleted="handleCommentDeleted"
      />
    </template>
  </div>
</template>

<script setup>
const props = defineProps({
  articleId: {
    type: Number,
    required: true
  }
})

const { commentEnabled } = useFeature()

// 获取评论数据
const { data, pending: loading, refresh } = await useFetch(
  `http://localhost:8000/api/articles/${props.articleId}/comments`
)

// 解析数据
const comments = computed(() => data.value?.comments || [])
const total = computed(() => data.value?.total || 0)
const featureEnabled = computed(() => data.value?.enabled !== false)
const articleAllowComment = computed(() => data.value?.article_allow_comment !== false)

// 评论添加后刷新列表
function handleCommentAdded() {
  refresh()
}

// 评论删除后刷新列表
function handleCommentDeleted() {
  refresh()
}
</script>

<style scoped>
.comment-section {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.section-title {
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
}

.comment-count {
  color: #6b7280;
  font-weight: normal;
}

.feature-disabled {
  text-align: center;
  padding: 2rem;
  background: #f9fafb;
  border-radius: 0.5rem;
  color: #6b7280;
}
</style>