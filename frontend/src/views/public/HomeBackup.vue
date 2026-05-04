<template>
  <div class="min-h-screen bg-gray-50 font-sans flex flex-col">
    <nav class="bg-white border-b border-gray-100 shadow-sm sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center gap-2">
            <svg
              class="w-8 h-8 text-blue-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 10V3L4 14h7v7l9-11h-7z"
              ></path>
            </svg>
            <span class="text-2xl font-black text-gray-900 tracking-tight"
              >Abu<span class="text-blue-600">Motor</span></span
            >
          </div>

          <div class="flex items-center gap-6">
            <a
              href="#katalog"
              class="text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors hidden sm:block"
              >Katalog Motor</a
            >
            <a
              href="#kontak"
              class="text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors hidden sm:block"
              >Hubungi Kami</a
            >

            <router-link
              to="/login"
              class="text-sm font-medium text-blue-600 bg-blue-50 px-4 py-2 rounded-lg hover:bg-blue-100 transition-colors"
            >
              Masuk Admin
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <header class="bg-gradient-to-br from-gray-900 to-blue-900 text-white">
      <div
        class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-32 flex flex-col items-center text-center"
      >
        <span
          class="text-blue-400 font-semibold tracking-wider uppercase text-sm mb-4"
          >Dealer Motor Terpercaya</span
        >
        <h1
          class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight mb-6 leading-tight"
        >
          Temukan Motor Impian<br />
          <span
            class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400"
            >Harga Terbaik & Proses Cepat</span
          >
        </h1>
        <p class="text-lg sm:text-xl text-gray-300 max-w-2xl mb-10">
          Koleksi motor terbaru dengan berbagai pilihan tipe dan warna. Melayani
          pembelian tunai maupun kredit dengan DP ringan.
        </p>
        <div class="flex flex-col sm:flex-row gap-4">
          <a
            href="#katalog"
            class="px-8 py-3.5 text-base font-medium bg-blue-600 hover:bg-blue-700 text-white rounded-full transition-all shadow-lg shadow-blue-600/30"
          >
            Lihat Katalog Stok
          </a>
          <a
            :href="waLinkGeneral"
            target="_blank"
            class="px-8 py-3.5 text-base font-medium bg-white/10 hover:bg-white/20 text-white border border-white/20 rounded-full transition-all backdrop-blur-sm flex items-center justify-center gap-2"
          >
            <svg
              class="w-5 h-5 text-green-400"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 00-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .1 5.392.1 11.947c0 2.096.546 4.142 1.584 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.945-5.393 11.945-11.95a11.813 11.813 0 00-3.53-8.406z"
              />
            </svg>
            Konsultasi WhatsApp
          </a>
        </div>
      </div>
    </header>

    <main
      id="katalog"
      class="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 w-full"
    >
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-gray-900">Katalog Motor</h2>
        <p class="text-gray-500 mt-2">
          Pilih motor idamanmu dari daftar stok yang tersedia.
        </p>
      </div>

      <div v-if="isLoading" class="flex justify-center py-12">
        <div class="animate-pulse flex flex-col items-center">
          <div class="h-10 w-10 bg-blue-200 rounded-full mb-4"></div>
          <p class="text-gray-500">Memuat katalog...</p>
        </div>
      </div>

      <div
        v-else-if="activeMotors.length > 0"
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8"
      >
        <div
          v-for="motor in activeMotors"
          :key="motor.id"
          class="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow duration-300 flex flex-col group"
        >
          <div
            class="h-48 bg-gray-100 relative flex items-center justify-center border-b border-gray-100 overflow-hidden"
          >
            <img
              v-if="motor.image_url"
              :src="`http://127.0.0.1:5001${motor.image_url}`"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              :alt="motor.model_name"
            />

            <div
              v-else
              class="absolute inset-0 flex items-center justify-center"
            >
              <div
                class="absolute inset-0 opacity-10"
                style="
                  background-image: radial-gradient(
                    #2563eb 1px,
                    transparent 1px
                  );
                  background-size: 16px 16px;
                "
              ></div>
              <svg
                class="w-20 h-20 text-gray-300 group-hover:scale-110 transition-transform duration-500 relative z-0"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                ></path>
              </svg>
            </div>

            <span
              class="absolute top-3 right-3 bg-white/90 backdrop-blur px-2.5 py-1 rounded-md text-xs font-bold text-gray-700 uppercase tracking-wide z-10 shadow-sm"
            >
              {{ motor.brand }}
            </span>
          </div>
          <div class="p-5 flex-1 flex flex-col">
            <h3
              class="text-lg font-bold text-gray-900 mb-1 leading-tight line-clamp-1"
              :title="motor.model_name"
            >
              {{ motor.model_name }}
            </h3>
            <p class="text-sm text-gray-500 mb-4">{{ motor.color }}</p>

            <div class="mt-auto">
              <p
                class="text-xs text-gray-400 font-medium uppercase tracking-wider mb-1"
              >
                Harga OTR
              </p>
              <p class="text-xl font-black text-blue-600">
                {{ formatCurrency(motor.price) }}
              </p>
            </div>
          </div>

          <div class="px-5 pb-5 pt-2">
            <a
              :href="getWaLink(motor)"
              target="_blank"
              class="w-full flex items-center justify-center gap-2 bg-gray-900 hover:bg-gray-800 text-white py-2.5 rounded-xl text-sm font-semibold transition-colors"
            >
              Tanya ke CS
            </a>
          </div>
        </div>
      </div>

      <div
        v-else
        class="text-center py-20 bg-white rounded-3xl border border-gray-200"
      >
        <svg
          class="mx-auto h-16 w-16 text-gray-300 mb-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
          ></path>
        </svg>
        <h3 class="text-lg font-medium text-gray-900">Belum Ada Stok Motor</h3>
        <p class="text-gray-500 mt-1">
          Silakan kunjungi kami kembali beberapa saat lagi.
        </p>
      </div>
    </main>

    <footer id="kontak" class="bg-gray-900 text-gray-400 py-12 mt-auto">
      <div
        class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-3 gap-8"
      >
        <div>
          <div class="flex items-center gap-2 mb-4">
            <svg
              class="w-6 h-6 text-blue-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 10V3L4 14h7v7l9-11h-7z"
              ></path>
            </svg>
            <span class="text-xl font-bold text-white tracking-tight"
              >AbuMotor</span
            >
          </div>
          <p class="text-sm leading-relaxed mb-4">
            Pusat penjualan motor baru dengan layanan purna jual terbaik dan
            proses kredit paling transparan.
          </p>
        </div>

        <div>
          <h4 class="text-white font-semibold mb-4">Kontak Kami</h4>
          <ul class="space-y-2 text-sm">
            <li>📍 Jl. Raya Motor No. 99, Kota Baru</li>
            <li>📞 0812-3456-7890 (WhatsApp)</li>
            <li>✉️ cs@abumotor.com</li>
          </ul>
        </div>

        <div>
          <h4 class="text-white font-semibold mb-4">Jam Operasional</h4>
          <ul class="space-y-2 text-sm">
            <li>Senin - Jumat: 08.00 - 17.00</li>
            <li>Sabtu: 08.00 - 15.00</li>
            <li>Minggu & Libur Nasional: Tutup</li>
          </ul>
        </div>
      </div>
      <div
        class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-12 pt-8 border-t border-gray-800 text-sm text-center"
      >
        &copy; {{ new Date().getFullYear() }} Abu Motor Dealer. All rights
        reserved.
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";

// Nomor WA CS Dealer (Ganti dengan nomor aslimu. Format: 628...)
const DEALER_WA_NUMBER = "6281234567890";

const isLoading = ref(true);
const motors = ref([]);

// URL API Backend (Jangan pakai instance interceptor yang kita buat,
// karena halaman ini tidak butuh token. Kita panggil axios mentah saja)
const API_URL = "http://127.0.0.1:5001/api/inventory/";

// Hanya tampilkan motor yang is_active = true dan stoknya ada
const activeMotors = computed(() => {
  return motors.value.filter((m) => m.is_active === true && m.stock > 0);
});

// Format Harga
const formatCurrency = (value) => {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    minimumFractionDigits: 0,
  }).format(value || 0);
};

// WA Link Khusus Tombol Bawah (Umum)
const waLinkGeneral = computed(() => {
  const text = encodeURIComponent(
    "Halo Abu Motor, saya ingin konsultasi mengenai pembelian motor.",
  );
  return `https://wa.me/${DEALER_WA_NUMBER}?text=${text}`;
});

// WA Link Khusus Tiap Motor
const getWaLink = (motor) => {
  const text = encodeURIComponent(
    `Halo CS Abu Motor, saya tertarik dengan motor *${motor.brand} ${motor.model_name}* warna ${motor.color} (Harga: ${formatCurrency(motor.price)}). Apakah stoknya masih tersedia?`,
  );
  return `https://wa.me/${DEALER_WA_NUMBER}?text=${text}`;
};

// Ambil Data
const fetchKatalog = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get(API_URL);
    motors.value = response.data.data;
  } catch (error) {
    console.error("Gagal mengambil data katalog:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchKatalog();
});
</script>

<style>
/* Memuluskan animasi scroll ketika klik link navbar */
html {
  scroll-behavior: smooth;
}
</style>
