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
            placeholder="Поиск по серийному номеру..."
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

        <!-- Кнопка обновления данных -->
        <button 
          @click="loadTestTools"
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
      </div>
    </div>

    <!-- Таблица -->
    <div v-if="!loading" style="overflow-x: auto; border: 1px solid #e0e0e0; border-radius: 8px;">
      <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
        <thead>
          <tr style="background-color: #f5f5f5; border-bottom: 2px solid #e0e0e0;">
            <th style="padding: 12px 15px; text-align: left;">ID</th>
            <th style="padding: 12px 15px; text-align: left;">Серийный номер</th>
            <th style="padding: 12px 15px; text-align: left;">Активен</th>
            <!-- Колонка действий ТОЛЬКО для администратора -->
            <th v-if="userRole === 'Администратор'" style="padding: 12px 15px; text-align: center;">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredData" :key="item.id" style="border-bottom: 1px solid #e0e0e0;">
            <td style="padding: 12px 15px;">{{ item.id }}</td>
            <td style="padding: 12px 15px;">{{ item.serial_number }}</td>
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
                  @click="toggleActive(item)" 
                  style="background: none; border: 1px solid #e0e0e0; border-radius: 4px; padding: 4px 8px; cursor: pointer;"
                  :title="item.active ? 'Деактивировать' : 'Активировать'"
                >
                  {{ item.active ? '🔴 Деакт.' : '🟢 Акт.' }}
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
          <input 
            v-model="modalForm.serial_number" 
            type="text" 
            style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;" 
            placeholder="Например: TB-001"
            :disabled="saving"
          >
        </div>

        <div style="margin-bottom: 20px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Активен</label>
          <div style="display: flex; gap: 20px;">
            <label style="display: flex; align-items: center; gap: 5px;">
              <input type="radio" v-model="modalForm.active" :value="true" :disabled="saving"> Да
            </label>
            <label style="display: flex; align-items: center; gap: 5px;">
              <input type="radio" v-model="modalForm.active" :value="false" :disabled="saving"> Нет
            </label>
          </div>
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

// Роль пользователя (получаем из localStorage)
const userRole = ref('Метролог')
const loading = ref(false)
const saving = ref(false)

// Состояние для поиска и фильтров
const searchQuery = ref('')
const showFilters = ref(false)
const filters = ref({
  activeStatus: 'all'
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

// Загрузка списка тестовых стендов
const loadTestTools = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }

  loading.value = true
  try {
    // Всегда загружаем все стенды, фильтрацию делаем на клиенте
    const response = await fetch(`${API_BASE_URL}/test-tools/`, {
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
      throw new Error('Ошибка загрузки тестовых стендов')
    }

    const data = await response.json()
    tableData.value = data
    console.log('Загружены тестовые стенды:', data)
  } catch (error) {
    console.error('Error loading test tools:', error)
    errorMessage.value = error.message || 'Ошибка загрузки тестовых стендов'
    showErrorDialog.value = true
  } finally {
    loading.value = false
  }
}

// Фильтрация данных (на клиенте)
const filteredData = computed(() => {
  return tableData.value.filter(item => {
    // Поиск по тексту
    const query = searchQuery.value.toLowerCase()
    const matchesSearch = query === '' || 
      item.serial_number?.toLowerCase().includes(query)
    
    // Фильтр по статусу (на клиенте)
    let matchesActive = true
    if (filters.value.activeStatus === 'active') {
      matchesActive = item.active === true
    } else if (filters.value.activeStatus === 'inactive') {
      matchesActive = item.active === false
    }
    
    return matchesSearch && matchesActive
  })
})

// Сбросить фильтры
const resetFilters = () => {
  filters.value = {
    activeStatus: 'all'
  }
  // Не перезагружаем с сервера
}

// Модальное окно
const showModal = ref(false)
const modalTitle = ref('Добавить тестовый стенд')
const editingId = ref(null)
const modalForm = ref({
  serial_number: '',
  active: true
})

const openAddModal = () => {
  if (userRole.value !== 'Администратор') return
  modalTitle.value = 'Добавить тестовый стенд'
  editingId.value = null
  modalForm.value = {
    serial_number: '',
    active: true
  }
  showModal.value = true
}

const openEditModal = (item) => {
  if (userRole.value !== 'Администратор') {
    errorMessage.value = 'У вас нет прав для редактирования'
    showErrorDialog.value = true
    return
  }
  modalTitle.value = 'Редактировать тестовый стенд'
  editingId.value = item.id
  modalForm.value = {
    serial_number: item.serial_number,
    active: item.active
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const saveItem = async () => {
  if (!modalForm.value.serial_number) {
    errorMessage.value = 'Заполните серийный номер'
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
      const response = await fetch(`${API_BASE_URL}/test-tools/${editingId.value}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(modalForm.value)
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Ошибка при обновлении тестового стенда')
      }

      successMessage.value = 'Тестовый стенд успешно обновлен'
    } else {
      // Добавление
      const response = await fetch(`${API_BASE_URL}/test-tools/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(modalForm.value)
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Ошибка при создании тестового стенда')
      }

      successMessage.value = 'Тестовый стенд успешно создан'
    }
    
    // Обновляем список
    await loadTestTools()
    showSuccessDialog.value = true
    closeModal()
  } catch (error) {
    console.error('Error saving test tool:', error)
    errorMessage.value = error.message || 'Ошибка при сохранении тестового стенда'
    showErrorDialog.value = true
  } finally {
    saving.value = false
  }
}

// Переключение статуса активности
const toggleActive = async (item) => {
  if (userRole.value !== 'Администратор') {
    errorMessage.value = 'У вас нет прав для изменения статуса'
    showErrorDialog.value = true
    return
  }

  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }

  try {
    const response = await fetch(`${API_BASE_URL}/test-tools/${item.id}/toggle`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Ошибка при изменении статуса')
    }

    const updatedItem = await response.json()
    
    // Обновляем элемент в списке
    const index = tableData.value.findIndex(t => t.id === item.id)
    if (index !== -1) {
      tableData.value[index] = updatedItem
    }
    
    successMessage.value = `Статус стенда изменен на ${updatedItem.active ? 'активный' : 'неактивный'}`
    showSuccessDialog.value = true
  } catch (error) {
    console.error('Error toggling test tool:', error)
    errorMessage.value = error.message || 'Ошибка при изменении статуса'
    showErrorDialog.value = true
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
  return `Вы уверены, что хотите удалить тестовый стенд "${itemToDelete.value?.serial_number || ''}"?`
})

const deleteItem = async () => {
  if (!itemToDelete.value) return

  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }

  try {
    const response = await fetch(`${API_BASE_URL}/test-tools/${itemToDelete.value.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Ошибка при удалении тестового стенда')
    }

    // Обновляем список
    await loadTestTools()
    successMessage.value = 'Тестовый стенд успешно удален'
    showSuccessDialog.value = true
  } catch (error) {
    console.error('Error deleting test tool:', error)
    errorMessage.value = error.message || 'Ошибка при удалении тестового стенда'
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
  loadTestTools()
})
</script>