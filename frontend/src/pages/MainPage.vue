<template>
  <div style="display: flex; min-height: 100vh; background-color: #f5f5f5; margin: 0; padding: 0;">
    <!-- Левая боковая панель с черными границами -->
    <div style="width: 260px; border-right: 1px solid black; background-color: #f5f5f5; display: flex; flex-direction: column; position: fixed; left: 0; top: 0; bottom: 0;">
      
      <!-- Логотип или название -->
      <div style="padding: 20px; border-bottom: 1px solid black;">
        <h2 style="margin: 0; font-size: 16px; color: black;">Система управления</h2>
      </div>
      
      <!-- Навигационные вкладки -->
      <div style="flex: 1; padding: 15px 10px; overflow-y: auto;">
        <div 
          v-for="item in filteredMenuItems" 
          :key="item.id"
          @click="navigateTo(item.route)"
          :style="{ 
            padding: '10px 15px', 
            margin: '4px 0',
            cursor: 'pointer',
            backgroundColor: isActiveRoute(item.route) ? 'white' : 'transparent',
            borderRadius: '8px',
            fontWeight: isActiveRoute(item.route) ? 'bold' : 'normal',
            fontSize: '14px',
            boxShadow: isActiveRoute(item.route) ? '0 2px 4px rgba(0,0,0,0.1)' : 'none'
          }"
        >
          {{ item.name }}
        </div>
      </div>
      
      <!-- Блок с информацией о пользователе (внизу) -->
      <div style="padding: 15px 20px; border-top: 1px solid black; background-color: #f5f5f5;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <!-- Фото-пустышка с черной обводкой -->
          <div style="width: 40px; height: 40px; border-radius: 50%; border: 1px solid black; background-color: white; display: flex; align-items: center; justify-content: center; color: black; font-size: 16px; font-weight: bold;">
            {{ userInitials }}
          </div>
          
          <!-- ФИО пользователя -->
          <div>
            <div style="font-weight: bold; margin-bottom: 2px; color: black; font-size: 13px;">{{ userFullName }}</div>
            <div style="font-size: 10px; color: #666;">{{ userRole }}</div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Правая основная область (с отступом от фиксированной левой панели) -->
    <div style="flex: 1; margin-left: 260px; min-height: 100vh; background-color: #f5f5f5;">
      <!-- Контент -->
      <div style="padding: 25px; background-color: #f5f5f5; min-height: 100vh;">
        <div style="padding: 20px; background-color: white; border-radius: 15px; width: 1000px;">
          <h2 style="margin-top: 0; margin-bottom: 20px; color: black; font-size: 20px;">{{ currentPageTitle }}</h2>
          
          <!-- Роутер-вью для отображения компонентов вкладок -->
          <router-view />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// Данные пользователя (в реальном проекте получать из БД/стора)
const userData = ref({
  id: 1,
  surname: 'Иванов',
  name: 'Иван',
  patronymic: 'Иванович',
  role: 'Администратор' // или 'Метролог' для проверки отображения
})

// Вычисляем инициалы
const userInitials = computed(() => {
  return (userData.value.surname.charAt(0) + userData.value.name.charAt(0)).toUpperCase()
})

// Вычисляем полное ФИО
const userFullName = computed(() => {
  return `${userData.value.surname} ${userData.value.name} ${userData.value.patronymic}`
})

// Вычисляем роль
const userRole = computed(() => {
  return userData.value.role
})

// Все пункты меню
const allMenuItems = ref([
  { id: 1, name: 'Журнал поверок', route: 'journal', roles: ['Администратор', 'Метролог'] },
  { id: 2, name: 'Эталонные средства', route: 'reference', roles: ['Администратор', 'Метролог'] },
  { id: 3, name: 'Тестовый стенд', route: 'test-tool', roles: ['Администратор', 'Метролог'] },
  { id: 4, name: 'Профиль', route: 'profile', roles: ['Администратор', 'Метролог'] },
  { id: 5, name: 'Пользователи', route: 'users', roles: ['Администратор'] } // Только для админа
])

// Фильтруем пункты меню по роли пользователя
const filteredMenuItems = computed(() => {
  return allMenuItems.value.filter(item => 
    item.roles.includes(userData.value.role)
  )
})

// Проверяем активный роут
const isActiveRoute = (routeName) => {
  return route.name === routeName
}

// Навигация
const navigateTo = (routeName) => {
  router.push({ name: routeName })
}

// Название текущей страницы
const currentPageTitle = computed(() => {
  const currentRoute = allMenuItems.value.find(item => item.route === route.name)
  return currentRoute ? currentRoute.name : 'Журнал поверок'
})
</script>

<style>
/* Глобальные стили для убирания отступов */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  background-color: #f5f5f5;
}
</style>