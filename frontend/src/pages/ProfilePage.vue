<template>
  <div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
      <!-- Левая колонка - информация о пользователе -->
      <div style="background-color: #fafafa; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px;">
        <h4 style="font-size: 16px; margin: 0 0 15px 0; color: #333;">Личная информация</h4>
        
        <div style="margin-bottom: 15px;">
          <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
            <!-- Аватар пользователя -->
            <div style="width: 60px; height: 60px; border-radius: 50%; border: 2px solid black; background-color: white; display: flex; align-items: center; justify-content: center; color: black; font-size: 24px; font-weight: bold;">
              {{ userInitials }}
            </div>
            <div>
              <div style="font-size: 18px; font-weight: bold;">{{ userFullName }}</div>
              <div style="font-size: 14px; color: #666;">{{ userRole }}</div>
            </div>
          </div>

          <div style="border-top: 1px solid #e0e0e0; padding-top: 15px;">
            <div style="display: flex; margin-bottom: 10px;">
              <div style="width: 120px; font-weight: 500; color: #666;">Логин:</div>
              <div>{{ userData.login }}</div>
            </div>
            
            <div style="display: flex; margin-bottom: 10px;">
              <div style="width: 120px; font-weight: 500; color: #666;">Фамилия:</div>
              <div>{{ userData.surname }}</div>
            </div>
            
            <div style="display: flex; margin-bottom: 10px;">
              <div style="width: 120px; font-weight: 500; color: #666;">Имя:</div>
              <div>{{ userData.name }}</div>
            </div>
            
            <div style="display: flex; margin-bottom: 10px;">
              <div style="width: 120px; font-weight: 500; color: #666;">Отчество:</div>
              <div>{{ userData.patronymic || '—' }}</div>
            </div>
            
            <div style="display: flex; margin-bottom: 10px;">
              <div style="width: 120px; font-weight: 500; color: #666;">Роль:</div>
              <div>
                <span :style="{ 
                  padding: '4px 8px', 
                  borderRadius: '4px', 
                  fontSize: '12px',
                  fontWeight: '500',
                  backgroundColor: userData.admin_role ? '#e3f2fd' : '#f5f5f5',
                  color: userData.admin_role ? '#1976d2' : '#666'
                }">
                  {{ userData.admin_role ? 'Администратор' : 'Пользователь' }}
                </span>
              </div>
            </div>

            <div style="display: flex; margin-bottom: 10px;" v-if="userData.id">
              <div style="width: 120px; font-weight: 500; color: #666;">ID:</div>
              <div>{{ userData.id }}</div>
            </div>
          </div>

          <!-- Кнопка обновления данных -->
          <div style="margin-top: 20px; display: flex; justify-content: flex-end;">
            <button 
              @click="refreshUserData"
              style="padding: 8px 16px; background-color: white; border: 1px solid #e0e0e0; border-radius: 6px; cursor: pointer; font-size: 14px; display: flex; align-items: center; gap: 5px;"
              :disabled="loading"
            >
              <span v-if="loading">⟳ Обновление...</span>
              <span v-else>⟳ Обновить данные</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Правая колонка - изменение пароля -->
      <div style="background-color: #fafafa; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px;">
        <h4 style="font-size: 16px; margin: 0 0 15px 0; color: #333;">Изменить пароль</h4>
        
        <form @submit.prevent="changePassword">
          <div style="margin-bottom: 15px;">
            <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Текущий пароль</label>
            <input 
              v-model="passwordForm.currentPassword" 
              :type="showCurrentPassword ? 'text' : 'password'"
              style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;"
              :disabled="passwordLoading"
            >
            <div style="display: flex; justify-content: flex-end; margin-top: 5px;">
              <button 
                type="button"
                @click="showCurrentPassword = !showCurrentPassword"
                style="background: none; border: none; color: #666; cursor: pointer; font-size: 12px;"
              >
                {{ showCurrentPassword ? '👁 Скрыть' : '👁 Показать' }}
              </button>
            </div>
          </div>

          <div style="margin-bottom: 15px;">
            <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Новый пароль</label>
            <input 
              v-model="passwordForm.newPassword" 
              :type="showNewPassword ? 'text' : 'password'"
              style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;"
              :disabled="passwordLoading"
            >
            <div style="display: flex; justify-content: flex-end; margin-top: 5px;">
              <button 
                type="button"
                @click="showNewPassword = !showNewPassword"
                style="background: none; border: none; color: #666; cursor: pointer; font-size: 12px;"
              >
                {{ showNewPassword ? '👁 Скрыть' : '👁 Показать' }}
              </button>
            </div>
          </div>

          <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Подтвердите новый пароль</label>
            <input 
              v-model="passwordForm.confirmPassword" 
              :type="showConfirmPassword ? 'text' : 'password'"
              style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;"
              :disabled="passwordLoading"
            >
            <div style="display: flex; justify-content: flex-end; margin-top: 5px;">
              <button 
                type="button"
                @click="showConfirmPassword = !showConfirmPassword"
                style="background: none; border: none; color: #666; cursor: pointer; font-size: 12px;"
              >
                {{ showConfirmPassword ? '👁 Скрыть' : '👁 Показать' }}
              </button>
            </div>
          </div>

          <div style="display: flex; gap: 10px; justify-content: flex-end;">
            <button 
              type="button"
              @click="resetPasswordForm"
              style="padding: 10px 20px; background-color: white; border: 1px solid #e0e0e0; border-radius: 6px; cursor: pointer; font-size: 14px;"
              :disabled="passwordLoading"
            >
              Очистить
            </button>
            <button 
              type="submit"
              style="padding: 10px 20px; background-color: black; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px;"
              :disabled="passwordLoading"
            >
              {{ passwordLoading ? 'Изменение...' : 'Изменить пароль' }}
            </button>
          </div>
        </form>

        <!-- Подсказки по паролю -->
        <div style="margin-top: 20px; padding: 10px; background-color: #f0f0f0; border-radius: 6px; font-size: 12px; color: #666;">
          <p style="margin: 0 0 5px 0;"><strong>Требования к паролю:</strong></p>
          <ul style="margin: 0; padding-left: 20px;">
            <li>Минимум 6 символов</li>
            <li>Хотя бы одна заглавная буква</li>
            <li>Хотя бы одна цифра</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Диалог успешного изменения пароля -->
    <Dialog
      v-model:show="showSuccessDialog"
      title="Успешно!"
      :message="successMessage"
      confirmText="ОК"
      @confirm="showSuccessDialog = false"
    />

    <!-- Диалог ошибки -->
    <Dialog
      v-model:show="showErrorDialog"
      title="Ошибка"
      :message="errorMessage"
      confirmText="Понятно"
      @confirm="showErrorDialog = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Dialog from '../components/blocks/Dialog.vue'

const router = useRouter()
const loading = ref(false)
const passwordLoading = ref(false)

// Данные пользователя из localStorage
const userData = ref({
  id: null,
  login: '',
  surname: '',
  name: '',
  patronymic: '',
  admin_role: false
})

// Состояние диалогов
const showSuccessDialog = ref(false)
const showErrorDialog = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Вычисляемые значения
const userInitials = computed(() => {
  if (userData.value.surname && userData.value.name) {
    return (userData.value.surname.charAt(0) + userData.value.name.charAt(0)).toUpperCase()
  }
  return '??'
})

const userFullName = computed(() => {
  const parts = [userData.value.surname, userData.value.name, userData.value.patronymic]
  return parts.filter(p => p && p.trim()).join(' ').trim() || 'Не указано'
})

const userRole = computed(() => userData.value.admin_role ? 'Администратор' : 'Пользователь')

// Форма изменения пароля
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// Состояние показа паролей
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

// Загрузка данных пользователя
const loadUserData = () => {
  try {
    // Пробуем получить данные из localStorage
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      userData.value = JSON.parse(storedUser)
    } else {
      // Если данных нет, пробуем получить через токен
      refreshUserData()
    }
  } catch (error) {
    console.error('Error loading user data:', error)
    errorMessage.value = 'Ошибка загрузки данных пользователя'
    showErrorDialog.value = true
  }
}

// Обновление данных пользователя с сервера
const refreshUserData = async () => {
  const token = localStorage.getItem('access_token')
  alert(token)
  if (!token) {
    router.push('/login')
    return
  }

  loading.value = true
  try {
    const response = await fetch('http://localhost:8000/users/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (!response.ok) {
      if (response.status === 401) {
        // Токен невалидный, перенаправляем на login
        localStorage.removeItem('access_token')
        localStorage.removeItem('token_type')
        localStorage.removeItem('user')
        router.push('/login')
        return
      }
      throw new Error('Ошибка получения данных')
    }

    const data = await response.json()
    userData.value = data
    localStorage.setItem('user', JSON.stringify(data))
    successMessage.value = 'Данные успешно обновлены'
    showSuccessDialog.value = true
  } catch (error) {
    console.error('Error refreshing user data:', error)
    errorMessage.value = error.message || 'Ошибка обновления данных'
    showErrorDialog.value = true
  } finally {
    loading.value = false
  }
}

// Валидация пароля
const validatePassword = (password) => {
  if (password.length < 6) return false
  if (!/[A-Z]/.test(password)) return false
  if (!/[0-9]/.test(password)) return false
  return true
}

// Смена пароля
const changePassword = async () => {
  // Проверка заполнения всех полей
  if (!passwordForm.value.currentPassword || !passwordForm.value.newPassword || !passwordForm.value.confirmPassword) {
    errorMessage.value = 'Заполните все поля'
    showErrorDialog.value = true
    return
  }

  // Проверка совпадения нового пароля и подтверждения
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    errorMessage.value = 'Новый пароль и подтверждение не совпадают'
    showErrorDialog.value = true
    return
  }

  // Проверка сложности пароля
  if (!validatePassword(passwordForm.value.newPassword)) {
    errorMessage.value = 'Пароль должен содержать минимум 6 символов, хотя бы одну заглавную букву и одну цифру'
    showErrorDialog.value = true
    return
  }

  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }

  passwordLoading.value = true
  try {
    const response = await fetch('http://localhost:8000/users/change-password', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        current_password: passwordForm.value.currentPassword,
        new_password: passwordForm.value.newPassword
      })
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || 'Ошибка при смене пароля')
    }

    // Успех
    successMessage.value = 'Пароль успешно изменен'
    showSuccessDialog.value = true
    resetPasswordForm()
  } catch (error) {
    console.error('Password change error:', error)
    errorMessage.value = error.message || 'Ошибка при смене пароля'
    showErrorDialog.value = true
  } finally {
    passwordLoading.value = false
  }
}

// Сброс формы пароля
const resetPasswordForm = () => {
  passwordForm.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
}

// Проверка авторизации при загрузке
onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }
  loadUserData()
})
</script>

<style scoped>
/* Дополнительные стили при необходимости */
</style>