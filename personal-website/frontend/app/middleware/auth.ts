// frontend/app/middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const { isLoggedIn } = useAuth()
  
  // 如果未登录，重定向到登录页
  if (!isLoggedIn.value) {
    return navigateTo({
      path: '/auth/login',
      query: { redirect: to.fullPath }  // 记录原本要去的页面
    })
  }
})