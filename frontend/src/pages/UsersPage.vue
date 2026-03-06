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
            placeholder="Поиск по логину, фамилии, имени, роли..."
            style="padding: 8px 12px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px; width: 400px;"
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
          @click="openAddModal"
          style="background-color: black; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 14px; display: flex; align-items: center; gap: 5px;"
        >
          <span style="font-size: 18px;">+</span> Добавить
        </button>

        <!-- Кнопка обновления данных -->
        <button 
          @click="loadUsers"
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
        
        <!-- Фильтр по роли -->
        <div>
          <label style="display: block; margin-bottom: 5px; font-size: 12px; color: #666;">Роль</label>
          <select v-model="filters.role" style="width: 100%; padding: 8px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
            <option value="all">Все роли</option>
            <option value="Администратор">Администратор</option>
            <option value="Метролог">Метролог</option>
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

    <!-- Таблица пользователей -->
    <div v-if="!loading" style="overflow-x: auto; border: 1px solid #e0e0e0; border-radius: 8px;">
      <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
        <thead>
          <tr style="background-color: #f5f5f5; border-bottom: 2px solid #e0e0e0;">
            <th style="padding: 12px 15px; text-align: left;">ID</th>
            <th style="padding: 12px 15px; text-align: left;">Логин</th>
            <th style="padding: 12px 15px; text-align: left;">Фамилия</th>
            <th style="padding: 12px 15px; text-align: left;">Имя</th>
            <th style="padding: 12px 15px; text-align: left;">Отчество</th>
            <th style="padding: 12px 15px; text-align: left;">Роль</th>
            <th style="padding: 12px 15px; text-align: center;">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredData" :key="item.id" style="border-bottom: 1px solid #e0e0e0;">
            <td style="padding: 12px 15px;">{{ item.id }}</td>
            <td style="padding: 12px 15px;">{{ item.login }}</td>
            <td style="padding: 12px 15px;">{{ item.surname }}</td>
            <td style="padding: 12px 15px;">{{ item.name }}</td>
            <td style="padding: 12px 15px;">{{ item.patronymic || '—' }}</td>
            <td style="padding: 12px 15px;">
              <span :style="{ 
                padding: '4px 8px', 
                borderRadius: '4px', 
                fontSize: '12px',
                fontWeight: '500',
                backgroundColor: item.admin_role ? '#e3f2fd' : '#f5f5f5',
                color: item.admin_role ? '#1976d2' : '#666'
              }">
                {{ item.admin_role ? 'Администратор' : 'Метролог' }}
              </span>
            </td>
            
            <!-- Кнопки действий -->
            <td style="padding: 12px 15px; text-align: center;">
              <div style="display: flex; gap: 8px; justify-content: center;">
                <button 
                  @click="openEditModal(item)" 
                  style="background: none; border: 1px solid #e0e0e0; border-radius: 4px; padding: 4px 8px; cursor: pointer;"
                  title="Редактировать"
                >
                  ✏️ Ред.
                </button>
                <button 
                  v-if="item.id !== currentUserId"
                  @click="confirmDelete(item)" 
                  style="background: none; border: 1px solid #ffcdd2; border-radius: 4px; padding: 4px 8px; cursor: pointer; color: #d32f2f;"
                  title="Удалить"
                >
                  🗑️ Удал.
                </button>
                <span v-else style="color: #999; font-size: 12px;">(текущий)</span>
              </div>
            </td>
          </tr>
          <tr v-if="filteredData.length === 0">
            <td colspan="7" style="padding: 40px; text-align: center; color: #999;">
              Нет данных, соответствующих критериям поиска
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модальное окно для добавления/редактирования пользователя -->
    <div v-if="showModal" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000;" @click.self="closeModal">
      <div style="background-color: white; border-radius: 12px; padding: 25px; width: 500px; max-width: 90%; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
        <h3 style="margin-top: 0; margin-bottom: 20px; font-size: 18px;">{{ modalTitle }}</h3>

        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Фамилия</label>
          <input v-model="modalForm.surname" type="text" style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;" placeholder="Введите фамилию">
        </div>

        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Имя</label>
          <input v-model="modalForm.name" type="text" style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;" placeholder="Введите имя">
        </div>

        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Отчество</label>
          <input v-model="modalForm.patronymic" type="text" style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;" placeholder="Введите отчество (необязательно)">
        </div>

        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Логин</label>
          <input v-model="modalForm.login" type="text" style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;" placeholder="Введите логин">
        </div>

        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Пароль</label>
          <input 
            v-model="modalForm.password" 
            :type="showPassword ? 'text' : 'password'"
            style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;" 
            :placeholder="editingId ? 'Оставьте пустым, чтобы не менять' : 'Введите пароль'"
          >
          <div style="display: flex; justify-content: flex-end; margin-top: 5px;">
            <button 
              type="button"
              @click="showPassword = !showPassword"
              style="background: none; border: none; color: #666; cursor: pointer; font-size: 12px;"
            >
              {{ showPassword ? 'Скрыть' : 'Показать' }}
            </button>
          </div>
        </div>

        <div style="margin-bottom: 20px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Роль</label>
          <select v-model="modalForm.admin_role" style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
            <option :value="false">Метролог</option>
            <option :value="true">Администратор</option>
          </select>
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 10px;">
          <button @click="closeModal" style="padding: 10px 20px; background-color: white; border: 1px solid #e0e0e0; border-radius: 6px; cursor: pointer; font-size: 14px;">Отмена</button>
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

// ID текущего пользователя (получаем из localStorage)
const currentUserId = ref(null)

// Состояние загрузки
const loading = ref(false)
const saving = ref(false)

// Состояние для поиска и фильтров
const searchQuery = ref('')
const showFilters = ref(false)
const filters = ref({
  role: 'all'
})

// Диалоги
const showErrorDialog = ref(false)
const showSuccessDialog = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Показ пароля в модальном окне
const showPassword = ref(false)

// Данные пользователей
const tableData = ref([])

// Загрузка списка пользователей с бэкенда
const loadUsers = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }

  loading.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/users/`, {
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
      throw new Error('Ошибка загрузки пользователей')
    }

    const data = await response.json()
    tableData.value = data
    console.log('Загружены пользователи:', data)
  } catch (error) {
    console.error('Error loading users:', error)
    errorMessage.value = error.message || 'Ошибка загрузки пользователей'
    showErrorDialog.value = true
  } finally {
    loading.value = false
  }
}

// Получение ID текущего пользователя
const loadCurrentUserId = () => {
  try {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      const user = JSON.parse(storedUser)
      currentUserId.value = user.id
    }
  } catch (error) {
    console.error('Error loading current user:', error)
  }
}

// Фильтрация данных
const filteredData = computed(() => {
  return tableData.value.filter(item => {
    // Поиск по тексту
    const query = searchQuery.value.toLowerCase()
    const role = item.admin_role ? 'Администратор' : 'Метролог'
    
    const matchesSearch = query === '' || 
      item.login?.toLowerCase().includes(query) ||
      item.surname?.toLowerCase().includes(query) || 
      item.name?.toLowerCase().includes(query) ||
      (item.patronymic && item.patronymic.toLowerCase().includes(query)) ||
      role.toLowerCase().includes(query)
    
    // Фильтр по роли
    const matchesRole = filters.value.role === 'all' || 
      (filters.value.role === 'Администратор' && item.admin_role) ||
      (filters.value.role === 'Метролог' && !item.admin_role)
    
    return matchesSearch && matchesRole
  })
})

// Применить фильтры
const applyFilters = () => {
  showFilters.value = false
}

// Сбросить фильтры
const resetFilters = () => {
  filters.value = {
    role: 'all'
  }
}

// Модальное окно
const showModal = ref(false)
const modalTitle = ref('Добавить пользователя')
const editingId = ref(null)
const modalForm = ref({
  login: '',
  surname: '',
  name: '',
  patronymic: '',
  admin_role: false,
  password: ''
})

const openAddModal = () => {
  modalTitle.value = 'Добавить пользователя'
  editingId.value = null
  modalForm.value = {
    surname: '',
    name: '',
    patronymic: '',
    login: '',
    password: '',
    admin_role: false
  }
  showPassword.value = false
  showModal.value = true
}

const openEditModal = (item) => {
  modalTitle.value = 'Редактировать пользователя'
  editingId.value = item.id
  modalForm.value = { 
    login: item.login,
    surname: item.surname,
    name: item.name,
    patronymic: item.patronymic || '',
    admin_role: item.admin_role,
    password: '' // Пароль не показываем при редактировании
  }
  showPassword.value = false
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  showPassword.value = false
}

const saveItem = async () => {
  // Валидация
  if (!modalForm.value.login || !modalForm.value.surname || !modalForm.value.name) {
    errorMessage.value = 'Заполните все обязательные поля'
    showErrorDialog.value = true
    return
  }

  if (!editingId.value && !modalForm.value.password) {
    errorMessage.value = 'Введите пароль для нового пользователя'
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
    // Подготавливаем данные для отправки - исключаем пустые поля
    const dataToSend = {
      login: modalForm.value.login,
      surname: modalForm.value.surname,
      name: modalForm.value.name,
      patronymic: modalForm.value.patronymic || null,
      admin_role: modalForm.value.admin_role
    }
    
    // Добавляем пароль только если он не пустой
    if (modalForm.value.password && modalForm.value.password.trim() !== '') {
      dataToSend.password = modalForm.value.password
    }
    
    console.log('Отправляемые данные:', dataToSend) // Для отладки

    if (editingId.value) {
      // Редактирование
      const response = await fetch(`${API_BASE_URL}/users/${editingId.value}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
      })

      if (!response.ok) {
        const error = await response.json()
        console.error('Ошибка ответа:', error)
        throw new Error(error.detail || 'Ошибка при обновлении пользователя')
      }

      successMessage.value = 'Пользователь успешно обновлен'
    } else {
      // Добавление
      const response = await fetch(`${API_BASE_URL}/users/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Ошибка при создании пользователя')
      }

      successMessage.value = 'Пользователь успешно создан'
    }
    
    // Обновляем список пользователей
    await loadUsers()
    showSuccessDialog.value = true
    closeModal()
  } catch (error) {
    console.error('Error saving user:', error)
    errorMessage.value = error.message || 'Ошибка при сохранении пользователя'
    showErrorDialog.value = true
  } finally {
    saving.value = false
  }
}
// Диалог удаления
const showDeleteDialog = ref(false)
const itemToDelete = ref(null)

const confirmDelete = (item) => {
  itemToDelete.value = item
  showDeleteDialog.value = true
}

const deleteMessage = computed(() => {
  if (!itemToDelete.value) return ''
  const role = itemToDelete.value.admin_role ? 'Администратор' : 'Метролог'
  return `Вы уверены, что хотите удалить пользователя "${itemToDelete.value.login}" (${itemToDelete.value.surname} ${itemToDelete.value.name}, ${role})?`
})

const deleteItem = async () => {
  if (!itemToDelete.value) return

  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }

  try {
    const response = await fetch(`${API_BASE_URL}/users/${itemToDelete.value.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Ошибка при удалении пользователя')
    }

    // Обновляем список пользователей
    await loadUsers()
    successMessage.value = 'Пользователь успешно удален'
    showSuccessDialog.value = true
  } catch (error) {
    console.error('Error deleting user:', error)
    errorMessage.value = error.message || 'Ошибка при удалении пользователя'
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
  loadCurrentUserId()
  loadUsers()
})
</script>