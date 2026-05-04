<template>
  <div>
    <div
      class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4"
    >
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Data Pelanggan</h1>
        <p class="text-sm text-gray-500 mt-1">
          Kelola daftar pelanggan dealer Anda.
        </p>
      </div>

      <div class="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
        <div class="relative w-full sm:w-64 shrink-0">
          <div
            class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
          >
            <svg
              class="h-5 w-5 text-gray-400"
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
            placeholder="Cari NIK atau Nama..."
            class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm shadow-sm"
          />
        </div>
        <button
          @click="openModal()"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium flex items-center justify-center gap-2 shadow-sm shrink-0 transition-colors"
        >
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path
              fill-rule="evenodd"
              d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
              clip-rule="evenodd"
            />
          </svg>
          Tambah Pelanggan
        </button>
      </div>
    </div>

    <div
      class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden"
    >
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider"
              >
                NIK KTP
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider"
              >
                Nama Lengkap
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider"
              >
                No. HP / WA
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider"
              >
                Alamat
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider"
              >
                Cabang
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider"
              >
                Aksi
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="isLoading" class="text-center">
              <td colspan="6" class="px-6 py-6 text-sm text-gray-500">
                Memuat data...
              </td>
            </tr>
            <tr v-else-if="filteredCustomers.length === 0" class="text-center">
              <td colspan="6" class="px-6 py-8 text-sm text-gray-500">
                Tidak ada pelanggan yang cocok.
              </td>
            </tr>
            <tr
              v-else
              v-for="c in filteredCustomers"
              :key="c.id"
              class="hover:bg-gray-50 transition-colors"
            >
              <td
                class="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900"
              >
                {{ c.nik }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-700"
              >
                {{ c.full_name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                {{ c.phone_number }}
              </td>
              <td
                class="px-6 py-4 text-sm text-gray-500 truncate max-w-xs"
                :title="c.address"
              >
                {{ c.address }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="px-2.5 py-1 bg-indigo-50 text-indigo-700 border border-indigo-100 text-[10px] font-bold rounded uppercase"
                >
                  {{ getBranchName(c.branch_id) }}
                </span>
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
              >
                <button
                  @click="openModal(c)"
                  class="text-blue-600 hover:text-blue-900 mr-4 transition-colors"
                >
                  Edit
                </button>
                <button
                  @click="deleteCustomer(c.id)"
                  class="text-red-600 hover:text-red-900 transition-colors"
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
      <div
        class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:p-0"
      >
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          @click="closeModal"
        ></div>
        <div
          class="relative bg-white rounded-xl shadow-xl w-full max-w-md p-6 text-left align-middle transition-all transform sm:my-8"
        >
          <h3 class="text-lg font-bold text-gray-900 mb-5 border-b pb-2">
            {{ isEditMode ? "Edit Data" : "Tambah Data" }} Pelanggan
          </h3>

          <form @submit.prevent="handleSubmit" class="space-y-4">
            <!-- Pilihan Cabang -->
            <div
              class="p-3 bg-indigo-50 border border-indigo-100 rounded-lg mb-2"
            >
              <label class="block text-sm font-bold text-indigo-900"
                >Cabang Terdaftar</label
              >
              <select
                v-model="form.branch_id"
                required
                class="mt-1 w-full border border-indigo-300 rounded-md py-2 px-3 bg-white focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm cursor-pointer"
              >
                <option value="" disabled>-- Pilih Cabang --</option>
                <option v-for="b in masterBranches" :key="b.id" :value="b.id">
                  {{ b.name }}
                </option>
              </select>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="sm:col-span-2">
                <label class="block text-sm font-semibold text-gray-700"
                  >Nama Lengkap</label
                ><input
                  v-model="form.full_name"
                  required
                  type="text"
                  class="mt-1 w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700"
                  >NIK KTP</label
                ><input
                  v-model="form.nik"
                  required
                  type="text"
                  class="mt-1 w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700"
                  >No HP/WA</label
                ><input
                  v-model="form.phone_number"
                  required
                  type="text"
                  class="mt-1 w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700"
                >Alamat Lengkap</label
              ><textarea
                v-model="form.address"
                rows="3"
                class="mt-1 w-full border border-gray-300 rounded-md py-2 px-3 focus:ring-blue-500 focus:border-blue-500 sm:text-sm resize-none"
              ></textarea>
            </div>

            <div class="flex justify-end gap-3 pt-5 border-t mt-6">
              <button
                type="button"
                @click="closeModal"
                class="px-5 py-2.5 bg-white border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors text-sm"
              >
                Batal
              </button>
              <button
                type="submit"
                class="px-5 py-2.5 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition-colors shadow-sm text-sm"
              >
                {{ isEditMode ? "Simpan Perubahan" : "Tambah Pelanggan" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import api from "../../services/api";

const customers = ref([]);
const masterBranches = ref([]);
const isLoading = ref(false);
const searchQuery = ref("");

const isModalOpen = ref(false);
const isEditMode = ref(false);
const currentId = ref(null);
const form = ref({
  nik: "",
  full_name: "",
  phone_number: "",
  address: "",
  branch_id: "",
});

// Pencarian
const filteredCustomers = computed(() => {
  if (!searchQuery.value) return customers.value;
  const q = searchQuery.value.toLowerCase();
  return customers.value.filter(
    (c) =>
      c.full_name.toLowerCase().includes(q) || c.nik.toLowerCase().includes(q),
  );
});

// Helper mendapatkan nama cabang
const getBranchName = (id) => {
  const branch = masterBranches.value.find((b) => b.id === id);
  return branch ? branch.name : "Unknown";
};

// Pengambilan Data Terpusat (Customers + Cabang)
const fetchData = async () => {
  isLoading.value = true;
  try {
    const branchId = localStorage.getItem("selected_branch_id") || "";

    const [custRes, branchRes] = await Promise.all([
      api.get(`/master/customers?branch_id=${branchId}`),
      api.get("/master/branches"),
    ]);

    customers.value = custRes.data.data;
    masterBranches.value = branchRes.data.data;
  } catch (e) {
    console.error("Gagal mengambil data pelanggan:", e);
  } finally {
    isLoading.value = false;
  }
};

// Listener untuk Navbar
const handleBranchChange = () => fetchData();

onMounted(() => {
  fetchData();
  window.addEventListener("branchChanged", handleBranchChange);
});

onUnmounted(() => {
  window.removeEventListener("branchChanged", handleBranchChange);
});

const openModal = (item = null) => {
  if (item) {
    isEditMode.value = true;
    currentId.value = item.id;
    form.value = { ...item };
  } else {
    isEditMode.value = false;
    currentId.value = null;
    form.value = {
      nik: "",
      full_name: "",
      phone_number: "",
      address: "",
      branch_id: "",
    };
  }
  isModalOpen.value = true;
};
const closeModal = () => (isModalOpen.value = false);

const handleSubmit = async () => {
  try {
    if (isEditMode.value)
      await api.put(`/master/customers/${currentId.value}`, form.value);
    else await api.post("/master/customers", form.value);
    closeModal();
    fetchData();
  } catch (e) {
    alert(e.response?.data?.message || "Gagal menyimpan data.");
  }
};

const deleteCustomer = async (id) => {
  if (confirm("Apakah Anda yakin ingin menghapus pelanggan ini?")) {
    try {
      await api.delete(`/master/customers/${id}`);
      fetchData();
    } catch (e) {
      alert("Gagal menghapus pelanggan.");
    }
  }
};
</script>
