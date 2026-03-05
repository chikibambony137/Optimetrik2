<template>
  <div>
    <!-- Заголовок и панель управления -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
      
      <div style="display: flex; gap: 10px;">
        <!-- Поле поиска -->
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Поиск по названию..."
          style="padding: 8px 12px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px; width: 450px;"
        >

        <!-- Кнопка фильтра -->
        <button 
          @click="showFilters = !showFilters"
          style="background-color: white; border: 1px solid #e0e0e0; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 14px; display: flex; align-items: center; gap: 5px;"
        >
          <span>⚙️</span> Фильтр
        </button>

        <!-- Кнопка добавления (доступна ВСЕМ) -->
        <button 
          @click="openAddModal"
          style="background-color: black; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 14px; display: flex; align-items: center; gap: 5px;"
        >
          <span style="font-size: 18px;">+</span> Добавить
        </button>
      </div>
    </div>

    <!-- Панель фильтров (без изменений) -->
    <div v-if="showFilters" style="background-color: #fafafa; border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px; margin-bottom: 20px;">
      <!-- ... содержимое фильтров ... -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 15px;">
        <div>
          <label style="display: block; margin-bottom: 5px; font-size: 12px; color: #666;">Статус</label>
          <select v-model="filters.status" style="width: 100%; padding: 8px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
            <option value="">Все статусы</option>
            <option value="Запланирована">Запланирована</option>
            <option value="В процессе">В процессе</option>
            <option value="Завершена">Завершена</option>
          </select>
        </div>
        <div>
          <label style="display: block; margin-bottom: 5px; font-size: 12px; color: #666;">Планируемая дата с</label>
          <input type="date" v-model="filters.plannedFrom" style="width: 100%; padding: 8px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
        </div>
        <div>
          <label style="display: block; margin-bottom: 5px; font-size: 12px; color: #666;">Планируемая дата по</label>
          <input type="date" v-model="filters.plannedTo" style="width: 100%; padding: 8px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
        </div>
        <div>
          <label style="display: block; margin-bottom: 5px; font-size: 12px; color: #666;">Фактическая дата с</label>
          <input type="date" v-model="filters.actualFrom" style="width: 100%; padding: 8px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
        </div>
        <div>
          <label style="display: block; margin-bottom: 5px; font-size: 12px; color: #666;">Фактическая дата по</label>
          <input type="date" v-model="filters.actualTo" style="width: 100%; padding: 8px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
        </div>
      </div>
      <div style="display: flex; gap: 10px; justify-content: flex-end;">
        <button @click="resetFilters" style="padding: 6px 12px; background-color: white; border: 1px solid #e0e0e0; border-radius: 6px; cursor: pointer; font-size: 13px;">Сбросить фильтры</button>
        <button @click="applyFilters" style="padding: 6px 12px; background-color: black; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">Применить</button>
      </div>
    </div>

    <!-- Таблица -->
    <div style="overflow-x: auto; border: 1px solid #e0e0e0; border-radius: 8px;">
      <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
        <thead>
          <tr style="background-color: #f5f5f5; border-bottom: 2px solid #e0e0e0;">
            <th style="padding: 12px 15px; text-align: left;">Проверка</th>
            <th style="padding: 12px 15px; text-align: left;">Статус</th>
            <th style="padding: 12px 15px; text-align: left;">Планируемая дата</th>
            <th style="padding: 12px 15px; text-align: left;">Фактическая дата</th>
            <!-- Колонка действий ТОЛЬКО для администратора -->
            <th v-if="userRole === 'Администратор'" style="padding: 12px 15px; text-align: center;">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredData" :key="item.id" style="border-bottom: 1px solid #e0e0e0;">
            <td style="padding: 12px 15px;">{{ item.name }}</td>
            <td style="padding: 12px 15px;">
              <span :style="{ 
                padding: '4px 8px', 
                borderRadius: '4px', 
                fontSize: '12px',
                fontWeight: '500',
                backgroundColor: getStatusColor(item.status).bg,
                color: getStatusColor(item.status).text
              }">
                {{ item.status }}
              </span>
            </td>
            <td style="padding: 12px 15px;">{{ formatDate(item.plannedDate) }}</td>
            <td style="padding: 12px 15px;">{{ formatDate(item.actualDate) }}</td>
            
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
            <td :colspan="userRole === 'Администратор' ? 5 : 4" style="padding: 40px; text-align: center; color: #999;">
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
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Название проверки</label>
          <input v-model="modalForm.name" type="text" style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
        </div>

        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Статус</label>
          <select v-model="modalForm.status" style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
            <option value="Запланирована">Запланирована</option>
            <option value="В процессе">В процессе</option>
            <option value="Завершена">Завершена</option>
          </select>
        </div>

        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Планируемая дата</label>
          <input v-model="modalForm.plannedDate" type="date" style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
        </div>

        <div style="margin-bottom: 20px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Фактическая дата</label>
          <input v-model="modalForm.actualDate" type="date" style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
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

// Роль пользователя (в реальном проекте получать из стора)
// Для проверки можешь менять на 'Метролог'
const userRole = ref('Администратор') 

// Состояние для поиска и фильтров
const searchQuery = ref('')
const showFilters = ref(false)
const filters = ref({
  status: '',
  plannedFrom: '',
  plannedTo: '',
  actualFrom: '',
  actualTo: ''
})

// Данные для таблицы
const tableData = ref([
  { id: 1, name: 'Поверка мультиметра Fluke 87V', status: 'Завершена', plannedDate: '2024-03-15', actualDate: '2024-03-15' },
  { id: 2, name: 'Поверка калибратора Fluke 5500A', status: 'В процессе', plannedDate: '2024-03-20', actualDate: '' },
  { id: 3, name: 'Поверка осциллографа Tektronix TBS2000', status: 'Запланирована', plannedDate: '2024-04-01', actualDate: '' },
  { id: 4, name: 'Поверка генератора сигналов АКИП-3409/4', status: 'Завершена', plannedDate: '2024-02-28', actualDate: '2024-02-28' },
  { id: 5, name: 'Поверка источника питания Б5-71', status: 'Завершена', plannedDate: '2024-03-10', actualDate: '2024-03-10' },
  { id: 6, name: 'Поверка частотомера Ч3-63', status: 'В процессе', plannedDate: '2024-03-25', actualDate: '' }
])

// Вычисляемые данные для отображения с учетом фильтров
const filteredData = computed(() => {
  return tableData.value.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesStatus = !filters.value.status || item.status === filters.value.status
    const matchesPlannedFrom = !filters.value.plannedFrom || item.plannedDate >= filters.value.plannedFrom
    const matchesPlannedTo = !filters.value.plannedTo || item.plannedDate <= filters.value.plannedTo
    const matchesActualFrom = !filters.value.actualFrom || (item.actualDate && item.actualDate >= filters.value.actualFrom)
    const matchesActualTo = !filters.value.actualTo || (item.actualDate && item.actualDate <= filters.value.actualTo)
    
    return matchesSearch && matchesStatus && matchesPlannedFrom && matchesPlannedTo && matchesActualFrom && matchesActualTo
  })
})

// Применить фильтры
const applyFilters = () => {
  showFilters.value = false
}

// Сбросить фильтры
const resetFilters = () => {
  filters.value = {
    status: '',
    plannedFrom: '',
    plannedTo: '',
    actualFrom: '',
    actualTo: ''
  }
}

// Цвет статуса
const getStatusColor = (status) => {
  switch(status) {
    case 'Завершена': return { bg: '#e8f5e8', text: '#2e7d32' }
    case 'В процессе': return { bg: '#fff4e5', text: '#f57c00' }
    case 'Запланирована': return { bg: '#e3f2fd', text: '#1976d2' }
    default: return { bg: '#f5f5f5', text: '#666' }
  }
}

// Форматирование даты
const formatDate = (date) => {
  if (!date) return '—'
  return new Date(date).toLocaleDateString('ru-RU')
}

// Модальное окно (доступно всем)
const showModal = ref(false)
const modalTitle = ref('Добавить поверку')
const editingId = ref(null)
const modalForm = ref({
  name: '',
  status: 'Запланирована',
  plannedDate: '',
  actualDate: ''
})

const openAddModal = () => {
  modalTitle.value = 'Добавить поверку'
  editingId.value = null
  modalForm.value = {
    name: '',
    status: 'Запланирована',
    plannedDate: '',
    actualDate: ''
  }
  showModal.value = true
}

// Редактирование - ТОЛЬКО для администратора
const openEditModal = (item) => {
  if (userRole.value !== 'Администратор') {
    alert('У вас нет прав для редактирования')
    return
  }
  modalTitle.value = 'Редактировать поверку'
  editingId.value = item.id
  modalForm.value = { ...item }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const saveItem = () => {
  if (!modalForm.value.name) {
    alert('Введите название проверки')
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
    // Добавление (доступно всем)
    const newId = Math.max(...tableData.value.map(item => item.id)) + 1
    tableData.value.push({ ...modalForm.value, id: newId })
  }
  closeModal()
}

// Диалог удаления (только для администратора)
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
  return `Вы уверены, что хотите удалить проверку "${itemToDelete.value?.name || ''}"?`
})

const deleteItem = () => {
  if (itemToDelete.value && userRole.value === 'Администратор') {
    tableData.value = tableData.value.filter(item => item.id !== itemToDelete.value.id)
    itemToDelete.value = null
  }
}
</script>