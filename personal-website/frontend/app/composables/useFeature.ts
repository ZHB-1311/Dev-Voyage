// frontend/app/composables/useFeature.ts

// 功能状态缓存
const featuresCache = ref<Record<string, boolean> | null>(null)
const featuresLoading = ref(false)

export const useFeature = () => {
  // 加载功能配置
  const loadFeatures = async () => {
    if (featuresCache.value || featuresLoading.value) return
    
    featuresLoading.value = true
    try {
      const data = await $fetch<Record<string, boolean>>(
        'http://localhost:8000/api/features'
      )
      featuresCache.value = data
    } catch (error) {
      console.error('加载功能配置失败:', error)
      // 失败时使用默认值
      featuresCache.value = {
        comment: true,
        like: false,
        favorite: false
      }
    } finally {
      featuresLoading.value = false
    }
  }
  
  // 检查功能是否开启
  const isEnabled = (featureName: string): boolean => {
    return featuresCache.value?.[featureName] ?? false
  }
  
  // 常用功能的快捷检查
  const commentEnabled = computed(() => isEnabled('comment'))
  const likeEnabled = computed(() => isEnabled('like'))
  const favoriteEnabled = computed(() => isEnabled('favorite'))
  
  return {
    loadFeatures,
    isEnabled,
    commentEnabled,
    likeEnabled,
    favoriteEnabled,
    isLoading: featuresLoading
  }
}