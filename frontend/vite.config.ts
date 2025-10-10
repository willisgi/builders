import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const port = Number(process.env.PORT || 5173)
const isCodespaces = !!process.env.CODESPACE_NAME && !!process.env.GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN
const hmrHost = isCodespaces
  ? `${process.env.CODESPACE_NAME}-${port}.${process.env.GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}`
  : 'localhost'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port,
    strictPort: true,
    hmr: {
      host: hmrHost,
      protocol: isCodespaces ? 'wss' : 'ws',
      clientPort: isCodespaces ? 443 : port,
    },
  },
})
