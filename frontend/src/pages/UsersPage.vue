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
      </div>
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
    <div style="overflow-x: auto; border: 1px solid #e0e0e0; border-radius: 8px;">
      <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
        <thead>
          <tr style="background-color: #f5f5f5; border-bottom: 2px solid #e0e0e0;">
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
                backgroundColor: item.role === 'Администратор' ? '#e3f2fd' : '#f5f5f5',
                color: item.role === 'Администратор' ? '#1976d2' : '#666'
              }">
                {{ item.role }}
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
            <td colspan="6" style="padding: 40px; text-align: center; color: #999;">
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
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Логин</label>
          <input v-model="modalForm.login" type="text" style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;" placeholder="Введите логин">
        </div>

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
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Пароль</label>
          <input 
            v-model="modalForm.password" 
            type="password" 
            style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;" 
            :placeholder="editingId ? 'Оставьте пустым, чтобы не менять' : 'Введите пароль'"
          >
        </div>

        <div style="margin-bottom: 20px;">
          <label style="display: block; margin-bottom: 5px; font-size: 14px; color: #333;">Роль</label>
          <select v-model="modalForm.role" style="width: 100%; padding: 10px; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px;">
            <option value="Метролог">Метролог</option>
            <option value="Администратор">Администратор</option>
          </select>
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

// ID текущего пользователя (чтобы нельзя было удалить самого себя)
const currentUserId = ref(1)

// Состояние для поиска и фильтров
const searchQuery = ref('')
const showFilters = ref(false)
const filters = ref({
  role: 'all'
})

// Данные пользователей
const tableData = ref([
  { 
    id: 1, 
    login: 'admin', 
    surname: 'Иванов', 
    name: 'Иван', 
    patronymic: 'Иванович', 
    role: 'Администратор',
    password: 'hashed_password_1'
  },
  { 
    id: 2, 
    login: 'petrov_p', 
    surname: 'Петров', 
    name: 'Петр', 
    patronymic: 'Петрович', 
    role: 'Метролог',
    password: 'hashed_password_2'
  },
  { 
    id: 3, 
    login: 'sidorova_a', 
    surname: 'Сидорова', 
    name: 'Анна', 
    patronymic: 'Алексеевна', 
    role: 'Метролог',
    password: 'hashed_password_3'
  },
  { 
    id: 4, 
    login: 'smirnov_d', 
    surname: 'Смирнов', 
    name: 'Дмитрий', 
    patronymic: 'Николаевич', 
    role: 'Администратор',
    password: 'hashed_password_4'
  },
  { 
    id: 5, 
    login: 'kuznetsova_e', 
    surname: 'Кузнецова', 
    name: 'Елена', 
    patronymic: 'Сергеевна', 
    role: 'Метролог',
    password: 'hashed_password_5'
  }
])

// Фильтрация данных
const filteredData = computed(() => {
  return tableData.value.filter(item => {
    // Поиск по тексту
    const query = searchQuery.value.toLowerCase()
    const matchesSearch = query === '' || 
      item.login.toLowerCase().includes(query) ||
      item.surname.toLowerCase().includes(query) || 
      item.name.toLowerCase().includes(query) ||
      (item.patronymic && item.patronymic.toLowerCase().includes(query)) ||
      item.role.toLowerCase().includes(query)
    
    // Фильтр по роли
    const matchesRole = filters.value.role === 'all' || item.role === filters.value.role
    
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
  role: 'Метролог',
  password: ''
})

const openAddModal = () => {
  modalTitle.value = 'Добавить пользователя'
  editingId.value = null
  modalForm.value = {
    login: '',
    surname: '',
    name: '',
    patronymic: '',
    role: 'Метролог',
    password: ''
  }
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
    role: item.role,
    password: '' // Пароль не показываем при редактировании
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const saveItem = () => {
  // Валидация
  if (!modalForm.value.login || !modalForm.value.surname || !modalForm.value.name || !modalForm.value.role) {
    alert('Заполните все обязательные поля')
    return
  }

  if (!editingId.value && !modalForm.value.password) {
    alert('Введите пароль для нового пользователя')
    return
  }

  if (editingId.value) {
    // Редактирование
    const index = tableData.value.findIndex(item => item.id === editingId.value)
    if (index !== -1) {
      const updatedUser = {
        id: editingId.value,
        login: modalForm.value.login,
        surname: modalForm.value.surname,
        name: modalForm.value.name,
        patronymic: modalForm.value.patronymic || null,
        role: modalForm.value.role,
        password: modalForm.value.password || tableData.value[index].password // Если пароль не меняли, оставляем старый
      }
      tableData.value[index] = updatedUser
    }
  } else {
    // Добавление
    const newId = Math.max(...tableData.value.map(item => item.id)) + 1
    tableData.value.push({
      id: newId,
      login: modalForm.value.login,
      surname: modalForm.value.surname,
      name: modalForm.value.name,
      patronymic: modalForm.value.patronymic || null,
      role: modalForm.value.role,
      password: `hashed_${modalForm.value.password}` // В реальности здесь должно быть хеширование
    })
  }
  closeModal()
}

// Диалог удаления
const showDeleteDialog = ref(false)
const itemToDelete = ref(null)

const confirmDelete = (item) => {
  itemToDelete.value = item
  showDeleteDialog.value = true
}

const deleteMessage = computed(() => {
  return `Вы уверены, что хотите удалить пользователя "${itemToDelete.value?.login}" (${itemToDelete.value?.surname} ${itemToDelete.value?.name})?`
})

const deleteItem = () => {
  if (itemToDelete.value) {
    tableData.value = tableData.value.filter(item => item.id !== itemToDelete.value.id)
    itemToDelete.value = null
  }
}
</script>