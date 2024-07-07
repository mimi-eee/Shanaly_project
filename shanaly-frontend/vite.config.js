import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { VitePWA } from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig({
  	plugins: [
		svelte(),

		VitePWA({
			registerType: 'autoUpdate',
			devOptions: {
				enabled: true
			},
			manifest: {
				name: 'シャナリ',
				short_name: 'Shanaly',
				description: 'シャナリ(Shanaly) SNS for Investors 投資特化型SNS',
				theme_color: '#000000',
				icons: [
					{
					  "src": "pwa-64x64.png",
					  "sizes": "64x64",
					  "type": "image/png"
					},
					{
					  "src": "pwa-192x192.png",
					  "sizes": "192x192",
					  "type": "image/png"
					},
					{
					  "src": "pwa-512x512.png",
					  "sizes": "512x512",
					  "type": "image/png"
					},
					{
					  "src": "maskable-icon-512x512.png",
					  "sizes": "512x512",
					  "type": "image/png",
					  "purpose": "maskable"
					}
				  ]
			}
		}),

	],
})
