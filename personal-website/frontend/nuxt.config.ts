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
    preset: 'netlify_static',
  },
})
