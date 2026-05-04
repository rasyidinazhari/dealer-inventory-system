<template>
  <div>
    <div
      class="flex flex-col items-start justify-between gap-4 mb-6 sm:flex-row sm:items-center"
    >
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Manajemen Banner Promo</h1>
        <p class="mt-1 text-sm text-gray-500">
          Atur gambar slider promo yang tampil di halaman depan website.
        </p>
      </div>

      <button
        @click="openModal"
        class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-lg text-sm font-bold flex items-center gap-2 shadow-sm transition-colors"
      >
        <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
          <path
            fill-rule="evenodd"
            d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
            clip-rule="evenodd"
          />
        </svg>
        Tambah Banner
      </button>
    </div>

    <div v-if="isLoading" class="flex justify-center py-12">
      <div
        class="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full"
      ></div>
    </div>

    <div
      v-else-if="banners.length === 0"
      class="bg-white border-2 border-dashed border-gray-200 rounded-2xl p-12 text-center"
    >
      <p class="text-gray-500">
        Belum ada banner promo. Silakan tambah banner baru.
      </p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="banner in banners"
        :key="banner.id"
        class="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="h-40 bg-gray-100 relative overflow-hidden">
          <img
            :src="getImageUrl(banner.image_url)"
            class="w-full h-full object-cover"
            alt="Banner"
          />
          <div class="absolute top-2 right-2 flex gap-2">
            <span
              :class="
                banner.is_active
                  ? 'bg-green-100 text-green-700'
                  : 'bg-gray-100 text-gray-700'
              "
              class="px-2 py-1 rounded text-[10px] font-bold uppercase shadow-sm"
            >
              {{ banner.is_active ? "Aktif" : "Nonaktif" }}
            </span>
          </div>
        </div>
        <div class="p-4">
          <h3 class="font-bold text-gray-900 truncate">
            {{ banner.title || "Tanpa Judul" }}
          </h3>
          <p class="text-xs text-gray-500 mt-1 truncate">
            {{ banner.link_url || "Tidak ada link" }}
          </p>
          <div
            class="flex items-center justify-between mt-4 pt-4 border-t border-gray-50"
          >
            <span class="text-xs font-medium text-gray-400"
              >Urutan: {{ banner.order }}</span
            >
            <button
              @click="handleDelete(banner.id)"
              class="text-red-600 hover:text-red-800 text-sm font-bold flex items-center gap-1"
            >
              <svg
                class="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                ></path>
              </svg>
              Hapus
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen px-4">
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75"
          @click="closeModal"
        ></div>
        <div
          class="relative bg-white rounded-2xl shadow-xl w-full max-w-lg p-6 overflow-hidden"
        >
          <form @submit.prevent="handleSubmit">
            <h3 class="text-xl font-bold text-gray-900 mb-6">
              Tambah Banner Promo
            </h3>

            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700"
                  >Judul Banner (Opsional)</label
                >
                <input
                  v-model="form.title"
                  type="text"
                  placeholder="Cth: Promo Ramadhan"
                  class="mt-1 block w-full border border-gray-300 rounded-xl px-4 py-2 text-sm focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700"
                  >Link Tujuan (Opsional)</label
                >
                <input
                  v-model="form.link_url"
                  type="text"
                  placeholder="Cth: /katalog?type=Mobil"
                  class="mt-1 block w-full border border-gray-300 rounded-xl px-4 py-2 text-sm focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700"
                    >Urutan Tampil</label
                  >
                  <input
                    v-model="form.order"
                    type="number"
                    class="mt-1 block w-full border border-gray-300 rounded-xl px-4 py-2 text-sm focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2"
                  >Gambar Banner (Rasio 16:9 disarankan)</label
                >
                <input
                  type="file"
                  @change="handleFileUpload"
                  accept="image/*"
                  required
                  class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                />
              </div>
            </div>

            <div class="mt-8 flex gap-3">
              <button
                type="button"
                @click="closeModal"
                class="flex-1 px-4 py-2.5 border border-gray-300 text-gray-700 font-bold rounded-xl hover:bg-gray-50 transition-colors"
              >
                Batal
              </button>
              <button
                type="submit"
                :disabled="isSaving"
                class="flex-1 px-4 py-2.5 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition-colors disabled:opacity-50"
              >
                {{ isSaving ? "Mengunggah..." : "Simpan Banner" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api, { BASE_URL } from "../../services/api";

const banners = ref([]);
const isLoading = ref(true);
const isModalOpen = ref(false);
const isSaving = ref(false);
const selectedImage = ref(null);

const form = ref({
  title: "",
  link_url: "",
  order: 0,
});

const getImageUrl = (url) => `${BASE_URL}${url}?t=${new Date().getTime()}`;

const fetchBanners = async () => {
  isLoading.value = true;
  try {
    const res = await api.get("/banners/");
    banners.value = res.data.data;
  } catch (err) {
    console.error("Gagal memuat banner", err);
  } finally {
    isLoading.value = false;
  }
};

const handleFileUpload = (e) => {
  selectedImage.value = e.target.files[0];
};

const openModal = () => {
  isModalOpen.value = true;
  form.value = { title: "", link_url: "", order: banners.value.length };
  selectedImage.value = null;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const handleSubmit = async () => {
  if (!selectedImage.value) return alert("Pilih gambar terlebih dahulu");

  isSaving.value = true;
  try {
    const formData = new FormData();
    formData.append("title", form.value.title);
    formData.append("link_url", form.value.link_url);
    formData.append("order", form.value.order);

    // Pastikan nama append ini 'image', karena backend mencarinya dengan request.files.get('image')
    formData.append("image", selectedImage.value);

    // FIX: Tambahkan header multipart/form-data agar Flask tahu ini adalah kiriman file fisik!
    await api.post("/banners/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    closeModal();
    fetchBanners();
    alert("Banner berhasil diunggah!");
  } catch (err) {
    alert(err.response?.data?.message || "Gagal mengunggah banner");
    console.error(err);
  } finally {
    isSaving.value = false;
  }
};

const handleDelete = async (id) => {
  if (!confirm("Hapus banner ini?")) return;
  try {
    await api.delete(`/banners/${id}`);
    fetchBanners();
  } catch (err) {
    alert("Gagal menghapus banner");
  }
};

onMounted(fetchBanners);
</script>
