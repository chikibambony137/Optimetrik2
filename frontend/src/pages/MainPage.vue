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
          @click="activeTab = item.id"
          :style="{ 
            padding: '10px 15px', 
            margin: '4px 0',
            cursor: 'pointer',
            backgroundColor: activeTab === item.id ? 'white' : 'transparent',
            borderRadius: '8px',
            fontWeight: activeTab === item.id ? 'bold' : 'normal',
            fontSize: '14px',
            boxShadow: activeTab === item.id ? '0 2px 4px rgba(0,0,0,0.1)' : 'none'
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
        <div style="padding: 20px; background-color: white; border-radius: 15px;">
          <h2 style="margin-top: 0; margin-bottom: 20px; color: black; font-size: 20px;">{{ currentTabName }}</h2>
          
          <!-- Заглушки для контента в зависимости от вкладки -->
          <div style="color: #666; font-size: 14px;">
            <div v-if="activeTab === 1">
              <h3 style="margin-bottom: 15px; font-size: 16px;">Журнал поверок</h3>
              <div v-for="i in 3" :key="i" style="padding: 12px; border: 1px solid #e0e0e0; margin-bottom: 10px; border-radius: 6px; background-color: #fafafa;">
                Поверка №{{ i }} - Средство измерения {{ i }}
              </div>
            </div>
            <div v-else-if="activeTab === 2">
              <h3 style="margin-bottom: 15px; font-size: 16px;">Эталонные средства</h3>
              <div v-for="i in 3" :key="i" style="padding: 12px; border: 1px solid #e0e0e0; margin-bottom: 10px; border-radius: 6px; background-color: #fafafa;">
                Эталонное средство {{ i }}
              </div>
            </div>
            <div v-else-if="activeTab === 3">
              <h3 style="margin-bottom: 15px; font-size: 16px;">Тестовый стенд</h3>
              <div v-for="i in 3" :key="i" style="padding: 12px; border: 1px solid #e0e0e0; margin-bottom: 10px; border-radius: 6px; background-color: #fafafa;">
                Тестовый стенд {{ i }}
              </div>
            </div>
            <div v-else-if="activeTab === 4">
              <h3 style="margin-bottom: 15px; font-size: 16px;">Профиль</h3>
              <div style="padding: 15px; border: 1px solid #e0e0e0; border-radius: 6px; background-color: #fafafa;">
                <p><strong>ФИО:</strong> {{ userFullName }}</p>
                <p><strong>Роль:</strong> {{ userRole }}</p>
                <p><strong>Логин:</strong> user{{ userData.value.id }}</p>
              </div>
            </div>
            <div v-else-if="activeTab === 5 && userData.value.role === 'Администратор'">
              <h3 style="margin-bottom: 15px; font-size: 16px;">Пользователи</h3>
              <div v-for="i in 3" :key="i" style="padding: 12px; border: 1px solid #e0e0e0; margin-bottom: 10px; border-radius: 6px; background-color: #fafafa;">
                Пользователь {{ i }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

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
  { id: 1, name: 'Журнал поверок', roles: ['Администратор', 'Метролог'] },
  { id: 2, name: 'Эталонные средства', roles: ['Администратор', 'Метролог'] },
  { id: 3, name: 'Тестовый стенд', roles: ['Администратор', 'Метролог'] },
  { id: 4, name: 'Профиль', roles: ['Администратор', 'Метролог'] },
  { id: 5, name: 'Пользователи', roles: ['Администратор'] } // Только для админа
])

// Фильтруем пункты меню по роли пользователя
const filteredMenuItems = computed(() => {
  return allMenuItems.value.filter(item => 
    item.roles.includes(userData.value.role)
  )
})

// Активная вкладка
const activeTab = ref(1)

// Название текущей вкладки
const currentTabName = computed(() => {
  const item = allMenuItems.value.find(item => item.id === activeTab.value)
  return item ? item.name : ''
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