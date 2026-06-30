type Theme = 'light' | 'dark' | 'system'

export const useTheme = () => {
  // 当前主题设置（用户选择）
  const themeSetting = useState<Theme>('theme_setting', () => 'system')
  
  // 实际应用的主题（考虑系统偏好后的结果）
  const actualTheme = useState<'light' | 'dark'>('actual_theme', () => 'light')
  
  // 是否是暗色模式
  const isDark = computed(() => actualTheme.value === 'dark')
  
  // 获取系统主题偏好
  const getSystemTheme = (): 'light' | 'dark' => {
    if (process.server) return 'light'
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }
  
  // 应用主题到 DOM
  const applyTheme = (theme: 'light' | 'dark') => {
    if (process.server) return
    
    actualTheme.value = theme
    
    if (theme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }
  
  // 更新主题
  const updateTheme = () => {
    let theme: 'light' | 'dark'
    
    if (themeSetting.value === 'system') {
      theme = getSystemTheme()
    } else {
      theme = themeSetting.value
    }
    
    applyTheme(theme)
  }
  
  // 设置主题
  const setTheme = (theme: Theme) => {
    themeSetting.value = theme
    
    // 保存到 localStorage
    if (process.client) {
      localStorage.setItem('theme', theme)
    }
    
    updateTheme()
  }
  
  // 切换主题（在亮/暗之间切换）
  const toggleTheme = () => {
    const newTheme = isDark.value ? 'light' : 'dark'
    setTheme(newTheme)
  }
  
  // 初始化主题
  const initTheme = () => {
    if (process.server) return
    
    // 从 localStorage 读取用户设置
    const savedTheme = localStorage.getItem('theme') as Theme | null
    if (savedTheme) {
      themeSetting.value = savedTheme
    }
    
    updateTheme()
    
    // 监听系统主题变化
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      if (themeSetting.value === 'system') {
        updateTheme()
      }
    })
  }
  
  return {
    themeSetting,
    actualTheme,
    isDark,
    setTheme,
    toggleTheme,
    initTheme
  }
}