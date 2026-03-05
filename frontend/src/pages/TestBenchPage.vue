<template>
  <div>
    <!-- Заголовок и панель управления -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
      
      <div style="display: flex; gap: 10px;">
        <!-- Расширенная строка поиска -->
        <div style="display: flex; gap: 5px;">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Поиск по названию или серийному номеру..."
            style="padding: 8px 12px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px; width: 350px;"
          >
        </div>

        <!-- Кнопка фильтра -->
        <button 
          @click="showFilters = !showFilters"
          style="background-color: white; border: 1px solid #e0e0e0; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 14px; display: flex; align-items: center; gap: 5px;"
        >
          <span>⚙️</span> Фильтр
        </button>

        <!-- Кнопка добавления (только для админа) -->
        <button 
          v-if="userRole === 'Администратор'"
          @click="openAddModal"
          style="background-color: black; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 14px; display: flex; align-items: center; gap: 5px;"
        >
          <span style="font-size: 18px;">+</span> Добавить
        </button>
      </div>
    </div>

    <!-- Панель фильтров -->
    <div v-if="showFilters" style="background-color: #fafafa; border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px; margin-bottom: 20px;">
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 15px;">
        
        <!-- Фильтр по статусу активности -->
        <div>
          <label style="display: block; margin-bottom: 5px; font-size: 12px; color: #666;">Статус</label>
          <select v-model="filters.activeStatus" style="width: 100%; padding: 8px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
            <option value="all">Все</option>
            <option value="active">Активные</option>
            <option value="inactive">Неактивные</option>
          </select>
        </div>
      </div>

      <!-- Кнопки управления фильтрами -->
      <div style="display: flex; gap: 10px; justify-content: flex-end;">
        <button 
          @click="resetFilters"
          style="padding: 6px 12px; background-color: white; border: 1px solid #e0e0e0; border-radius: 6px; cursor: pointer; font-size: 13px;"
        >
          Сбросить фильтры
        </button>
        <button 
          @click="applyFilters"
          style="padding: 6px 12px; background-color: black; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;"
        >
          Применить
        </button>
      </div>
    </div>

    <!-- Таблица -->
    <div style="overflow-x: auto; border: 1px solid #e0e0e0; border-radius: 8px;">
      <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
        <thead>
          <tr style="background-color: #f5f5f5; border-bottom: 2px solid #e0e0e0;">
            <th style="padding: 12px 15px; text-align: left;">Серийный номер</th>
            <th style="padding: 12px 15px; text-align: left;">Название</th>
            <th style="padding: 12px 15px; text-align: left;">Активен</th>
            <!-- Колонка действий ТОЛЬКО для администратора -->
            <th v-if="userRole === 'Администратор'" style="padding: 12px 15px; text-align: center;">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredData" :key="item.id" style="border-bottom: 1px solid #e0e0e0;">
            <td style="padding: 12px 15px;">{{ item.serialNumber }}</td>
            <td style="padding: 12px 15px;">{{ item.name }}</td>
            <td style="padding: 12px 15px;">
              <span :style="{ 
                padding: '4px 8px', 
                borderRadius: '4px', 
                fontSize: '12px',
                fontWeight: '500',
                backgroundColor: item.active ? '#e8f5e8' : '#ffebee',
                color: item.active ? '#2e7d32' : '#d32f2f'
              }">
                {{ item.active ? 'Да' : 'Нет' }}
              </span>
            </td>
            
            <!-- Кнопки действий ТОЛЬКО для администратора -->
            <td v-if="userRole === 'Администратор'" style="padding: 12px 15px; text-align: center;">
              <div style="display: flex; gap: 8px; justify-content: center;">
                <button 
                  @click="openEditModal(item)" 
                  style="background: none; border: 1px solid #e0e0e0; border-radius: 4px; padding: 4px 8px; cursor: pointer;"
                  title="Редактировать"
                >
                  ✏️ Ред.
                </button>
                <button 
                  @click="confirmDelete(item)" 
                  style="background: none; border: 1px solid #ffcdd2; border-radius: 4px; padding: 4px 8px; cursor: pointer; color: #d32f2f;"
                  title="Удалить"
                >
                  🗑️ Удал.
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="filteredData.length === 0">
            <td :colspan="userRole === 'Администратор' ? 4 : 3" style="padding: 40px; text-align: center; color: #999;">
              Нет данных, соответствующих критериям поиска
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модальное окно для добавления/редактирования -->
    <div v-if="showModal" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000;" @click.self="closeModal">
      <div style="background-color: white; border-radius: 12px; padding: 25px; width: 500px; max-width: 90%; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
        <h3 style="margin-top: 0; margin-bottom: 20px; font-size: 18px;">{{ modalTitle }}</h3>
        
        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Серийный номер</label>
          <input v-model="modalForm.serialNumber" type="text" style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;" placeholder="Например: TB-001">
        </div>

        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Название</label>
          <input v-model="modalForm.name" type="text" style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;" placeholder="Например: Тестовый стенд №1">
        </div>

        <div style="margin-bottom: 20px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Активен</label>
          <div style="display: flex; gap: 20px;">
            <label style="display: flex; align-items: center; gap: 5px;">
              <input type="radio" v-model="modalForm.active" :value="true"> Да
            </label>
            <label style="display: flex; align-items: center; gap: 5px;">
              <input type="radio" v-model="modalForm.active" :value="false"> Нет
            </label>
          </div>
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 10px;">
          <button @click="closeModal" style="padding: 10px 20px; background-color: white; border: 1px solid #e0e0e0; border-radius: 6px; cursor: pointer; font-size: 14px;">Отмена</button>
          <button @click="saveItem" style="padding: 10px 20px; background-color: black; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px;">Сохранить</button>
        </div>
      </div>
    </div>

    <!-- Диалог подтверждения удаления -->
    <Dialog
      v-model:show="showDeleteDialog"
      title="Подтверждение удаления"
      :message="deleteMessage"
      confirmText="Удалить"
      @confirm="deleteItem"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Dialog from '../components/blocks/Dialog.vue'

// Роль пользователя
const userRole = ref('Администратор') // Для проверки меняй на 'Метролог'

// Состояние для поиска и фильтров
const searchQuery = ref('')
const showFilters = ref(false)
const filters = ref({
  activeStatus: 'all'
})

// Данные для таблицы
const tableData = ref([
  { id: 1, serialNumber: 'TB-001', name: 'Тестовый стенд №1 (Основной)', active: true },
  { id: 2, serialNumber: 'TB-002', name: 'Тестовый стенд №2 (Резервный)', active: true },
  { id: 3, serialNumber: 'TB-003', name: 'Тестовый стенд №3 (В ремонте)', active: false },
  { id: 4, serialNumber: 'TB-004', name: 'Тестовый стенд для мультиметров', active: true },
  { id: 5, serialNumber: 'TB-005', name: 'Тестовый стенд для осциллографов', active: false },
  { id: 6, serialNumber: 'TB-006', name: 'Тестовый стенд высоковольтный', active: true }
])

// Фильтрация данных
const filteredData = computed(() => {
  return tableData.value.filter(item => {
    // Поиск по тексту
    const query = searchQuery.value.toLowerCase()
    const matchesSearch = query === '' || 
      item.name.toLowerCase().includes(query) || 
      item.serialNumber.toLowerCase().includes(query)
    
    // Фильтр по статусу активности
    let matchesActive = true
    if (filters.value.activeStatus === 'active') {
      matchesActive = item.active === true
    } else if (filters.value.activeStatus === 'inactive') {
      matchesActive = item.active === false
    }
    
    return matchesSearch && matchesActive
  })
})

// Применить фильтры
const applyFilters = () => {
  showFilters.value = false
}

// Сбросить фильтры
const resetFilters = () => {
  filters.value = {
    activeStatus: 'all'
  }
}

// Модальное окно
const showModal = ref(false)
const modalTitle = ref('Добавить тестовый стенд')
const editingId = ref(null)
const modalForm = ref({
  serialNumber: '',
  name: '',
  active: true
})

const openAddModal = () => {
  if (userRole.value !== 'Администратор') return
  modalTitle.value = 'Добавить тестовый стенд'
  editingId.value = null
  modalForm.value = {
    serialNumber: '',
    name: '',
    active: true
  }
  showModal.value = true
}

const openEditModal = (item) => {
  if (userRole.value !== 'Администратор') {
    alert('У вас нет прав для редактирования')
    return
  }
  modalTitle.value = 'Редактировать тестовый стенд'
  editingId.value = item.id
  modalForm.value = { ...item }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const saveItem = () => {
  if (!modalForm.value.serialNumber || !modalForm.value.name) {
    alert('Заполните все поля')
    return
  }

  if (editingId.value) {
    // Редактирование (только админ)
    if (userRole.value !== 'Администратор') return
    const index = tableData.value.findIndex(item => item.id === editingId.value)
    if (index !== -1) {
      tableData.value[index] = { ...modalForm.value, id: editingId.value }
    }
  } else {
    // Добавление (только админ)
    if (userRole.value !== 'Администратор') return
    const newId = Math.max(...tableData.value.map(item => item.id)) + 1
    tableData.value.push({ ...modalForm.value, id: newId })
  }
  closeModal()
}

// Диалог удаления
const showDeleteDialog = ref(false)
const itemToDelete = ref(null)

const confirmDelete = (item) => {
  if (userRole.value !== 'Администратор') {
    alert('У вас нет прав для удаления')
    return
  }
  itemToDelete.value = item
  showDeleteDialog.value = true
}

const deleteMessage = computed(() => {
  return `Вы уверены, что хотите удалить тестовый стенд "${itemToDelete.value?.name || ''}"?`
})

const deleteItem = () => {
  if (itemToDelete.value && userRole.value === 'Администратор') {
    tableData.value = tableData.value.filter(item => item.id !== itemToDelete.value.id)
    itemToDelete.value = null
  }
}
</script>