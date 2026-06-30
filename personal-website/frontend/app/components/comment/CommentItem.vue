<!-- frontend/app/components/comment/CommentItem.vue -->
<template>
  <div class="comment-item">
    <div class="comment-avatar">
      {{ comment.user?.username?.charAt(0).toUpperCase() || '?' }}
    </div>
    
    <div class="comment-body">
      <div class="comment-header">
        <span class="username">{{ comment.user?.username || '未知用户' }}</span>
        <span class="time">{{ comment.created_at }}</span>
      </div>
      
      <div class="comment-content">
        {{ comment.content }}
      </div>
      
      <div class="comment-actions">
        <button 
          v-if="canDelete" 
          @click="handleDelete"
          class="btn-delete"
          :disabled="isDeleting"
        >
          {{ isDeleting ? '删除中...' : '删除' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  comment: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['delete'])

const { user, token, isLoggedIn } = useAuth()

// 是否可以删除（只能删除自己的评论）
const canDelete = computed(() => {
  return isLoggedIn.value && user.value?.id === props.comment.user?.id
})

const isDeleting = ref(false)

async function handleDelete() {
  if (!confirm('确定要删除这条评论吗？')) return
  
  isDeleting.value = true
  
  try {
    await $fetch(`http://localhost:8000/api/comments/${props.comment.id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    
    emit('delete', props.comment.id)
  } catch (error) {
    alert('删除失败：' + (error.data?.detail || '未知错误'))
  } finally {
    isDeleting.value = false
  }
}
</script>

<style scoped>
.comment-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.5rem;
}

.comment-avatar {
  width: 36px;
  height: 36px;
  background: #e5e7eb;
  color: #6b7280;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.comment-body {
  flex: 1;
  min-width: 0;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.username {
  font-weight: 600;
  color: #374151;
}

.time {
  font-size: 0.875rem;
  color: #9ca3af;
}

.comment-content {
  color: #4b5563;
  line-height: 1.6;
  word-break: break-word;
}

.comment-actions {
  margin-top: 0.5rem;
}

.btn-delete {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  color: #dc2626;
  background: transparent;
  border: 1px solid #fecaca;
  border-radius: 0.25rem;
  cursor: pointer;
}

.btn-delete:hover {
  background: #fef2f2;
}

.btn-delete:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>