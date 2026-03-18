<template>
  <div>
    <!-- Заголовок и панель управления -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; color: black;">
      
      <div style="display: flex; gap: 10px; color: black">
        <!-- Расширенная строка поиска -->
        <div style="display: flex; gap: 5px;">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Поиск по названию, серийному номеру или дате..."
            style="padding: 8px 12px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px; width: 350px; background-color: white;"
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

        <!-- Кнопка обновления данных -->
        <button 
          @click="loadReferenceDevices"
          :disabled="loading"
          style="background-color: white; border: 1px solid #e0e0e0; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 14px; display: flex; align-items: center; gap: 5px;"
        >
          <span>🔄</span> {{ loading ? 'Загрузка...' : 'Обновить' }}
        </button>
      </div>
    </div>

    <!-- Индикатор загрузки -->
    <div v-if="loading" style="text-align: center; padding: 40px; color: #666;">
      Загрузка данных...
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

        <!-- Фильтр по дате поступления с -->
        <div>
          <label style="display: block; margin-bottom: 5px; font-size: 12px; color: #666;">Поступление с</label>
          <input type="date" v-model="filters.admissionFrom" style="width: 100%; padding: 8px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
        </div>

        <!-- Фильтр по дате поступления по -->
        <div>
          <label style="display: block; margin-bottom: 5px; font-size: 12px; color: #666;">Поступление по</label>
          <input type="date" v-model="filters.admissionTo" style="width: 100%; padding: 8px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
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
    <div v-if="!loading" style="overflow-x: auto; border: 1px solid #e0e0e0; border-radius: 8px;">
      <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
        <thead>
          <tr style="background-color: #f5f5f5; border-bottom: 2px solid #e0e0e0;">
            <th style="padding: 12px 15px; text-align: left;">ID</th>
            <th style="padding: 12px 15px; text-align: left;">Серийный номер</th>
            <th style="padding: 12px 15px; text-align: left;">Дата поступления</th>
            <th style="padding: 12px 15px; text-align: left;">Валиден до</th>
            <!-- Колонка действий ТОЛЬКО для администратора -->
            <th v-if="userRole === 'Администратор'" style="padding: 12px 15px; text-align: center;">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredData" :key="item.id" style="border-bottom: 1px solid #e0e0e0;">
            <td style="padding: 12px 15px;">{{ item.id }}</td>
            <td style="padding: 12px 15px;">{{ item.serial_number }}</td>
            <td style="padding: 12px 15px;">{{ formatDate(item.date_admission) }}</td>
            <td style="padding: 12px 15px;">
              <span :style="{ 
                padding: '4px 8px', 
                borderRadius: '4px', 
                fontSize: '12px',
                fontWeight: '500',
                backgroundColor: isExpired(item.valid_for) ? '#ffebee' : '#e8f5e8',
                color: isExpired(item.valid_for) ? '#d32f2f' : '#2e7d32'
              }">
                {{ formatDate(item.valid_for) }}
                <span v-if="isExpired(item.valid_for)" style="margin-left: 5px;">(просрочен)</span>
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
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Серийный номер</label>
          <input 
            v-model="modalForm.serial_number" 
            type="text" 
            style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;" 
            placeholder="Например: FL-87V-001"
            :disabled="saving"
          >
        </div>

        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Дата поступления</label>
          <input 
            v-model="modalForm.date_admission" 
            type="date" 
            style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;"
            :disabled="saving"
          >
        </div>

        <div style="margin-bottom: 20px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Валиден до</label>
          <input 
            v-model="modalForm.valid_for" 
            type="date" 
            style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;"
            :disabled="saving"
          >
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 10px;">
          <button @click="closeModal" style="padding: 10px 20px; background-color: white; border: 1px solid #e0e0e0; border-radius: 6px; cursor: pointer; font-size: 14px;" :disabled="saving">Отмена</button>
          <button @click="saveItem" :disabled="saving" style="padding: 10px 20px; background-color: black; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px;">
            {{ saving ? 'Сохранение...' : 'Сохранить' }}
          </button>
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

    <!-- Диалог ошибки -->
    <Dialog
      v-model:show="showErrorDialog"
      title="Ошибка"
      :message="errorMessage"
      confirmText="Понятно"
      @confirm="showErrorDialog = false"
    />

    <!-- Диалог успеха -->
    <Dialog
      v-model:show="showSuccessDialog"
      title="Успешно"
      :message="successMessage"
      confirmText="ОК"
      @confirm="showSuccessDialog = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Dialog from '../components/blocks/Dialog.vue'

const router = useRouter()
const API_BASE_URL = 'http://localhost:8000'

// Роль пользователя
const userRole = ref('Метролог')
const loading = ref(false)
const saving = ref(false)

// Состояние для поиска и фильтров
const searchQuery = ref('')
const showFilters = ref(false)
const filters = ref({
  validityStatus: 'all',
  admissionFrom: '',
  admissionTo: '',
  validFrom: '',
  validTo: ''
})

// Диалоги
const showErrorDialog = ref(false)
const showSuccessDialog = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Данные для таблицы
const tableData = ref([])

// Загрузка роли пользователя
const loadUserRole = () => {
  try {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      const user = JSON.parse(storedUser)
      userRole.value = user.admin_role ? 'Администратор' : 'Метролог'
    }
  } catch (error) {
    console.error('Error loading user role:', error)
  }
}

// Загрузка списка эталонов
const loadReferenceDevices = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }

  loading.value = true
  try {
    const url = filters.value.validityStatus === 'valid'
      ? `${API_BASE_URL}/reference-devices/?valid_only=true`
      : `${API_BASE_URL}/reference-devices/`
    
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (!response.ok) {
      if (response.status === 401) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')
        router.push('/login')
        return
      }
      throw new Error('Ошибка загрузки эталонов')
    }

    const data = await response.json()
    tableData.value = data
    console.log('Загружены эталоны:', data)
  } catch (error) {
    console.error('Error loading reference devices:', error)
    errorMessage.value = error.message || 'Ошибка загрузки эталонов'
    showErrorDialog.value = true
  } finally {
    loading.value = false
  }
}

// Фильтрация данных
const filteredData = computed(() => {
  return tableData.value.filter(item => {
    // Поиск по тексту
    const query = searchQuery.value.toLowerCase()
    const matchesSearch = query === '' || 
      item.serial_number?.toLowerCase().includes(query) ||
      formatDate(item.date_admission).toLowerCase().includes(query) ||
      formatDate(item.valid_for).toLowerCase().includes(query)
    
    // Фильтр по статусу валидности (на клиенте)
    let matchesValidity = true
    if (filters.value.validityStatus === 'valid') {
      matchesValidity = !isExpired(item.valid_for)
    } else if (filters.value.validityStatus === 'expired') {
      matchesValidity = isExpired(item.valid_for)
    }
    
    // Фильтр по дате поступления
    const matchesAdmissionFrom = !filters.value.admissionFrom || 
      item.date_admission >= filters.value.admissionFrom
    const matchesAdmissionTo = !filters.value.admissionTo || 
      item.date_admission <= filters.value.admissionTo
    
    // Фильтр по дате валидности
    const matchesValidFrom = !filters.value.validFrom || 
      item.valid_for >= filters.value.validFrom
    const matchesValidTo = !filters.value.validTo || 
      item.valid_for <= filters.value.validTo
    
    return matchesSearch && matchesValidity && 
           matchesAdmissionFrom && matchesAdmissionTo &&
           matchesValidFrom && matchesValidTo
  })
})

// Применить фильтры
const applyFilters = () => {
  showFilters.value = false
  if (filters.value.validityStatus !== 'all') {
    loadReferenceDevices() // Перезагружаем с сервера с фильтром valid_only
  }
}

// Сбросить фильтры
const resetFilters = () => {
  filters.value = {
    validityStatus: 'all',
    admissionFrom: '',
    admissionTo: '',
    validFrom: '',
    validTo: ''
  }
  loadReferenceDevices() // Перезагружаем все
}

// Проверка на просроченность
const isExpired = (dateStr) => {
  if (!dateStr) return false
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const validDate = new Date(dateStr)
  validDate.setHours(0, 0, 0, 0)
  return validDate < today
}

// Форматирование даты
const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  const date = new Date(dateStr)
  return date.toLocaleDateString('ru-RU')
}

// Модальное окно
const showModal = ref(false)
const modalTitle = ref('Добавить эталонное средство')
const editingId = ref(null)
const modalForm = ref({
  serial_number: '',
  date_admission: '',
  valid_for: ''
})

const openAddModal = () => {
  if (userRole.value !== 'Администратор') return
  modalTitle.value = 'Добавить эталонное средство'
  editingId.value = null
  modalForm.value = {
    serial_number: '',
    date_admission: '',
    valid_for: ''
  }
  showModal.value = true
}

const openEditModal = (item) => {
  if (userRole.value !== 'Администратор') {
    errorMessage.value = 'У вас нет прав для редактирования'
    showErrorDialog.value = true
    return
  }
  modalTitle.value = 'Редактировать эталонное средство'
  editingId.value = item.id
  modalForm.value = {
    serial_number: item.serial_number,
    date_admission: item.date_admission,
    valid_for: item.valid_for
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const saveItem = async () => {
  if (!modalForm.value.serial_number || !modalForm.value.date_admission || !modalForm.value.valid_for) {
    errorMessage.value = 'Заполните все поля'
    showErrorDialog.value = true
    return
  }

  // Проверка дат
  if (new Date(modalForm.value.valid_for) <= new Date(modalForm.value.date_admission)) {
    errorMessage.value = 'Дата окончания срока должна быть позже даты поступления'
    showErrorDialog.value = true
    return
  }

  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }

  saving.value = true
  try {
    if (editingId.value) {
      // Редактирование
      const response = await fetch(`${API_BASE_URL}/reference-devices/${editingId.value}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(modalForm.value)
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Ошибка при обновлении эталона')
      }

      successMessage.value = 'Эталон успешно обновлен'
    } else {
      // Добавление
      const response = await fetch(`${API_BASE_URL}/reference-devices/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(modalForm.value)
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Ошибка при создании эталона')
      }

      successMessage.value = 'Эталон успешно создан'
    }
    
    // Обновляем список
    await loadReferenceDevices()
    showSuccessDialog.value = true
    closeModal()
  } catch (error) {
    console.error('Error saving reference device:', error)
    errorMessage.value = error.message || 'Ошибка при сохранении эталона'
    showErrorDialog.value = true
  } finally {
    saving.value = false
  }
}

// Диалог удаления
const showDeleteDialog = ref(false)
const itemToDelete = ref(null)

const confirmDelete = (item) => {
  if (userRole.value !== 'Администратор') {
    errorMessage.value = 'У вас нет прав для удаления'
    showErrorDialog.value = true
    return
  }
  itemToDelete.value = item
  showDeleteDialog.value = true
}

const deleteMessage = computed(() => {
  return `Вы уверены, что хотите удалить эталон "${itemToDelete.value?.serial_number || ''}"?`
})

const deleteItem = async () => {
  if (!itemToDelete.value) return

  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }

  try {
    const response = await fetch(`${API_BASE_URL}/reference-devices/${itemToDelete.value.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Ошибка при удалении эталона')
    }

    // Обновляем список
    await loadReferenceDevices()
    successMessage.value = 'Эталон успешно удален'
    showSuccessDialog.value = true
  } catch (error) {
    console.error('Error deleting reference device:', error)
    errorMessage.value = error.message || 'Ошибка при удалении эталона'
    showErrorDialog.value = true
  } finally {
    showDeleteDialog.value = false
    itemToDelete.value = null
  }
}

// Инициализация при загрузке компонента
onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }
  loadUserRole()
  loadReferenceDevices()
})
</script>