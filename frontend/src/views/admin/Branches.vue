<template>
  <div>
    <!-- HEADER -->
    <div
      class="flex flex-col items-start justify-between gap-4 mb-6 sm:flex-row sm:items-center"
    >
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Manajemen Cabang</h1>
        <p class="mt-1 text-sm text-gray-500">
          Kelola daftar cabang atau lokasi dealer Abu Motor.
        </p>
      </div>

      <div class="flex flex-col w-full gap-3 sm:flex-row sm:w-auto">
        <div class="relative w-full sm:w-64">
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
            placeholder="Cari nama cabang..."
            class="block w-full py-2 pl-10 pr-3 leading-5 placeholder-gray-500 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>
        <button
          @click="openModal()"
          class="flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-white transition-colors bg-indigo-600 rounded-lg shadow-sm hover:bg-indigo-700 shrink-0"
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
              d="M12 4v16m8-8H4"
            ></path>
          </svg>
          Tambah Cabang
        </button>
      </div>
    </div>

    <!-- TABEL CABANG -->
    <div
      class="overflow-hidden bg-white border border-gray-200 shadow-sm rounded-xl"
    >
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                class="px-6 py-3 text-xs font-semibold text-left text-gray-500 uppercase"
              >
                Nama Cabang
              </th>
              <th
                class="px-6 py-3 text-xs font-semibold text-left text-gray-500 uppercase"
              >
                Alamat Lengkap
              </th>
              <th
                class="px-6 py-3 text-xs font-semibold text-left text-gray-500 uppercase"
              >
                Kontak / Telepon
              </th>
              <th
                class="px-6 py-3 text-xs font-semibold text-right text-gray-500 uppercase"
              >
                Aksi
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="isLoading" class="text-center">
              <td colspan="4" class="px-6 py-6 text-sm text-gray-500">
                Memuat data...
              </td>
            </tr>
            <tr v-else-if="filteredBranches.length === 0" class="text-center">
              <td colspan="4" class="px-6 py-8 text-sm text-gray-500">
                Tidak ada cabang yang ditemukan.
              </td>
            </tr>
            <tr
              v-else
              v-for="branch in filteredBranches"
              :key="branch.id"
              class="transition-colors hover:bg-gray-50"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center gap-3">
                  <div
                    class="flex items-center justify-center w-10 h-10 bg-indigo-100 rounded-lg shrink-0"
                  >
                    <svg
                      class="w-5 h-5 text-indigo-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1v1H9V7zm5 0h1v1h-1V7zm-5 4h1v1H9v-1zm5 0h1v1h-1v-1zm-3 4H2v-2h9v2z"
                      ></path>
                    </svg>
                  </div>
                  <div>
                    <div class="text-sm font-bold text-gray-900">
                      {{ branch.name }}
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">
                <p class="w-64 truncate whitespace-normal line-clamp-2">
                  {{ branch.address || "-" }}
                </p>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600 whitespace-nowrap">
                {{ branch.phone || "-" }}
              </td>
              <td
                class="px-6 py-4 text-sm font-medium text-right whitespace-nowrap"
              >
                <button
                  @click="openModal(branch)"
                  class="mr-3 text-blue-600 transition-colors hover:text-blue-900"
                >
                  Edit
                </button>
                <button
                  @click="deleteBranch(branch.id)"
                  class="text-red-600 transition-colors hover:text-red-900"
                >
                  Hapus
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL FORM -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen px-4">
        <div
          class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
          @click="closeModal"
        ></div>
        <div
          class="relative w-full max-w-md p-6 transition-all bg-white shadow-xl rounded-xl"
        >
          <h3 class="pb-2 mb-4 text-lg font-bold text-gray-900 border-b">
            {{ isEditMode ? "Edit Cabang" : "Tambah Cabang Baru" }}
          </h3>
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700"
                >Nama Cabang</label
              >
              <input
                v-model="form.name"
                required
                type="text"
                placeholder="Contoh: Abu Motor Pusat"
                class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700"
                >No. Telepon / WhatsApp</label
              >
              <input
                v-model="form.phone"
                type="text"
                placeholder="Contoh: 0812xxxxxx"
                class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700"
                >Alamat Lengkap</label
              >
              <textarea
                v-model="form.address"
                rows="3"
                placeholder="Jl. Raya Utama No. 1..."
                class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg resize-none focus:ring-indigo-500 focus:border-indigo-500"
              ></textarea>
            </div>

            <div class="flex justify-end gap-2 pt-5 mt-5 border-t">
              <button
                type="button"
                @click="closeModal"
                class="px-5 py-2 text-sm font-medium text-gray-700 transition-colors bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Batal
              </button>
              <button
                type="submit"
                :disabled="isSaving"
                class="px-5 py-2 text-sm font-bold text-white transition-colors bg-indigo-600 rounded-lg shadow-sm hover:bg-indigo-700 disabled:opacity-70"
              >
                {{
                  isSaving
                    ? "Menyimpan..."
                    : isEditMode
                      ? "Simpan Perubahan"
                      : "Buat Cabang"
                }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../../services/api";

const branches = ref([]);
const isLoading = ref(false);
const isSaving = ref(false);
const searchQuery = ref("");

const isModalOpen = ref(false);
const isEditMode = ref(false);
const currentId = ref(null);

const form = ref({ name: "", address: "", phone: "" });

// Filter Pencarian
const filteredBranches = computed(() => {
  if (!searchQuery.value) return branches.value;
  const q = searchQuery.value.toLowerCase();
  return branches.value.filter(
    (b) =>
      b.name.toLowerCase().includes(q) ||
      (b.address && b.address.toLowerCase().includes(q)),
  );
});

// Ambil Data Cabang
const fetchBranches = async () => {
  isLoading.value = true;
  try {
    const res = await api.get("/master/branches");
    branches.value = res.data.data;
  } catch (e) {
    console.error(e);
    alert("Gagal mengambil data cabang.");
  } finally {
    isLoading.value = false;
  }
};

const openModal = (item = null) => {
  if (item) {
    isEditMode.value = true;
    currentId.value = item.id;
    form.value = {
      name: item.name,
      address: item.address || "",
      phone: item.phone || "",
    };
  } else {
    isEditMode.value = false;
    currentId.value = null;
    form.value = { name: "", address: "", phone: "" };
  }
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const handleSubmit = async () => {
  isSaving.value = true;
  try {
    if (isEditMode.value) {
      await api.put(`/master/branches/${currentId.value}`, form.value);
    } else {
      await api.post("/master/branches", form.value);
    }
    closeModal();
    fetchBranches();
  } catch (e) {
    alert(e.response?.data?.message || "Gagal menyimpan data cabang.");
  } finally {
    isSaving.value = false;
  }
};

const deleteBranch = async (id) => {
  if (
    confirm(
      "HAPUS CABANG?\n\nPeringatan: Menghapus cabang dapat menyebabkan error pada data stok dan karyawan yang terhubung ke cabang ini. Lanjutkan?",
    )
  ) {
    try {
      await api.delete(`/master/branches/${id}`);
      fetchBranches();
    } catch (e) {
      alert(
        "Gagal menghapus cabang. Pastikan tidak ada data yang terkait dengan cabang ini.",
      );
    }
  }
};

onMounted(() => {
  fetchBranches();
});
</script>
