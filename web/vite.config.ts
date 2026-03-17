import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Daily Briefing 前端：纯静态展示列表和详情
export default defineConfig({
  plugins: [react()],
  root: '.',
  build: {
    outDir: 'dist'
  }
})

