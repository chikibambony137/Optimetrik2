<template>
  <div v-if="show" class="dialog-overlay" @click.self="closeOnOverlay ? close() : null">
    <div class="dialog-container">
      <!-- Заголовок -->
      <div class="dialog-header">
        <h3>{{ title }}</h3>
        <button v-if="showClose" class="close-btn" @click="close">✕</button>
      </div>
      
      <!-- Описание/контент -->
      <div class="dialog-content">
        <p>{{ message }}</p>
        <!-- Слот для дополнительного контента -->
        <slot></slot>
      </div>
      
      <!-- Кнопки действий -->
      <div class="dialog-actions">
        <button 
          class="btn-primary" 
          @click="handleConfirm"
        >
          {{ confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

// Определяем пропсы
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Уведомление'
  },
  message: {
    type: String,
    default: ''
  },
  confirmText: {
    type: String,
    default: 'ОК'
  },
  showClose: {
    type: Boolean,
    default: true
  },
  closeOnOverlay: {
    type: Boolean,
    default: true
  }
})

// Определяем события
const emit = defineEmits(['update:show', 'confirm'])

// Закрытие диалога
const close = () => {
  emit('update:show', false)
}

// Обработка подтверждения
const handleConfirm = () => {
  emit('confirm')
  close()
}
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog-container {
  background-color: white;
  border-radius: 12px;
  min-width: 300px;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.dialog-header {
  padding: 16px 20px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #666;
  padding: 0 5px;
}

.close-btn:hover {
  color: #333;
}

.dialog-content {
  padding: 20px;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.dialog-content p {
  margin: 0;
}

.dialog-actions {
  padding: 16px 20px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  justify-content: flex-end;
}

.btn-primary {
  background-color: black;
  color: white;
  border: none;
  padding: 8px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.btn-primary:hover {
  background-color: #333;
}
</style>