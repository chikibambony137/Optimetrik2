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
        
        <button 
          type="submit"
          style="background-color: black; color: white; width: 100%; padding: 12px; border: none; border-radius: 15px; cursor: pointer; font-size: 16px; margin-bottom: 15px;"
        >
          Войти
        </button>

        <div style="text-align: center;">
          <span style="color: #666;">Нет аккаунта? </span>
          <button 
            type="button"
            @click="goToRegistration"
            style="background: none; border: none; color: black; font-weight: bold; cursor: pointer; text-decoration: underline; font-size: 16px;"
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

const handleLogin = () => {
  console.log('Login:', login.value)
  console.log('Password:', password.value)
  // Здесь будет логика входа
  showSuccessDialog.value = true
}

const goToRegistration = () => {
  router.push('/registration') // или путь к твоему компоненту регистрации
}
</script>