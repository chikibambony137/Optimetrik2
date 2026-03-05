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
            placeholder="Поиск по названию, серийному номеру или дате..."
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
        
        <!-- Фильтр по статусу валидности -->
        <div>
          <label style="display: block; margin-bottom: 5px; font-size: 12px; color: #666;">Статус</label>
          <select v-model="filters.validityStatus" style="width: 100%; padding: 8px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
            <option value="all">Все</option>
            <option value="valid">Валидные</option>
            <option value="expired">Просроченные</option>
          </select>
        </div>

        <!-- Фильтр по дате валидности с -->
        <div>
          <label style="display: block; margin-bottom: 5px; font-size: 12px; color: #666;">Валиден с</label>
          <input type="date" v-model="filters.validFrom" style="width: 100%; padding: 8px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
        </div>

        <!-- Фильтр по дате валидности по -->
        <div>
          <label style="display: block; margin-bottom: 5px; font-size: 12px; color: #666;">Валиден по</label>
          <input type="date" v-model="filters.validTo" style="width: 100%; padding: 8px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
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
            <th style="padding: 12px 15px; text-align: left;">Валиден до</th>
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
                backgroundColor: isExpired(item.validUntil) ? '#ffebee' : '#e8f5e8',
                color: isExpired(item.validUntil) ? '#d32f2f' : '#2e7d32'
              }">
                {{ formatDate(item.validUntil) }}
                <span v-if="isExpired(item.validUntil)" style="margin-left: 5px;">(просрочен)</span>
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

    <!-- Модальное окно для добавления/редактирования (без изменений) -->
    <div v-if="showModal" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000;" @click.self="closeModal">
      <!-- ... содержимое модального окна ... -->
      <div style="background-color: white; border-radius: 12px; padding: 25px; width: 500px; max-width: 90%; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
        <h3 style="margin-top: 0; margin-bottom: 20px; font-size: 18px;">{{ modalTitle }}</h3>
        
        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Серийный номер</label>
          <input v-model="modalForm.serialNumber" type="text" style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;" placeholder="Например: FL-87V-001">
        </div>

        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Название</label>
          <input v-model="modalForm.name" type="text" style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;" placeholder="Например: Мультиметр Fluke 87V">
        </div>

        <div style="margin-bottom: 20px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Валиден до</label>
          <input v-model="modalForm.validUntil" type="date" style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
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
  validityStatus: 'all',
  validFrom: '',
  validTo: ''
})

// Данные для таблицы
const tableData = ref([
  { id: 1, serialNumber: 'FL-87V-001', name: 'Мультиметр Fluke 87V', validUntil: '2026-06-15' },
  { id: 2, serialNumber: 'FL-5500A-002', name: 'Калибратор Fluke 5500A', validUntil: '2024-12-20' },
  { id: 3, serialNumber: 'TEK-TBS2000-003', name: 'Осциллограф Tektronix TBS2000', validUntil: '2025-03-10' },
  { id: 4, serialNumber: 'AKIP-3409-004', name: 'Генератор сигналов АКИП-3409/4', validUntil: '2026-02-01' },
  { id: 5, serialNumber: 'B5-71-005', name: 'Источник питания Б5-71', validUntil: '2023-08-25' },
  { id: 6, serialNumber: 'CH3-63-006', name: 'Частотомер Ч3-63', validUntil: '2027-11-30' }
])

// Фильтрация данных
const filteredData = computed(() => {
  return tableData.value.filter(item => {
    // Поиск по тексту
    const query = searchQuery.value.toLowerCase()
    const matchesSearch = query === '' || 
      item.name.toLowerCase().includes(query) || 
      item.serialNumber.toLowerCase().includes(query) ||
      formatDate(item.validUntil).toLowerCase().includes(query)
    
    // Фильтр по статусу валидности
    let matchesValidity = true
    if (filters.value.validityStatus === 'valid') {
      matchesValidity = !isExpired(item.validUntil)
    } else if (filters.value.validityStatus === 'expired') {
      matchesValidity = isExpired(item.validUntil)
    }
    
    // Фильтр по дате валидности
    const matchesValidFrom = !filters.value.validFrom || item.validUntil >= filters.value.validFrom
    const matchesValidTo = !filters.value.validTo || item.validUntil <= filters.value.validTo
    
    return matchesSearch && matchesValidity && matchesValidFrom && matchesValidTo
  })
})

// Применить фильтры
const applyFilters = () => {
  showFilters.value = false
}

// Сбросить фильтры
const resetFilters = () => {
  filters.value = {
    validityStatus: 'all',
    validFrom: '',
    validTo: ''
  }
}

// Проверка на просроченность
const isExpired = (date) => {
  if (!date) return false
  return new Date(date) < new Date()
}

// Форматирование даты
const formatDate = (date) => {
  if (!date) return '—'
  return new Date(date).toLocaleDateString('ru-RU')
}

// Модальное окно
const showModal = ref(false)
const modalTitle = ref('Добавить эталонное средство')
const editingId = ref(null)
const modalForm = ref({
  serialNumber: '',
  name: '',
  validUntil: ''
})

const openAddModal = () => {
  if (userRole.value !== 'Администратор') return
  modalTitle.value = 'Добавить эталонное средство'
  editingId.value = null
  modalForm.value = { serialNumber: '', name: '', validUntil: '' }
  showModal.value = true
}

const openEditModal = (item) => {
  if (userRole.value !== 'Администратор') {
    alert('У вас нет прав для редактирования')
    return
  }
  modalTitle.value = 'Редактировать эталонное средство'
  editingId.value = item.id
  modalForm.value = { ...item }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const saveItem = () => {
  if (!modalForm.value.serialNumber || !modalForm.value.name || !modalForm.value.validUntil) {
    alert('Заполните все поля')
    return
  }

  if (editingId.value) {
    if (userRole.value !== 'Администратор') return
    const index = tableData.value.findIndex(item => item.id === editingId.value)
    if (index !== -1) {
      tableData.value[index] = { ...modalForm.value, id: editingId.value }
    }
  } else {
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
  return `Вы уверены, что хотите удалить эталонное средство "${itemToDelete.value?.name || ''}"?`
})

const deleteItem = () => {
  if (itemToDelete.value && userRole.value === 'Администратор') {
    tableData.value = tableData.value.filter(item => item.id !== itemToDelete.value.id)
    itemToDelete.value = null
  }
}
</script>