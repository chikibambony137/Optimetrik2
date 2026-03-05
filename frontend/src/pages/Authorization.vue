<template>
  <div style="display: flex; justify-content: center; align-items: center; min-height: 100vh;">
    <div style="border: 2px solid black; border-radius: 20px; padding: 40px; max-width: 450px; width: 100%; background-color: #f5f5f5;">
      <h1 style="text-align: center; margin-bottom: 30px;">Авторизация</h1>
      
      <form @submit.prevent="handleLogin">
        <div style="margin-bottom: 25px;">
          <label style="display: block; text-align: left; margin-bottom: 5px;">Логин</label>
          <input 
            type="text" 
            v-model="login"
            style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 5px;"
            :disabled="loading"
          >
        </div>
        
        <div style="margin-bottom: 25px;">
          <label style="display: block; text-align: left; margin-bottom: 5px;">Пароль</label>
          <input 
            :type="showPassword ? 'text' : 'password'" 
            v-model="password"
            style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 5px;"
            :disabled="loading"
          >
          <div style="display: flex; justify-content: flex-end; margin-top: 5px;">
            <button 
              type="button"
              @click="showPassword = !showPassword"
              style="background: none; border: none; color: #666; cursor: pointer; font-size: 12px;"
            >
              {{ showPassword ? 'Скрыть' : 'Показать' }}
            </button>
          </div>
        </div>
        
        <button 
          type="submit"
          style="background-color: black; color: white; width: 100%; padding: 12px; border: none; border-radius: 15px; cursor: pointer; font-size: 16px; margin-bottom: 15px;"
          :disabled="loading"
        >
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>

        <div style="text-align: center;">
          <span style="color: #666;">Нет аккаунта? </span>
          <button 
            type="button"
            @click="goToRegistration"
            style="background: none; border: none; color: black; font-weight: bold; cursor: pointer; text-decoration: underline; font-size: 16px;"
            :disabled="loading"
          >
            Зарегистрироваться
          </button>
        </div>
      </form>
      
      <!-- Диалог успешного входа -->
      <Dialog
        v-model:show="showSuccessDialog"
        title="Успешный вход"
        message="Вы успешно авторизовались в системе!"
        confirmText="ОК"
        @confirm="handleSuccessConfirm"
      />

      <!-- Диалог ошибки -->
      <Dialog
        v-model:show="showErrorDialog"
        title="Ошибка входа"
        :message="errorMessage"
        confirmText="Понятно"
        @confirm="showErrorDialog = false"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Dialog from '../components/blocks/Dialog.vue'

const router = useRouter()

const login = ref('')
const password = ref('')
const showPassword = ref(false)
const showSuccessDialog = ref(false)
const showErrorDialog = ref(false)
const errorMessage = ref('')
const loading = ref(false)

const handleLogin = async () => {
  // Валидация
  if (!login.value || !password.value) {
    errorMessage.value = 'Заполните логин и пароль'
    showErrorDialog.value = true
    return
  }

  loading.value = true

  try {
    // Отправка запроса на бэкенд
    const response = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        'username': login.value,
        'password': password.value
      })
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || 'Ошибка авторизации')
    }

    // Сохраняем токен
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('token_type', data.token_type)

    // Получаем данные пользователя
    await fetchUserData()

    // Показываем успешный вход
    showSuccessDialog.value = true

  } catch (error) {
    console.error('Login error:', error)
    errorMessage.value = error.message || 'Неверный логин или пароль'
    showErrorDialog.value = true
  } finally {
    loading.value = false
  }
}

const fetchUserData = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('http://localhost:8000/users/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      const userData = await response.json()
      // Сохраняем данные пользователя
      localStorage.setItem('user', JSON.stringify(userData))
    }
  } catch (error) {
    console.error('Error fetching user data:', error)
  }
}

const handleSuccessConfirm = () => {
  router.push('/main/journal')
}

const goToRegistration = () => {
  router.push('/registration')
}
</script>