import path from "node:path";
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  plugins: [react()],
  define: {
    'import.meta.env.VITE_FIREBASE_API_KEY': JSON.stringify('test-api-key'),
    'import.meta.env.VITE_FIREBASE_AUTH_DOMAIN': JSON.stringify('test.firebaseapp.com'),
    'import.meta.env.VITE_FIREBASE_DATABASE_URL': JSON.stringify('https://test-default-rtdb.firebaseio.com'),
    'import.meta.env.VITE_FIREBASE_PROJECT_ID': JSON.stringify('test-project'),
    'import.meta.env.VITE_FIREBASE_STORAGE_BUCKET': JSON.stringify('test-project.appspot.com'),
    'import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID': JSON.stringify('test-sender'),
    'import.meta.env.VITE_FIREBASE_APP_ID': JSON.stringify('test-app-id'),
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
    include: ["src/**/*.{test,spec}.{ts,tsx}"],
    reporters: ["default"],
  },
});
