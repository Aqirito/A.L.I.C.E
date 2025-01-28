import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
  optimizeDeps: {
    exclude: ['babylon-mmd', '@babylonjs/havok']
  },
  build: {
    rollupOptions: {
      external: ['babylon-mmd']
    }
  }
});
