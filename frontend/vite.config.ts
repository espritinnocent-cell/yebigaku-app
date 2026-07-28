import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: 'autoUpdate', // 更新があったら自動でアップデート
      devOptions: {
        enabled: true // 開発サーバー（localhost）でもPWAのテストを有効にする
      },
      manifest: {
        name: '耳学 (Yebigaku)',
        short_name: '耳学',
        description: '法律の条文をAIの要約と音声で学ぶアプリ',
        theme_color: '#1d4ed8', // ヘッダーの色（blue-700）に合わせる
        background_color: '#f1f5f9', // 背景色（slate-100）に合わせる
        display: 'standalone', // ブラウザのURLバーを消してアプリ風にする
        start_url: '/', // ← ★これを追加！
        icons: [
          {
            src: '/pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      }
    })
  ],
})