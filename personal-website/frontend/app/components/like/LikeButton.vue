<template>
  <div class="like-container">
    <button class="like-btn" :class="{ liked: isLiked }" @click="toggleLike" :disabled="loading">
      <span class="heart-icon">{{ isLiked ? '❤️' : '🤍' }}</span>
      <span class="like-count">{{ likeCount }}</span>
    </button>
    <div v-for="heart in floatingHearts" :key="heart.id" class="floating-heart" :style="heart.style">
      ❤️
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  articleId: { type: Number, required: true },
  initialLiked: { type: Boolean, default: false },
  initialCount: { type: Number, default: 0 }
})

const emit = defineEmits(['update'])

const { user, token, isLoggedIn } = useAuth()
const isLiked = ref(props.initialLiked)
const likeCount = ref(props.initialCount)
const loading = ref(false)
const floatingHearts = ref([])
let heartId = 0

async function toggleLike() {
  if (!isLoggedIn.value) {
    return navigateTo('/auth/login')
  }

  loading.value = true
  const wasLiked = isLiked.value
  isLiked.value = !isLiked.value
  likeCount.value += isLiked.value ? 1 : -1

  if (isLiked.value) {
    spawnHearts()
  }

  try {
    const res = await $fetch(`http://localhost:8000/api/articles/${props.articleId}/like`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    likeCount.value = res.like_count
    isLiked.value = res.liked
    emit('update', { liked: res.liked, count: res.like_count })
  } catch {
    isLiked.value = wasLiked
    likeCount.value = wasLiked ? props.initialCount : props.initialCount + 1
  } finally {
    loading.value = false
  }
}

function spawnHearts() {
  for (let i = 0; i < 6; i++) {
    const id = heartId++
    floatingHearts.value.push({
      id,
      style: {
        left: `${20 + Math.random() * 60}%`,
        animationDelay: `${Math.random() * 0.3}s`,
        fontSize: `${1 + Math.random() * 0.8}rem`
      }
    })
    setTimeout(() => {
      floatingHearts.value = floatingHearts.value.filter(h => h.id !== id)
    }, 1200)
  }
}
</script>

<style scoped>
.like-container {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.like-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1.25rem;
  border: 2px solid #e2e8f0;
  border-radius: 9999px;
  background: white;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.like-btn:hover {
  border-color: #fc8181;
  background: #fff5f5;
}

.like-btn.liked {
  border-color: #fc8181;
  background: #fff5f5;
}

.heart-icon {
  font-size: 1.25rem;
  line-height: 1;
}

.like-count {
  font-weight: 600;
  color: #4a5568;
}

.like-btn.liked .like-count {
  color: #e53e3e;
}

.floating-heart {
  position: absolute;
  bottom: 100%;
  left: 50%;
  pointer-events: none;
  animation: floatUp 1.2s ease-out forwards;
}

@keyframes floatUp {
  0% {
    opacity: 1;
    transform: translateY(0) scale(1) rotate(0deg);
  }
  100% {
    opacity: 0;
    transform: translateY(-80px) scale(0.5) rotate(45deg);
  }
}
</style>