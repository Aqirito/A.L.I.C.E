import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
	plugins: [sveltekit()],
  optimizeDeps: {
    include: ['babylon-mmd'],
    exclude: ['@babylonjs/havok']
  },
  build: {
    rollupOptions: {
      external: ['babylon-mmd']
    }
  },
  resolve: {
    alias: {
      'babylon-mmd': path.resolve(__dirname, './node_modules/babylon-mmd')
    }
  },
  server: {
    allowedHosts: ['alice.aqirito.online']
  }
});
