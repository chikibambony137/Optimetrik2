<template>
  <div style="display: flex; justify-content: center; align-items: center; min-height: 100vh;">
    <div style="border: 2px solid black; border-radius: 20px; padding: 50px; max-width: 600px; width: 100%; background-color: #f5f5f5;">
      <h1 style="text-align: center; margin-bottom: 30px; font-size: 24px;">Авторизация</h1>
      
      <form @submit.prevent="handleLogin">
        <div style="margin-bottom: 25px;">
          <label style="display: block; text-align: left; margin-bottom: 5px;">Логин</label>
          <input 
            type="text" 
            v-model="login"
            style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px; font-size: 16px;"
          >
        </div>
        
        <div style="margin-bottom: 25px;">
          <label style="display: block; text-align: left; margin-bottom: 5px;">Пароль</label>
          <input 
            :type="showPassword ? 'text' : 'password'" 
            v-model="password"
            style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px; font-size: 16px;"
          >
          <div style="display: flex; justify-content: space-between; margin-top: 5px;">
          </div>
        </div>
        
        <button 
          type="submit"
          style="background-color: black; color: white; width: 100%; padding: 14px; border: none; border-radius: 15px; cursor: pointer; font-size: 18px;"
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