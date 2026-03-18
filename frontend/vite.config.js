import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: '127.0.0.1',  // или '0.0.0.0' для всех интерфейсов
    port: 5173,
    strictPort: true,    // если порт занят - ошибка, а не другой порт
  }
})