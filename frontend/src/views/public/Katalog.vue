<template>
  <div class="min-h-screen bg-gray-50 font-sans flex flex-col">
    <PublicNavbar />

    <div class="bg-blue-600 text-white py-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 class="text-3xl md:text-4xl font-extrabold mb-3">
          Katalog Kendaraan
        </h1>
        <p class="text-blue-100 max-w-2xl mx-auto text-sm md:text-base">
          Temukan berbagai pilihan mobil dan motor dengan harga dan penawaran
          terbaik di Abu Motor.
        </p>
      </div>
    </div>

    <main
      class="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full flex flex-col lg:flex-row gap-8"
    >
      <!-- SIDEBAR FILTER -->
      <aside class="w-full lg:w-1/4">
        <div
          class="p-4 bg-white border border-gray-200 shadow-sm sm:p-5 rounded-xl sm:rounded-2xl lg:sticky lg:top-24"
        >
          <div
            class="flex items-center justify-between mb-3 border-b border-gray-100 sm:mb-5 pb-2 sm:pb-3"
          >
            <h3
              class="flex items-center gap-2 text-sm font-bold text-gray-900 sm:text-base"
            >
              <svg
                class="w-4 h-4 text-blue-600 sm:w-5 sm:h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"
                ></path>
              </svg>
              Filter Pencarian
            </h3>
            <button
              v-if="hasActiveFilters"
              @click="resetFilters"
              class="text-[10px] sm:text-xs font-bold text-red-500 transition-colors hover:text-red-700"
            >
              Reset
            </button>
          </div>

          <!-- MENGGUNAKAN GRID 2 KOLOM DI MOBILE, 1 KOLOM DI DESKTOP -->
          <div class="grid grid-cols-2 gap-3 lg:grid-cols-1 sm:gap-5">
            <!-- Kata Kunci (Penuh 2 Kolom di HP) -->
            <div class="col-span-2 lg:col-span-1">
              <label
                class="block mb-1 text-[10px] sm:text-xs font-bold tracking-wider text-gray-500 uppercase sm:mb-2"
                >Kata Kunci</label
              >
              <div class="relative">
                <input
                  v-model="filters.q"
                  type="text"
                  placeholder="Cari model/merek..."
                  class="w-full py-2 pl-3 pr-8 text-xs font-medium bg-white border border-gray-300 sm:text-sm rounded-lg sm:rounded-xl focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                />
                <button
                  v-if="filters.q"
                  @click="filters.q = ''"
                  class="absolute text-gray-400 right-2 top-1/2 -translate-y-1/2 hover:text-red-500"
                >
                  <svg
                    class="w-3.5 h-3.5 sm:w-4 sm:h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M6 18L18 6M6 6l12 12"
                    ></path>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Tipe Kendaraan (Berbagi ruang di HP) -->
            <div class="col-span-1">
              <label
                class="block mb-1 text-[10px] sm:text-xs font-bold tracking-wider text-gray-500 uppercase sm:mb-2"
                >Tipe</label
              >
              <select
                v-model="filters.type"
                @change="adjustCategoryOptions"
                class="w-full px-2 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 cursor-pointer sm:px-3 sm:text-sm rounded-lg sm:rounded-xl focus:outline-none focus:border-blue-500"
              >
                <option value="">Semua</option>
                <option value="Motor">Motor</option>
                <option value="Mobil">Mobil</option>
              </select>
            </div>

            <!-- Kondisi (Berbagi ruang di HP) -->
            <div class="col-span-1">
              <label
                class="block mb-1 text-[10px] sm:text-xs font-bold tracking-wider text-gray-500 uppercase sm:mb-2"
                >Kondisi</label
              >
              <select
                v-model="filters.condition"
                class="w-full px-2 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 cursor-pointer sm:px-3 sm:text-sm rounded-lg sm:rounded-xl focus:outline-none focus:border-blue-500"
              >
                <option value="">Semua</option>
                <option value="Baru">Baru</option>
                <option value="Bekas">Bekas</option>
              </select>
            </div>

            <!-- Kategori (Penuh 2 Kolom di HP) -->
            <div class="col-span-2 lg:col-span-1">
              <label
                class="block mb-1 text-[10px] sm:text-xs font-bold tracking-wider text-gray-500 uppercase sm:mb-2"
                >Kategori</label
              >
              <select
                v-model="filters.category"
                class="w-full px-3 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 cursor-pointer sm:text-sm rounded-lg sm:rounded-xl focus:outline-none focus:border-blue-500"
              >
                <option value="">Semua Kategori</option>
                <option
                  v-for="cat in dynamicCategories"
                  :key="cat.id"
                  :value="cat.name"
                >
                  {{ cat.name }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </aside>

      <section class="w-full lg:w-3/4 flex flex-col">
        <div
          class="flex flex-col sm:flex-row justify-between items-center bg-white p-4 rounded-2xl shadow-sm border border-gray-200 mb-6 gap-4"
        >
          <p class="text-sm text-gray-600 font-medium">
            Menampilkan
            <span class="font-bold text-gray-900">{{
              sortedAndFilteredMotors.length
            }}</span>
            kendaraan
          </p>

          <div class="flex items-center gap-2 w-full sm:w-auto">
            <label class="text-sm font-bold text-gray-500 shrink-0"
              >Urutkan:</label
            >
            <select
              v-model="sortBy"
              class="w-full sm:w-48 px-3 py-2 border border-gray-300 rounded-xl text-sm font-medium text-gray-900 bg-gray-50 focus:outline-none focus:border-blue-500 focus:bg-white transition-colors"
            >
              <option value="newest">Terbaru</option>
              <option value="price_asc">Harga: Rendah ke Tinggi</option>
              <option value="price_desc">Harga: Tinggi ke Rendah</option>
            </select>
          </div>
        </div>

        <div v-if="isLoading" class="flex justify-center py-20 flex-1">
          <div class="animate-pulse flex flex-col items-center">
            <div
              class="h-12 w-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-4"
            ></div>
            <p class="text-gray-500 font-medium">Mencari kendaraan...</p>
          </div>
        </div>

        <div
          v-else-if="sortedAndFilteredMotors.length === 0"
          class="text-center py-24 bg-white rounded-3xl border border-dashed border-gray-300 flex-1 flex flex-col justify-center items-center"
        >
          <svg
            class="w-20 h-20 text-gray-300 mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            ></path>
          </svg>
          <h3 class="text-xl font-bold text-gray-900">
            Tidak ada kendaraan yang cocok
          </h3>
          <p class="text-gray-500 mt-2 max-w-md">
            Coba kurangi filter pencarian atau gunakan kata kunci lain untuk
            menemukan kendaraan yang Anda inginkan.
          </p>
          <button
            @click="resetFilters"
            class="mt-6 px-6 py-2.5 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition-colors shadow-md"
          >
            Reset Filter
          </button>
        </div>

        <!-- GRID KENDARAAN (Dibuat 2 Kolom untuk HP) -->
        <div
          v-else
          class="grid grid-cols-2 sm:grid-cols-2 xl:grid-cols-3 gap-3 sm:gap-6 auto-rows-max"
        >
          <!-- CARD KENDARAAN -->
          <div
            v-for="motor in sortedAndFilteredMotors"
            :key="motor.id"
            class="bg-white rounded-xl sm:rounded-2xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-xl transition-all duration-300 flex flex-col group relative"
          >
            <router-link
              :to="'/motor/' + motor.id"
              class="flex flex-col flex-1 outline-none"
            >
              <!-- FOTO (Lebih pendek di layar HP) -->
              <div
                class="relative flex items-center justify-center overflow-hidden border-b border-gray-100 h-32 sm:h-48 bg-gray-50"
              >
                <img
                  v-if="motor.image_url"
                  :src="getImageUrl(motor.image_url)"
                  class="object-cover w-full h-full transition-transform duration-700 group-hover:scale-105"
                  :alt="motor.model_name"
                />
                <div
                  v-else
                  class="absolute inset-0 flex items-center justify-center"
                >
                  <svg
                    class="w-10 h-10 text-gray-300 sm:w-16 sm:h-16"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="1.5"
                      d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
                    ></path>
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="1.5"
                      d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"
                    ></path>
                  </svg>
                </div>

                <!-- LABEL KONDISI & MEREK -->
                <div
                  class="absolute flex flex-col items-end gap-1 top-2 right-2 sm:top-3 sm:right-3"
                >
                  <span
                    class="bg-white/95 backdrop-blur-sm px-1.5 sm:px-2.5 py-0.5 sm:py-1 rounded sm:rounded-md text-[9px] sm:text-xs font-black text-gray-800 uppercase tracking-wide shadow-sm"
                  >
                    {{ motor.brand }}
                  </span>
                  <span
                    :class="
                      motor.vehicle_type === 'Mobil'
                        ? 'bg-indigo-600/95'
                        : 'bg-blue-600/95'
                    "
                    class="backdrop-blur-sm px-1.5 sm:px-2 py-0.5 sm:py-1 rounded sm:rounded-md text-[8px] sm:text-[10px] font-bold text-white uppercase tracking-wide shadow-sm"
                  >
                    {{ motor.condition }}
                  </span>
                </div>
              </div>

              <!-- INFO KENDARAAN (Padding disesuaikan untuk layar sempit) -->
              <div class="flex flex-col flex-1 p-3 sm:p-5">
                <h3
                  class="mb-1 text-sm font-bold leading-tight transition-colors sm:text-lg text-gray-900 line-clamp-2 group-hover:text-blue-600"
                  :title="motor.model_name"
                >
                  {{ motor.model_name }}
                </h3>

                <div
                  class="flex flex-wrap items-center gap-1 sm:gap-2 mb-3 sm:mb-4 text-[10px] sm:text-xs font-medium text-gray-500"
                >
                  <span>{{ motor.year }}</span>
                  <span class="hidden sm:inline">•</span>
                  <span class="sm:hidden">-</span>
                  <span>{{ motor.transmission }}</span>
                </div>

                <div class="pt-2 mt-auto border-t sm:pt-4 border-gray-100">
                  <p
                    class="text-[9px] sm:text-[11px] font-bold tracking-wider text-gray-400 uppercase mb-0.5 sm:mb-0.5"
                  >
                    Harga OTR
                  </p>
                  <p
                    class="text-sm font-black text-blue-600 sm:text-xl truncate"
                    :title="formatCurrency(motor.price)"
                  >
                    {{ formatCurrency(motor.price) }}
                  </p>
                </div>
              </div>
            </router-link>

            <!-- TOMBOL WA (Pengecilan ukuran di layar HP) -->
            <div class="px-3 pb-3 sm:px-5 sm:pb-5 pt-0">
              <a
                :href="getWaLink(motor)"
                target="_blank"
                class="relative z-10 flex items-center justify-center w-full gap-1.5 sm:gap-2 py-2 sm:py-2.5 text-xs sm:text-sm font-semibold text-white transition-colors bg-gray-900 shadow-sm rounded-lg sm:rounded-xl hover:bg-gray-800"
              >
                <svg
                  class="w-3.5 h-3.5 sm:w-4 sm:h-4 shrink-0"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 00-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347"
                  />
                </svg>
                <span class="truncate">Tanya CS</span>
              </a>
            </div>
          </div>
        </div>
      </section>
    </main>

    <PublicFooter />
  </div>
</template>

<script setup>
import { BASE_URL } from "../../services/api";
import { ref, onMounted, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import PublicNavbar from "../../components/PublicNavbar.vue";
import PublicFooter from "../../components/PublicFooter.vue";

const route = useRoute();
const router = useRouter();

const DEALER_WA_NUMBER = "6281222444951";
const isLoading = ref(true);
const motors = ref([]);

// OPSI KATEGORI DINAMIS
// const motorCategories = ["Matic", "Sport", "Bebek", "EV", "Lainnya"];
// const mobilCategories = [
//   "SUV",
//   "MPV",
//   "Sedan",
//   "Hatchback",
//   "Pickup",
//   "Lainnya",
// ];
// const dynamicCategories = ref([...motorCategories, ...mobilCategories]);

// STATE FILTER & SORTING
const filters = ref({
  q: "",
  type: "",
  condition: "",
  category: "",
});
const sortBy = ref("newest");

const hasActiveFilters = computed(() => {
  return (
    filters.value.q !== "" ||
    filters.value.type !== "" ||
    filters.value.condition !== "" ||
    filters.value.category !== ""
  );
});

const adjustCategoryOptions = () => {
  // if (filters.value.type === "Mobil") {
  //   dynamicCategories.value = mobilCategories;
  // } else if (filters.value.type === "Motor") {
  //   dynamicCategories.value = motorCategories;
  // } else {
  //   dynamicCategories.value = [
  //     ...new Set([...motorCategories, ...mobilCategories]),
  //   ];
  // }
  // filters.value.category = ""; // Reset kategori saat tipe berubah
};

// COMPUTED UNTUK FILTER & SORTING AKTIF (Berjalan otomatis di Frontend)
const sortedAndFilteredMotors = computed(() => {
  // 1. Ambil yang aktif dan ber-stok
  let result = motors.value.filter((m) => m.is_active === true && m.stock > 0);

  // 2. Terapkan Filter Teks (Cari di Merek atau Model)
  if (filters.value.q) {
    const keyword = filters.value.q.toLowerCase();
    result = result.filter(
      (m) =>
        m.brand.toLowerCase().includes(keyword) ||
        m.model_name.toLowerCase().includes(keyword),
    );
  }

  // 3. Terapkan Filter Dropdown
  if (filters.value.type)
    result = result.filter((m) => m.vehicle_type === filters.value.type);
  if (filters.value.condition)
    result = result.filter((m) => m.condition === filters.value.condition);
  if (filters.value.category)
    result = result.filter((m) => m.category === filters.value.category);

  // 4. Terapkan Sorting
  result.sort((a, b) => {
    if (sortBy.value === "price_asc") return a.price - b.price;
    if (sortBy.value === "price_desc") return b.price - a.price;
    // Default 'newest' mengandalkan ID terbesar
    return b.id - a.id;
  });

  return result;
});

const formatCurrency = (value) => {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    minimumFractionDigits: 0,
  }).format(value || 0);
};

const getImageUrl = (url) => {
  if (!url) return null;
  return `${BASE_URL}${url}?t=${new Date().getTime()}`;
};

const getWaLink = (motor) => {
  return `https://wa.me/${DEALER_WA_NUMBER}?text=${encodeURIComponent(`Halo CS Abu Motor, saya tertarik dengan ${motor.vehicle_type} *${motor.brand} ${motor.model_name}* warna ${motor.color} (Harga: ${formatCurrency(motor.price)}). Apakah stoknya tersedia?`)}`;
};

const fetchKatalog = async () => {
  isLoading.value = true;
  try {
    // Kita ambil semua data sekali dari API, lalu sisanya di-handle Vue Computed agar super cepat!
    const response = await axios.get(`${BASE_URL}/api/inventory/`);
    motors.value = response.data.data;
  } catch (error) {
    console.error("Gagal mengambil data katalog:", error);
  } finally {
    isLoading.value = false;
  }
};

const resetFilters = () => {
  filters.value = { q: "", type: "", condition: "", category: "" };
  sortBy.value = "newest";
  adjustCategoryOptions();

  // Bersihkan URL tanpa merefresh halaman
  if (Object.keys(route.query).length > 0) {
    router.replace("/katalog");
  }
};

// SINKRONISASI DARI URL KE STATE (Saat pengunjung klik dari Home)
const syncFromUrl = () => {
  if (route.query.q) filters.value.q = route.query.q;
  if (route.query.type) filters.value.type = route.query.type;
  if (route.query.condition) filters.value.condition = route.query.condition;
  if (route.query.category) filters.value.category = route.query.category;
  adjustCategoryOptions();
};

// PANTAU PERUBAHAN STATE UNTUK DIKEMBALIKAN KE URL (Opsional agar URL bisa di-share)
watch(
  filters,
  (newFilters) => {
    const query = {};
    if (newFilters.q) query.q = newFilters.q;
    if (newFilters.type) query.type = newFilters.type;
    if (newFilters.condition) query.condition = newFilters.condition;
    if (newFilters.category) query.category = newFilters.category;

    // Update URL secara senyap
    router.replace({ query }).catch(() => {});
  },
  { deep: true },
);

const dynamicCategories = ref([]);

const fetchCategories = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/api/master/categories`);
    dynamicCategories.value = response.data.data;
  } catch (err) {
    console.error("Failed fetching categories", err);
  }
};

onMounted(() => {
  syncFromUrl();
  fetchCategories();
  fetchKatalog();
});
</script>
