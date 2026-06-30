<template>
  <div class="pagination" v-if="totalPages > 1">
    <button
      @click="goTo(currentPage - 1)"
      :disabled="currentPage <= 1"
      class="page-btn"
    >
      上一页
    </button>

    <button
      v-for="page in visiblePages"
      :key="page"
      @click="goTo(page)"
      class="page-btn"
      :class="{ active: page === currentPage }"
    >
      {{ page }}
    </button>

    <button
      @click="goTo(currentPage + 1)"
      :disabled="currentPage >= totalPages"
      class="page-btn"
    >
      下一页
    </button>

    <span class="page-info">
      第 {{ currentPage }} / {{ totalPages }} 页
    </span>
  </div>
</template>

<script setup>
const props = defineProps({
  currentPage: { type: Number, required: true },
  totalPages: { type: Number, required: true }
})

const emit = defineEmits(['change'])

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, props.currentPage - 2)
  const end = Math.min(props.totalPages, props.currentPage + 2)
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

function goTo(page) {
  if (page >= 1 && page <= props.totalPages && page !== props.currentPage) {
    emit('change', page)
  }
}
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem 0;
}

.page-btn {
  padding: 0.5rem 0.85rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.page-btn:hover:not(:disabled) {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.page-btn.active {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.875rem;
  color: var(--color-text-muted);
  margin-left: 0.5rem;
}
</style>