import { boot } from 'quasar/wrappers'
import axios from 'axios'

// Создаем экземпляр axios с базовым URL
const api = axios.create({ 
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:5173',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Добавляем перехватчик для токена
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Перехватчик ответов для обработки ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Неавторизован - перенаправляем на логин
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default boot(({ app }) => {
  // Добавляем api в глобальные свойства приложения
  app.config.globalProperties.$api = api
})

// Экспортируем api для использования в компонентах
export { api }