// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    css: [
    '~/assets/css/variables.css'
  ],  
  modules: [
    '@nuxtjs/tailwindcss', // [!code ++]
    // ... 其他模块
  ],
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  srcDir: 'app/',
  nitro: {
    prerender: {
      failOnError: false,
    },
  },
  routeRules: {
    '/blog/publish': { prerender: false },
    '/blog/create': { prerender: false },
    '/blog/edit/**': { prerender: false },
    '/auth/**': { prerender: false },
    '/settings/**': { prerender: false },
    '/user/**': { prerender: false },
  },
})
