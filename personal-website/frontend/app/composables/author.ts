// frontend/app/middleware/author.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const { user, isLoggedIn } = useAuth()
  
  // 先检查是否登录
  if (!isLoggedIn.value) {
    return navigateTo({
      path: '/auth/login',
      query: { redirect: to.fullPath }
    })
  }
  
  // 再检查是否是作者
  if (user.value?.role !== 'author') {
    // 可以跳转到提示页面，或者返回上一页
    return navigateTo({
      path: '/user',
      query: { message: 'need-author' }  // 提示需要成为作者
    })
  }
})