<template>
  <div class="like-list" v-if="total > 0">
    <h4 class="like-list-title">❤️ {{ total }} 人觉得很赞</h4>
    <div class="likers">
      <div
        v-for="liker in likes"
        :key="liker.user_id"
        class="liker-item"
      >
        <img
          :src="liker.avatar ? `http://localhost:8000${liker.avatar}` : '/default-avatar.png'"
          :alt="liker.username"
          class="liker-avatar"
        />
        <span class="liker-name">{{ liker.username }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  articleId: { type: Number, required: true }
})

const { data } = await useFetch(
  `http://localhost:8000/api/articles/${props.articleId}/likes`
)

const likes = computed(() => data.value?.likes || [])
const total = computed(() => data.value?.total || 0)
</script>

<style scoped>
.like-list {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #fafafa;
  border-radius: 0.75rem;
}

.like-list-title {
  font-size: 0.95rem;
  color: #4a5568;
  margin-bottom: 0.75rem;
}

.likers {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.liker-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.3rem 0.6rem;
  background: white;
  border-radius: 9999px;
  border: 1px solid #e2e8f0;
}

.liker-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
}

.liker-name {
  font-size: 0.8rem;
  color: #4a5568;
}
</style>