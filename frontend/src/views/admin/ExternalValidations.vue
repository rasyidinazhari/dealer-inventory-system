<template>
  <div>
    <div
      class="flex flex-col items-start justify-between gap-4 mb-6 sm:flex-row sm:items-center"
    >
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Validasi Motor Seller</h1>
        <p class="mt-1 text-sm text-gray-500">
          Tinjau dan setujui pengajuan motor dari seller eksternal.
        </p>
      </div>

      <div class="relative w-full sm:w-72">
        <div
          class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none"
        >
          <svg
            class="w-5 h-5 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Cari motor atau nama seller..."
          class="block w-full py-2 pl-10 pr-3 leading-5 placeholder-gray-500 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>
    </div>

    <div
      class="overflow-hidden bg-white border border-gray-200 shadow-sm rounded-xl"
    >
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Unit & Seller
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Tanggal Pengajuan
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Harga Asli (Base)
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Status
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-right text-gray-500 uppercase"
              >
                Aksi
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="isLoading" class="text-center">
              <td colspan="5" class="px-6 py-8 text-sm text-gray-500">
                Memuat data pengajuan...
              </td>
            </tr>
            <tr v-else-if="pendingMotors.length === 0" class="text-center">
              <td colspan="5" class="px-6 py-12">
                <svg
                  class="w-12 h-12 mx-auto mb-3 text-gray-300"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  ></path>
                </svg>
                <p class="text-sm font-medium text-gray-500">
                  Hore! Tidak ada pengajuan motor yang menunggu validasi.
                </p>
              </td>
            </tr>
            <tr
              v-else
              v-for="motor in filteredMotors"
              :key="motor.id"
              class="hover:bg-gray-50"
            >
              <td class="flex items-center gap-4 px-6 py-4 whitespace-nowrap">
                <div
                  class="flex items-center justify-center flex-shrink-0 w-12 h-12 overflow-hidden border border-gray-200 rounded-md bg-gray-50"
                >
                  <img
                    v-if="motor.image_url"
                    :src="getImageUrl(motor.image_url)"
                    class="object-cover w-full h-full"
                  />
                  <span v-else class="text-xs text-gray-400">No Pic</span>
                </div>
                <div>
                  <div class="text-sm font-bold text-gray-900">
                    {{ motor.brand }} {{ motor.model_name }}
                  </div>
                  <div class="text-xs font-medium text-blue-600">
                    Seller: @{{ motor.seller_name }}
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500 whitespace-nowrap">
                {{ motor.created_at }}
              </td>
              <td
                class="px-6 py-4 text-sm font-bold text-gray-900 whitespace-nowrap"
              >
                {{ formatCurrency(motor.base_price) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="px-2.5 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800"
                  >Menunggu Review</span
                >
              </td>
              <td
                class="px-6 py-4 text-sm font-medium text-right whitespace-nowrap"
              >
                <button
                  @click="openModal(motor)"
                  class="px-4 py-2 text-white transition-colors bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700"
                >
                  Review Data
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 z-40 overflow-y-auto">
      <div
        class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:p-0"
      >
        <div
          class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
          @click="closeModal"
        ></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen"
          >&#8203;</span
        >

        <div
          class="inline-block w-full overflow-hidden text-left align-bottom transition-all transform bg-white shadow-xl rounded-xl sm:my-8 sm:align-middle sm:max-w-4xl"
        >
          <form @submit.prevent="handleApprove">
            <div
              class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4 max-h-[85vh] overflow-y-auto"
            >
              <div class="flex items-center justify-between pb-3 mb-5 border-b">
                <h3 class="text-xl font-bold text-gray-900">
                  Review Titipan: {{ selectedMotor?.brand }}
                  {{ selectedMotor?.model_name }}
                </h3>
                <span
                  class="px-3 py-1 text-xs font-bold text-blue-800 bg-blue-100 rounded-full"
                  >Seller: @{{ selectedMotor?.seller_name }}</span
                >
              </div>

              <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
                <div class="space-y-5 md:col-span-2">
                  <h4
                    class="p-2 text-sm font-bold text-gray-700 uppercase border border-gray-200 rounded bg-gray-50"
                  >
                    1. Spesifikasi Kendaraan
                  </h4>

                  <div
                    class="grid grid-cols-2 gap-4 px-2 text-sm sm:grid-cols-3"
                  >
                    <div>
                      <span class="block text-xs text-gray-500">Kategori</span
                      ><span class="font-medium text-gray-900">{{
                        selectedMotor?.category || "-"
                      }}</span>
                    </div>
                    <div>
                      <span class="block text-xs text-gray-500">Warna</span
                      ><span class="font-medium text-gray-900">{{
                        selectedMotor?.color || "-"
                      }}</span>
                    </div>
                    <div>
                      <span class="block text-xs text-gray-500">Tahun</span
                      ><span class="font-medium text-gray-900">{{
                        selectedMotor?.year || "-"
                      }}</span>
                    </div>
                    <div>
                      <span class="block text-xs text-gray-500">Transmisi</span
                      ><span class="font-medium text-gray-900">{{
                        selectedMotor?.transmission || "-"
                      }}</span>
                    </div>
                    <div>
                      <span class="block text-xs text-gray-500"
                        >Jarak Tempuh</span
                      ><span class="font-medium text-gray-900">{{
                        selectedMotor?.mileage || "-"
                      }}</span>
                    </div>
                    <div>
                      <span class="block text-xs text-gray-500"
                        >Kapasitas Mesin</span
                      ><span class="font-medium text-gray-900">{{
                        selectedMotor?.engine_capacity || "-"
                      }}</span>
                    </div>
                  </div>

                  <div class="px-2">
                    <span class="text-gray-500 block text-xs mb-1.5"
                      >Fitur Unggulan</span
                    >
                    <div
                      class="flex flex-wrap gap-2"
                      v-if="selectedMotor?.features"
                    >
                      <span
                        v-for="(feat, idx) in selectedMotor.features.split(',')"
                        :key="idx"
                        class="bg-gray-100 text-gray-700 px-2.5 py-1 rounded border border-gray-200 text-xs font-medium"
                        >{{ feat.trim() }}</span
                      >
                    </div>
                    <span v-else class="text-sm text-gray-900">-</span>
                  </div>

                  <div class="px-2">
                    <span class="text-gray-500 block text-xs mb-1.5"
                      >Kelengkapan Dokumen</span
                    >
                    <div
                      class="flex flex-wrap gap-2"
                      v-if="selectedMotor?.documents"
                    >
                      <span
                        v-for="(doc, idx) in selectedMotor.documents.split(',')"
                        :key="idx"
                        class="bg-green-50 text-green-700 px-2.5 py-1 rounded border border-green-200 text-xs font-bold flex items-center gap-1"
                      >
                        <svg
                          class="w-3 h-3"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="3"
                            d="M5 13l4 4L19 7"
                          ></path>
                        </svg>
                        {{ doc.trim() }}
                      </span>
                    </div>
                    <span v-else class="text-sm font-medium text-red-500"
                      >Dokumen tidak dicantumkan!</span
                    >
                  </div>

                  <div class="px-2">
                    <span class="text-gray-500 block text-xs mb-1.5"
                      >Deskripsi dari Seller</span
                    >
                    <div
                      class="p-3 text-sm leading-relaxed text-gray-700 whitespace-pre-line border border-gray-200 rounded-lg bg-gray-50"
                    >
                      {{
                        selectedMotor?.description ||
                        "Tidak ada deskripsi tambahan."
                      }}
                    </div>
                  </div>
                </div>

                <div
                  class="relative flex flex-col h-full p-5 overflow-hidden bg-white border border-blue-100 shadow-sm rounded-xl"
                >
                  <div
                    class="absolute top-0 right-0 w-20 h-20 rounded-bl-full bg-blue-50 -z-10"
                  ></div>
                  <h4
                    class="pb-2 mb-4 text-sm font-bold text-gray-700 uppercase border-b"
                  >
                    2. Inspeksi & Harga
                  </h4>

                  <!-- PREVIEW GAMBAR & THUMBNAIL -->
                  <div class="mb-5">
                    <!-- Foto Utama yang Aktif -->
                    <div
                      @click="openLightbox"
                      class="relative flex items-center justify-center mb-2 overflow-hidden bg-gray-100 border border-gray-200 rounded-lg cursor-pointer h-44 group"
                    >
                      <img
                        v-if="activeImage"
                        :src="getImageUrl(activeImage)"
                        class="object-cover w-full h-full transition-transform duration-300 group-hover:scale-105"
                        alt="Preview"
                      />
                      <div
                        v-else
                        class="flex flex-col items-center text-gray-400"
                      >
                        <svg
                          class="w-10 h-10 mb-2 text-gray-300"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="1.5"
                            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                          ></path>
                        </svg>
                        <span class="text-xs font-medium">Tidak ada foto</span>
                      </div>
                    </div>

                    <!-- Deretan Thumbnail Galeri -->
                    <div
                      class="flex gap-2 pb-1 overflow-x-auto hide-scrollbar snap-x"
                    >
                      <!-- Thumbnail Utama -->
                      <img
                        v-if="selectedMotor?.image_url"
                        @click="activeImage = selectedMotor.image_url"
                        :src="getImageUrl(selectedMotor.image_url)"
                        class="object-cover w-12 h-12 border-2 rounded-md cursor-pointer shrink-0 snap-start transition-all"
                        :class="
                          activeImage === selectedMotor.image_url
                            ? 'border-blue-500 shadow-sm'
                            : 'border-transparent opacity-60 hover:opacity-100'
                        "
                      />
                      <!-- Thumbnail Galeri Lainnya -->
                      <img
                        v-for="(g_img, idx) in selectedMotor?.gallery"
                        :key="idx"
                        @click="activeImage = g_img"
                        :src="getImageUrl(g_img)"
                        class="object-cover w-12 h-12 border-2 rounded-md cursor-pointer shrink-0 snap-start transition-all"
                        :class="
                          activeImage === g_img
                            ? 'border-blue-500 shadow-sm'
                            : 'border-transparent opacity-60 hover:opacity-100'
                        "
                      />
                    </div>
                  </div>

                  <div class="mb-5">
                    <p
                      class="mb-1 text-xs font-medium tracking-wider text-gray-500 uppercase"
                    >
                      Harga Dasar (Permintaan Seller)
                    </p>
                    <p class="text-2xl font-bold text-gray-900">
                      {{ formatCurrency(selectedMotor?.base_price) }}
                    </p>
                  </div>

                  <div class="mb-5">
                    <label class="block mb-2 text-sm font-bold text-gray-700"
                      >Margin Dealer / Fee (Rp)</label
                    >
                    <input
                      v-model="dealerFee"
                      type="number"
                      min="0"
                      required
                      @wheel.prevent
                      class="block w-full border-2 border-blue-200 rounded-lg py-2.5 px-3 focus:ring-blue-500 focus:border-blue-500 sm:text-sm font-bold text-blue-700 bg-blue-50/50"
                    />
                    <p class="mt-2 text-xs leading-snug text-gray-500">
                      Input keuntungan yang akan diambil dealer. Harga ini akan
                      ditambahkan ke Harga Dasar.
                    </p>
                  </div>

                  <div
                    class="p-4 mt-auto text-white bg-blue-600 shadow-md rounded-xl"
                  >
                    <p
                      class="mb-1 text-xs font-medium tracking-wider text-blue-100 uppercase"
                    >
                      Harga Tayang (OTR)
                    </p>
                    <p class="text-2xl font-black">
                      {{ formatCurrency(finalPrice) }}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div
              class="px-4 py-4 border-t border-gray-200 bg-gray-50 sm:px-6 sm:flex sm:items-center sm:justify-between"
            >
              <button
                type="button"
                @click="openRejectModal"
                class="w-full sm:w-auto inline-flex justify-center items-center gap-2 rounded-lg shadow-sm px-6 py-2.5 bg-red-100 text-base font-bold text-red-700 hover:bg-red-200 sm:text-sm transition-colors mt-3 sm:mt-0"
              >
                <svg
                  class="w-5 h-5"
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
                Tolak Pengajuan
              </button>

              <div
                class="flex flex-col-reverse sm:flex-row gap-3 mt-3 sm:mt-0 w-full sm:w-auto"
              >
                <button
                  type="button"
                  @click="closeModal"
                  class="w-full inline-flex justify-center rounded-lg border border-gray-300 shadow-sm px-6 py-2.5 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:w-auto sm:text-sm transition-colors"
                >
                  Batal
                </button>
                <button
                  type="submit"
                  :disabled="isSaving"
                  class="w-full inline-flex justify-center items-center gap-2 rounded-lg shadow-sm px-6 py-2.5 bg-green-600 text-base font-bold text-white hover:bg-green-700 sm:w-auto sm:text-sm transition-colors disabled:opacity-70"
                >
                  <svg
                    v-if="!isSaving"
                    class="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    ></path>
                  </svg>
                  {{ isSaving ? "Memproses..." : "Setujui & Tayangkan" }}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="isRejectModalOpen" class="fixed inset-0 z-[60] overflow-y-auto">
      <div
        class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:p-0"
      >
        <div
          class="fixed inset-0 transition-opacity bg-gray-800 bg-opacity-75 backdrop-blur-sm"
          @click="closeRejectModal"
        ></div>
        <div
          class="inline-block w-full max-w-lg p-6 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
        >
          <div class="flex items-center gap-4 mb-5">
            <div
              class="flex items-center justify-center w-12 h-12 bg-red-100 rounded-full shrink-0"
            >
              <svg
                class="w-6 h-6 text-red-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                ></path>
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900">
                Tolak Pengajuan Motor
              </h3>
              <p class="text-sm text-gray-500">
                Beri tahu seller mengapa motor ini ditolak.
              </p>
            </div>
          </div>

          <textarea
            v-model="rejectionReason"
            rows="4"
            class="w-full p-3 text-sm text-gray-700 border border-gray-300 rounded-lg bg-gray-50 focus:bg-white focus:ring-red-500 focus:border-red-500"
            placeholder="Contoh: Dokumen tidak lengkap, STNK mati, atau Harga dari seller terlalu tinggi..."
            required
          ></textarea>

          <div class="flex justify-end gap-3 mt-6">
            <button
              @click="closeRejectModal"
              class="px-5 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Kembali
            </button>
            <button
              @click="handleReject"
              :disabled="!rejectionReason.trim() || isRejecting"
              class="px-5 py-2 text-sm font-bold text-white bg-red-600 rounded-lg hover:bg-red-700 disabled:opacity-50"
            >
              {{ isRejecting ? "Memproses..." : "Konfirmasi Tolak" }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="isLightboxOpen && activeImage"
      class="fixed inset-0 z-[70] flex items-center justify-center p-4 bg-black/90 backdrop-blur-sm transition-opacity"
      @click="isLightboxOpen = false"
    >
      <div
        class="relative flex items-center justify-center w-full h-full max-w-7xl"
      >
        <img
          :src="getImageUrl(activeImage)"
          class="object-contain max-w-full max-h-full rounded-lg shadow-2xl"
          @click.stop
          alt="Full screen preview"
        />
        <button
          @click="isLightboxOpen = false"
          class="absolute p-2 text-white transition-colors rounded-full top-4 right-4 bg-black/50 hover:bg-black/70 focus:outline-none group"
        >
          <svg
            class="w-8 h-8 transition-transform group-hover:scale-110"
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
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from "vue";
import api, { BASE_URL } from "../../services/api";

const pendingMotors = ref([]);
const searchQuery = ref("");
const isLoading = ref(true);

// State Modal Review & Lightbox
const isModalOpen = ref(false);
const isLightboxOpen = ref(false);
const isSaving = ref(false);
const selectedMotor = ref(null);
const activeImage = ref(null);
const dealerFee = ref(0);

// State Modal Penolakan (Reject)
const isRejectModalOpen = ref(false);
const isRejecting = ref(false);
const rejectionReason = ref("");

const finalPrice = computed(() => {
  if (!selectedMotor.value) return 0;
  return Number(selectedMotor.value.base_price) + Number(dealerFee.value || 0);
});

const filteredMotors = computed(() => {
  if (!searchQuery.value) return pendingMotors.value;
  const query = searchQuery.value.toLowerCase();
  return pendingMotors.value.filter((motor) => {
    return (
      motor.model_name.toLowerCase().includes(query) ||
      motor.brand.toLowerCase().includes(query) ||
      motor.seller_name.toLowerCase().includes(query) ||
      motor.sku_code.toLowerCase().includes(query)
    );
  });
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
  return `${BASE_URL}${url}`;
};

const fetchPendingMotors = async () => {
  isLoading.value = true;
  try {
    // 1. Ambil ID Cabang dari LocalStorage (Di-set oleh Navbar)
    const branchId = localStorage.getItem("selected_branch_id") || "";

    // 2. Kirim branch_id ke Backend
    const response = await api.get(`/inventory/pending?branch_id=${branchId}`);

    pendingMotors.value = response.data.data;
  } catch (error) {
    console.error("Gagal mengambil data:", error);
  } finally {
    isLoading.value = false;
  }
};

// --- FUNGSI MODAL REVIEW ---
const openModal = (motor) => {
  selectedMotor.value = motor;
  activeImage.value = motor.image_url;
  dealerFee.value = 0;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  isLightboxOpen.value = false;
  selectedMotor.value = null;
};

const openLightbox = () => {
  if (selectedMotor.value?.image_url) {
    isLightboxOpen.value = true;
  }
};

const handleApprove = async () => {
  isSaving.value = true;
  try {
    await api.put(`/inventory/${selectedMotor.value.id}/approve`, {
      dealer_fee: dealerFee.value,
    });
    closeModal();
    fetchPendingMotors();
    alert("Sukses! Motor berhasil tayang di Katalog Utama.");
  } catch (error) {
    alert(error.response?.data?.message || "Gagal menyetujui motor");
  } finally {
    isSaving.value = false;
  }
};

// --- FUNGSI MODAL PENOLAKAN ---
const openRejectModal = () => {
  rejectionReason.value = ""; // Kosongkan form teks setiap kali dibuka
  isRejectModalOpen.value = true;
};

const closeRejectModal = () => {
  isRejectModalOpen.value = false;
};

const handleReject = async () => {
  if (!rejectionReason.value.trim()) return;

  isRejecting.value = true;
  try {
    await api.put(`/inventory/${selectedMotor.value.id}/reject`, {
      rejection_reason: rejectionReason.value,
    });

    closeRejectModal();
    closeModal(); // Tutup juga modal review utama
    fetchPendingMotors(); // Refresh tabel
    alert("Pengajuan motor telah berhasil ditolak.");
  } catch (error) {
    alert(error.response?.data?.message || "Gagal menolak pengajuan motor");
  } finally {
    isRejecting.value = false;
  }
};

const handleBranchChange = () => {
  fetchPendingMotors(); // Panggil ulang API jika cabang berubah
};

onMounted(() => {
  fetchPendingMotors();
  window.addEventListener("branchChanged", handleBranchChange); // Dengarkan perubahan
});

onUnmounted(() => {
  window.removeEventListener("branchChanged", handleBranchChange); // Bersihkan saat pindah halaman
});
</script>
