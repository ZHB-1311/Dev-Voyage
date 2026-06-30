<!-- frontend/app/components/comment/CommentList.vue -->
<template>
  <div class="comment-list">
    <!-- 加载中 -->
    <div v-if="loading" class="loading">
      加载评论中...
    </div>
    
    <!-- 评论列表 -->
    <div v-else-if="comments.length > 0" class="comments">
      <CommentItem
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        @delete="handleDelete"
      />
    </div>
    
    <!-- 空状态 -->
    <div v-else class="empty">
      <p>📝 还没有评论，来发表第一条吧！</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  comments: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['comment-deleted'])

function handleDelete(commentId) {
  emit('comment-deleted', commentId)
}
</script>

<style scoped>
.loading,
.empty {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.comments {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>