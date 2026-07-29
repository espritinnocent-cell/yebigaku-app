import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      // アプリの更新があった場合、自動的に新しいバージョンを読み込む
      registerType: 'autoUpdate',
      
      // インストール時に強制的にキャッシュする静的ファイル
      includeAssets: ['favicon.svg', 'icons.svg', 'laws.json'],
      
      manifest: {
        name: '耳学 (Yebigaku)',
        short_name: '耳学',
        description: 'スキマ時間で学ぶ法律音声アプリ',
        theme_color: '#1d4ed8',
        background_color: '#f1f5f9',
        display: 'standalone',
        icons: [
          {
            src: 'pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      },
      
      workbox: {
        // js, css, html, 画像, json をインストール時に全てプレキャッシュ
        globPatterns: ['**/*.{js,css,html,ico,png,svg,json}'],
        
        // 音声ファイルに対するオンデマンドキャッシュ（CacheFirst戦略）
        runtimeCaching: [
          {
            // /audio/ フォルダ内の mp3 ファイルを対象とする
            urlPattern: /^\/audio\/.*\.mp3$/i,
            handler: 'CacheFirst', // まずキャッシュを探し、無ければネットワークへ
            options: {
              cacheName: 'audio-cache',
              expiration: {
                maxEntries: 50, // 最大50件の音声のみ保存（スマホの容量圧迫防止）
                maxAgeSeconds: 60 * 60 * 24 * 30 // 30日間保持
              },
              cacheableResponse: {
                statuses: [0, 200]
              }
            }
          }
        ]
      }
    })
  ]
})