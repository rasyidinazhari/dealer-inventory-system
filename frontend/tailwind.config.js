/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Kita bisa tambahkan warna kustom dealer di sini nanti
      colors: {
        primary: '#2563eb', // Contoh warna biru modern
        secondary: '#475569',
      }
    },
  },
  plugins: [],
}