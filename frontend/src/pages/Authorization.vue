<template>
  <div style="display: flex; justify-content: center; align-items: center; min-height: 100vh;">
    <div style="border: 2px solid black; padding: 30px; max-width: 400px; width: 100%;">
      <h1 style="text-align: center;">Авторизация</h1>
      
      <form @submit.prevent="handleLogin">
        <div style="margin-bottom: 20px;">
          <label>Логин</label>
          <input 
            type="text" 
            v-model="login"
            style="width: 100%; margin-top: 5px;"
          >
          <div style="margin-top: 5px;">Value</div>
        </div>
        
        <div style="margin-bottom: 20px;">
          <label>Пароль</label>
          <input 
            :type="showPassword ? 'text' : 'password'" 
            v-model="password"
            style="width: 100%; margin-top: 5px;"
          >
          <div style="display: flex; justify-content: space-between; margin-top: 5px;">
            <span>Value</span>
            <button 
              type="button"
              @click="showPassword = !showPassword"
              style="background: none; border: none; cursor: pointer;"
            >
              👁
            </button>
          </div>
        </div>
        
        <button 
          type="submit"
          style="background-color: black; color: white; width: 100%; padding: 10px; border: none; cursor: pointer;"
        >
          Войти
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const login = ref('')
const password = ref('')
const showPassword = ref(false)

const handleLogin = () => {
  console.log('Login:', login.value)
  console.log('Password:', password.value)
}
</script>