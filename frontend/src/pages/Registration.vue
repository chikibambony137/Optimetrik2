<template>
  <div style="display: flex; justify-content: center; align-items: center; min-height: 100vh;">
    <div style="border: 2px solid black; border-radius: 20px; padding: 40px; max-width: 450px; width: 100%; background-color: #f5f5f5;">
      <h1 style="text-align: center; margin-bottom: 30px;">Регистрация</h1>
      
      <form @submit.prevent="handleRegister">
        <!-- Фамилия -->
        <div style="margin-bottom: 15px;">
          <label style="display: block; text-align: left; margin-bottom: 5px;">Фамилия</label>
          <input 
            type="text" 
            v-model="surname"
            style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 5px;"
            :disabled="loading"
            required
          >
        </div>

        <!-- Имя -->
        <div style="margin-bottom: 15px;">
          <label style="display: block; text-align: left; margin-bottom: 5px;">Имя</label>
          <input 
            type="text" 
            v-model="name"
            style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 5px;"
            :disabled="loading"
            required
          >
        </div>

        <!-- Отчество (необязательное) -->
        <div style="margin-bottom: 15px;">
          <label style="display: block; text-align: left; margin-bottom: 5px;">Отчество (необязательно)</label>
          <input 
            type="text" 
            v-model="patronymic"
            style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 5px;"
            :disabled="loading"
          >
        </div>

        <!-- Логин -->
        <div style="margin-bottom: 15px;">
          <label style="display: block; text-align: left; margin-bottom: 5px;">Логин</label>
          <input 
            type="text" 
            v-model="login"
            style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 5px;"
            :disabled="loading"
            required
          >
        </div>
        
        <!-- Пароль -->
        <div style="margin-bottom: 15px;">
          <label style="display: block; text-align: left; margin-bottom: 5px;">Пароль</label>
          <input 
            :type="showPassword ? 'text' : 'password'" 
            v-model="password"
            style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 5px;"
            :disabled="loading"
            required
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

        <!-- Подтверждение пароля -->
        <div style="margin-bottom: 25px;">
          <label style="display: block; text-align: left; margin-bottom: 5px;">Повторите пароль</label>
          <input 
            :type="showConfirmPassword ? 'text' : 'password'" 
            v-model="confirmPassword"
            style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 5px;"
            :disabled="loading"
            required
          >
          <div style="display: flex; justify-content: flex-end; margin-top: 5px;">
            <button 
              type="button"
              @click="showConfirmPassword = !showConfirmPassword"
              style="background: none; border: none; color: #666; cursor: pointer; font-size: 12px;"
            >
              {{ showConfirmPassword ? 'Скрыть' : 'Показать' }}
            </button>
          </div>
        </div>
        
        <!-- Подсказка по паролю -->
        <div style="margin-bottom: 15px; padding: 8px; background-color: #f0f0f0; border-radius: 5px; font-size: 12px; color: #666;">
          <strong>Требования к паролю:</strong>
          <ul style="margin: 5px 0 0 20px;">
            <li>Минимум 6 символов</li>
            <li>Хотя бы одна заглавная буква (A-Z)</li>
            <li>Хотя бы одна цифра (0-9)</li>
          </ul>
        </div>
        
        <button 
          type="submit"
          style="background-color: black; color: white; width: 100%; padding: 12px; border: none; border-radius: 15px; cursor: pointer; font-size: 16px; margin-bottom: 15px;"
          :disabled="loading"
        >
          {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>

        <div style="text-align: center;">
          <span style="color: #666;">Уже есть аккаунт? </span>
          <button 
            type="button"
            @click="goToLogin"
            style="background: none; border: none; color: black; font-weight: bold; cursor: pointer; text-decoration: underline; font-size: 16px;"
            :disabled="loading"
          >
            Войти
          </button>
        </div>
      </form>

      <!-- Диалог успешной регистрации -->
      <Dialog
        v-model:show="showSuccessDialog"
        title="Регистрация"
        message="Регистрация прошла успешно! Теперь вы можете войти в систему."
        confirmText="Войти"
        @confirm="goToLogin"
      />

      <!-- Диалог ошибки -->
      <Dialog
        v-model:show="showErrorDialog"
        title="Ошибка регистрации"
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

// Поля формы
const surname = ref('')
const name = ref('')
const patronymic = ref('')
const login = ref('')
const password = ref('')
const confirmPassword = ref('')

// Состояния
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const loading = ref(false)
const showSuccessDialog = ref(false)
const showErrorDialog = ref(false)
const errorMessage = ref('')

// Валидация пароля
const validatePassword = (pass) => {
  if (pass.length < 6) return false
  if (!/[A-Z]/.test(pass)) return false
  if (!/[0-9]/.test(pass)) return false
  return true
}

// Обработка регистрации
const handleRegister = async () => {
  // Проверка заполнения обязательных полей
  if (!surname.value || !name.value || !login.value || !password.value) {
    errorMessage.value = 'Заполните все обязательные поля'
    showErrorDialog.value = true
    return
  }

  // Проверка совпадения паролей
  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Пароли не совпадают'
    showErrorDialog.value = true
    return
  }
  
  // Проверка сложности пароля
  if (!validatePassword(password.value)) {
    errorMessage.value = 'Пароль должен содержать минимум 6 символов, хотя бы одну заглавную букву и одну цифру'
    showErrorDialog.value = true
    return
  }
  
  loading.value = true

  try {
    // Отправка данных на бэкенд
    const response = await fetch('http://localhost:8000/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        login: login.value,
        surname: surname.value,
        name: name.value,
        patronymic: patronymic.value || null,
        admin_role: false, // По умолчанию все новые пользователи - метрологи
        password: password.value
      })
    })

    const data = await response.json()

    if (!response.ok) {
      // Обработка ошибок от сервера
      if (response.status === 400 && data.detail === 'Пользователь с таким логином уже существует') {
        throw new Error('Пользователь с таким логином уже существует')
      }
      throw new Error(data.detail || 'Ошибка регистрации')
    }

    // Успешная регистрация
    showSuccessDialog.value = true

  } catch (error) {
    console.error('Registration error:', error)
    errorMessage.value = error.message
    showErrorDialog.value = true
  } finally {
    loading.value = false
  }
}

const goToLogin = () => {
  router.push('/login')
}
</script>