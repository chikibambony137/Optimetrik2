<template>
  <div style="display: flex; justify-content: center; align-items: center; min-height: 100vh;">
    <div style="border: 2px solid black; border-radius: 20px; padding: 40px; max-width: 450px; width: 100%; background-color: #f5f5f5;">
      <h1 style="text-align: center; margin-bottom: 30px;">Регистрация</h1>
      
      <form @submit.prevent="handleRegister">
        <div style="margin-bottom: 25px;">
          <label style="display: block; text-align: left; margin-bottom: 5px;">Логин</label>
          <input 
            type="text" 
            v-model="login"
            style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 5px;"
          >
        </div>
        
        <div style="margin-bottom: 25px;">
          <label style="display: block; text-align: left; margin-bottom: 5px;">Пароль</label>
          <input 
            :type="showPassword ? 'text' : 'password'" 
            v-model="password"
            style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 5px;"
          >
        </div>

        <div style="margin-bottom: 25px;">
          <label style="display: block; text-align: left; margin-bottom: 5px;">Повторите пароль</label>
          <input 
            :type="showConfirmPassword ? 'text' : 'password'" 
            v-model="confirmPassword"
            style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 5px;"
          >
        </div>
        
        <button 
          type="submit"
          style="background-color: black; color: white; width: 100%; padding: 12px; border: none; border-radius: 15px; cursor: pointer; font-size: 16px; margin-bottom: 15px;"
        >
          Зарегистрироваться
        </button>

        <div style="text-align: center;">
          <span style="color: #666;">Уже есть аккаунт? </span>
          <button 
            type="button"
            @click="goToLogin"
            style="background: none; border: none; color: black; font-weight: bold; cursor: pointer; text-decoration: underline; font-size: 16px;"
          >
            Войти
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const login = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const handleRegister = () => {
  if (password.value !== confirmPassword.value) {
    alert('Пароли не совпадают!')
    return
  }
  
  if (password.value.length < 6) {
    alert('Пароль должен быть не менее 6 символов')
    return
  }
  
  console.log('Register:', login.value)
  console.log('Password:', password.value)
  // Здесь будет логика регистрации
}

const goToLogin = () => {
  router.push('/') // или путь к твоему компоненту авторизации
}
</script>