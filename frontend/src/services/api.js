import axios from "axios";

// ==========================================
// 1. DEFINISI & EKSPOR BASE URL (KHUSUS UNTUK FOTO/ASSET)
// ==========================================
export const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5001";

// ==========================================
// 2. KONFIGURASI INSTANCE AXIOS (KHUSUS UNTUK REQUEST DATA API)
// ==========================================
const api = axios.create({
  baseURL: BASE_URL + "/api", // Menggunakan BASE_URL di atas ditambah "/api"
  headers: {
    "Content-Type": "application/json",
  },
});

// ==========================================
// 3. REQUEST INTERCEPTOR (MENYISIPKAN TOKEN)
// ==========================================
api.interceptors.request.use(
  (config) => {
    // Ambil token dari local storage
    const token = localStorage.getItem("access_token");

    // Jika token ada, sisipkan ke header Authorization
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// ==========================================
// 4. RESPONSE INTERCEPTOR (MENANGANI ERROR 401)
// ==========================================
api.interceptors.response.use(
  (response) => {
    // Jika response sukses, langsung kembalikan datanya
    return response;
  },
  (error) => {
    // Jika error 401 (Unauthorized / Token Kedaluwarsa)
    if (error.response && error.response.status === 401) {
      console.warn("Sesi kedaluwarsa, silakan login kembali.");

      // Bersihkan data lokal
      localStorage.removeItem("access_token");
      localStorage.removeItem("user_data");

      // Lempar paksa ke halaman login
      // Kita gunakan window.location agar tidak terjadi circular dependency dengan Vue Router
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  },
);

export default api;
