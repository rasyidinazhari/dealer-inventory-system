<template>
  <div>
    <div
      class="flex flex-col items-start justify-between gap-4 mb-6 sm:flex-row sm:items-center"
    >
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Master Data Seller</h1>
        <p class="mt-1 text-sm text-gray-500">
          Daftar mitra eksternal yang menitipkan motor di dealer.
        </p>
      </div>

      <div class="relative w-full sm:w-64">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Cari nama seller atau nomor HP..."
          class="block w-full py-2.5 pl-4 pr-3 text-sm bg-white border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500"
        />
      </div>
    </div>

    <div class="bg-white border border-gray-200 shadow-sm rounded-xl">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                scope="col"
                class="px-4 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase sm:px-6"
              >
                Nama Seller
              </th>
              <th
                scope="col"
                class="px-4 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase sm:px-6"
              >
                Kontak
              </th>
              <!-- TAMBAHKAN HEADER CABANG DI SINI -->
              <th
                scope="col"
                class="px-4 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase sm:px-6"
              >
                Cabang
              </th>
              <th
                scope="col"
                class="px-4 py-3 text-xs font-semibold tracking-wider text-center text-gray-500 uppercase sm:px-6"
              >
                Titipan
              </th>
              <th
                scope="col"
                class="px-4 py-3 text-xs font-semibold tracking-wider text-center text-gray-500 uppercase sm:px-6"
              >
                Aktif
              </th>
              <th
                scope="col"
                class="hidden px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase md:table-cell"
              >
                Bergabung
              </th>
              <th
                scope="col"
                class="px-4 py-3 text-xs font-semibold tracking-wider text-right text-gray-500 uppercase sm:px-6"
              >
                Aksi
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="isLoading">
              <td colspan="6" class="px-6 py-8 text-center text-gray-500">
                Memuat data seller...
              </td>
            </tr>
            <tr v-else-if="filteredSellers.length === 0">
              <td colspan="6" class="px-6 py-8 text-center text-gray-500">
                Tidak ada data seller ditemukan.
              </td>
            </tr>

            <tr
              v-else
              v-for="seller in filteredSellers"
              :key="seller.id"
              class="transition-colors hover:bg-gray-50"
            >
              <td class="px-4 py-4 whitespace-nowrap sm:px-6">
                <div class="text-sm font-medium text-gray-900">
                  {{ seller.full_name }}
                </div>
                <div class="text-xs text-gray-500">@{{ seller.username }}</div>
              </td>
              <td
                class="px-4 py-4 text-sm text-gray-700 whitespace-nowrap sm:px-6"
              >
                {{ seller.phone_number }}
              </td>
              <td
                class="px-4 py-4 text-sm font-bold text-indigo-700 whitespace-nowrap sm:px-6"
              >
                {{ seller.branch_name }}
              </td>
              <td
                class="px-4 py-4 text-sm font-bold text-center text-gray-900 whitespace-nowrap sm:px-6"
              >
                {{ seller.total_motors }}
              </td>
              <td class="px-4 py-4 text-center whitespace-nowrap sm:px-6">
                <span
                  class="px-2.5 py-1 text-xs font-semibold text-green-800 bg-green-100 rounded-full"
                  >{{ seller.active_motors }}</span
                >
              </td>
              <td
                class="hidden px-6 py-4 text-sm text-gray-500 whitespace-nowrap md:table-cell"
              >
                {{ seller.joined_at }}
              </td>
              <td class="px-4 py-4 text-right whitespace-nowrap sm:px-6">
                <button
                  @click="contactWhatsApp(seller)"
                  class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs sm:text-sm font-medium text-white transition-colors bg-green-500 rounded-md hover:bg-green-600 focus:outline-none"
                  :disabled="
                    !seller.phone_number || seller.phone_number === '-'
                  "
                  :class="{
                    'opacity-50 cursor-not-allowed':
                      !seller.phone_number || seller.phone_number === '-',
                  }"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path
                      d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 00-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"
                    />
                  </svg>
                  <span class="hidden sm:inline">Hubungi WA</span>
                  <span class="inline sm:hidden">Chat</span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import api from "../../services/api"; // Pastikan path ini benar

const sellers = ref([]);
const isLoading = ref(true);
const searchQuery = ref("");

const filteredSellers = computed(() => {
  if (!searchQuery.value) return sellers.value;
  const query = searchQuery.value.toLowerCase();
  return sellers.value.filter(
    (s) =>
      s.full_name.toLowerCase().includes(query) ||
      s.username.toLowerCase().includes(query) ||
      (s.phone_number && s.phone_number.includes(query)) ||
      (s.branch_name && s.branch_name.toLowerCase().includes(query)), // <--- Tambah baris ini
  );
});

const fetchSellers = async () => {
  isLoading.value = true;
  try {
    // Ambil branch_id dari localStorage (yang di-set oleh Navbar)
    const branchId = localStorage.getItem("selected_branch_id") || "";

    // Kirim branch_id sebagai query parameter
    const response = await api.get(`/sellers/?branch_id=${branchId}`);
    sellers.value = response.data.data;
  } catch (error) {
    console.error("Gagal mengambil data seller", error);
  } finally {
    isLoading.value = false;
  }
};

const handleBranchChange = () => {
  fetchSellers(); // Refresh data tabel otomatis saat Navbar berubah
};

const contactWhatsApp = (seller) => {
  if (!seller.phone_number || seller.phone_number === "-") return;

  // Format nomor HP (Ganti 0 awalan dengan 62)
  let formattedNumber = seller.phone_number.replace(/\D/g, ""); // Hapus karakter non-angka
  if (formattedNumber.startsWith("0")) {
    formattedNumber = "62" + formattedNumber.substring(1);
  }

  const message = encodeURIComponent(
    `Halo Kak ${seller.full_name}, saya Admin dari Abu Motor Dealer. Saya ingin mengabarkan mengenai motor titipan Kakak...`,
  );
  window.open(`https://wa.me/${formattedNumber}?text=${message}`, "_blank");
};

onMounted(() => {
  fetchSellers();
  window.addEventListener("branchChanged", handleBranchChange); // Daftarkan listener
});

onUnmounted(() => {
  window.removeEventListener("branchChanged", handleBranchChange); // Hapus listener saat pindah halaman
});
</script>
