// frontend/app/composables/usePermission.ts
export const usePermission = () => {
  const { user, isLoggedIn } = useAuth()
  
  // 检查是否有某个角色
  const hasRole = (role: string) => {
    if (!isLoggedIn.value || !user.value) return false
    
    const roleLevels: Record<string, number> = {
      reader: 1,
      author: 2,
    }
    
    const userLevel = roleLevels[user.value.role] || 0
    const requiredLevel = roleLevels[role] || 0
    
    return userLevel >= requiredLevel
  }
  
  // 常用权限检查
  const canComment = computed(() => isLoggedIn.value)
  const canPublish = computed(() => hasRole('author'))
  const isAuthor = computed(() => user.value?.role === 'author')
  
  // 检查是否是某篇文章的所有者
  const isOwner = (articleUserId: number) => {
    return user.value?.id === articleUserId
  }
  
  return {
    hasRole,
    canComment,
    canPublish,
    isAuthor,
    isOwner
  }
}