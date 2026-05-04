<template>
  <div>
    <!-- HEADER & PENCARIAN -->
    <div
      class="flex flex-col items-start justify-between gap-4 mb-6 sm:flex-row sm:items-center"
    >
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Manajemen Akun (Users)</h1>
        <p class="mt-1 text-sm text-gray-500">
          Kelola akses login untuk karyawan dan divisi.
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
            placeholder="Cari username..."
            class="block w-full py-2 pl-10 pr-3 leading-5 placeholder-gray-500 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>
        <button
          @click="openModal()"
          class="flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg shadow-sm hover:bg-indigo-700 shrink-0"
        >
          <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
            <path
              fill-rule="evenodd"
              d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
              clip-rule="evenodd"
            />
          </svg>
          Tambah Akun
        </button>
      </div>
    </div>

    <!-- TABEL USERS -->
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
                Username
              </th>
              <th
                class="px-6 py-3 text-xs font-semibold text-left text-gray-500 uppercase"
              >
                Role / Divisi
              </th>
              <th
                class="px-6 py-3 text-xs font-semibold text-left text-gray-500 uppercase"
              >
                Tgl Terdaftar
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
            <tr v-else-if="filteredUsers.length === 0" class="text-center">
              <td colspan="4" class="px-6 py-8 text-sm text-gray-500">
                Tidak ada user yang cocok.
              </td>
            </tr>
            <tr
              v-else
              v-for="user in filteredUsers"
              :key="user.id"
              class="hover:bg-gray-50"
            >
              <td
                class="px-6 py-4 text-sm font-bold text-gray-900 whitespace-nowrap"
              >
                <div class="flex items-center gap-3">
                  <div
                    class="flex items-center justify-center w-8 h-8 font-bold text-gray-600 uppercase bg-gray-200 rounded-full"
                  >
                    {{ user.username.charAt(0) }}
                  </div>
                  {{ user.username }}
                </div>
              </td>
              <!-- ROLE DAN CABANG -->
              <td class="px-6 py-4 text-sm whitespace-nowrap">
                <div class="flex flex-col items-start gap-1">
                  <!-- BADGE ROLE -->
                  <span
                    v-if="user.role === 'super_admin'"
                    class="px-2.5 py-1 bg-purple-100 text-purple-800 text-xs font-bold rounded-full"
                    >Super Admin</span
                  >
                  <span
                    v-else-if="user.role === 'admin_cabang'"
                    class="px-2.5 py-1 bg-indigo-100 text-indigo-800 text-xs font-bold rounded-full"
                    >Admin Cabang</span
                  >
                  <span
                    v-else-if="user.role === 'finance'"
                    class="px-2.5 py-1 bg-green-100 text-green-800 text-xs font-bold rounded-full"
                    >Finance</span
                  >
                  <span
                    v-else-if="user.role === 'cs'"
                    class="px-2.5 py-1 bg-blue-100 text-blue-800 text-xs font-bold rounded-full"
                    >CS / Kasir</span
                  >
                  <span
                    v-else
                    class="px-2.5 py-1 bg-gray-100 text-gray-800 text-xs font-bold rounded-full capitalize"
                    >{{ user.role }}</span
                  >

                  <!-- NAMA CABANG (Jika bukan Super Admin / Seller) -->
                  <span
                    v-if="user.branch_id && user.role !== 'super_admin'"
                    class="text-xs text-gray-500 font-medium ml-1"
                  >
                    📍 {{ getBranchName(user.branch_id) }}
                  </span>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500 whitespace-nowrap">
                {{ formatDate(user.created_at) }}
              </td>
              <td
                class="px-6 py-4 text-sm font-medium text-right whitespace-nowrap"
              >
                <button
                  @click="openModal(user)"
                  class="mr-3 text-blue-600 hover:text-blue-900 transition-colors"
                >
                  Edit
                </button>
                <button
                  @click="deleteUser(user.id)"
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
      <div class="flex items-center justify-center min-h-screen px-4">
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          @click="closeModal"
        ></div>
        <div
          class="relative w-full max-w-md p-6 bg-white shadow-xl rounded-xl transition-all"
        >
          <h3 class="mb-4 text-lg font-bold text-gray-900 border-b pb-2">
            {{ isEditMode ? "Edit Akun" : "Tambah Akun Baru" }}
          </h3>
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700"
                >Username</label
              >
              <input
                v-model="form.username"
                required
                type="text"
                class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 bg-gray-50"
                :disabled="isEditMode"
              />
              <p v-if="isEditMode" class="mt-1 text-xs text-gray-500 italic">
                *Username tidak dapat diubah setelah dibuat.
              </p>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700"
                >Password</label
              >
              <input
                v-model="form.password"
                :required="!isEditMode"
                type="password"
                placeholder="••••••••"
                class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
              />
              <p v-if="isEditMode" class="mt-1 text-xs text-gray-500 italic">
                *Kosongkan jika tidak ingin mengubah password.
              </p>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700"
                >Hak Akses (Role)</label
              >
              <select
                v-model="form.role"
                required
                @change="handleRoleChange"
                class="w-full px-3 py-2 mt-1 bg-white border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 font-medium"
              >
                <option value="cs">Customer Service (Kasir)</option>
                <option value="finance">Finance</option>
                <option value="admin_cabang">Admin Cabang</option>
                <option value="super_admin">Super Admin (Pusat)</option>
                <option value="seller">Seller (Eksternal)</option>
              </select>
            </div>

            <!-- PILIHAN CABANG MUNCUL DINAMIS -->
            <div
              v-if="
                ['cs', 'finance', 'admin_cabang', 'seller'].includes(form.role)
              "
              class="p-3 bg-indigo-50 border border-indigo-100 rounded-lg"
            >
              <label class="block text-sm font-bold text-indigo-900"
                >Penempatan Cabang</label
              >
              <select
                v-model="form.branch_id"
                required
                class="w-full px-3 py-2 mt-1 bg-white border border-indigo-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="" disabled>-- Pilih Cabang --</option>
                <option
                  v-for="branch in masterBranches"
                  :key="branch.id"
                  :value="branch.id"
                >
                  {{ branch.name }}
                </option>
              </select>
              <p class="mt-1 text-xs text-indigo-700">
                Karyawan ini hanya bisa mengelola data di cabang yang dipilih.
              </p>
            </div>
            <!-- FORM KHUSUS SELLER (Nama & Kontak) -->
            <div
              v-if="form.role === 'seller'"
              class="p-3 mt-4 bg-green-50 border border-green-200 rounded-lg space-y-3"
            >
              <p
                class="text-xs font-bold text-green-800 border-b border-green-200 pb-2 mb-2 uppercase"
              >
                Data Profil Seller
              </p>
              <div>
                <label class="block text-sm font-semibold text-green-900"
                  >Nama Lengkap</label
                >
                <input
                  v-model="form.full_name"
                  type="text"
                  placeholder="Contoh: Budi Santoso"
                  class="w-full px-3 py-2 mt-1 bg-white border border-green-300 rounded-md focus:ring-green-500 focus:border-green-500"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-green-900"
                  >Nomor WhatsApp</label
                >
                <input
                  v-model="form.phone_number"
                  type="text"
                  placeholder="Contoh: 08123456789"
                  class="w-full px-3 py-2 mt-1 bg-white border border-green-300 rounded-md focus:ring-green-500 focus:border-green-500"
                />
              </div>
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
                class="px-5 py-2 text-sm font-bold text-white transition-colors bg-indigo-600 rounded-lg hover:bg-indigo-700 shadow-sm"
              >
                {{ isEditMode ? "Simpan Perubahan" : "Buat Akun" }}
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

const users = ref([]);
const masterBranches = ref([]); // State untuk daftar cabang
const isLoading = ref(false);
const searchQuery = ref("");

const isModalOpen = ref(false);
const isEditMode = ref(false);
const currentId = ref(null);

// Form data
const form = ref({
  username: "",
  password: "",
  role: "cs",
  branch_id: "",
  full_name: "", // Tambahan
  phone_number: "", // Tambahan
});

// Pencarian real-time
const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value;
  const q = searchQuery.value.toLowerCase();
  return users.value.filter(
    (u) =>
      u.username.toLowerCase().includes(q) || u.role.toLowerCase().includes(q),
  );
});

// Format Tanggal
const formatDate = (dateString) => {
  if (!dateString) return "-";
  const date = new Date(dateString);
  return date.toLocaleDateString("id-ID", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

// Fungsi helper untuk mendapatkan nama cabang berdasarkan ID
const getBranchName = (branchId) => {
  const branch = masterBranches.value.find((b) => b.id === branchId);
  return branch ? branch.name : "Unknown";
};

// Ambil data users dan branches
const fetchData = async () => {
  isLoading.value = true;
  try {
    // Ambil users dan branches secara bersamaan agar cepat
    const [userRes, branchRes] = await Promise.all([
      api.get("/users/"),
      api.get("/master/branches"),
    ]);
    users.value = userRes.data.data;
    masterBranches.value = branchRes.data.data;
  } catch (e) {
    console.error(e);
    alert("Gagal mengambil data sistem.");
  } finally {
    isLoading.value = false;
  }
};

// Mereset branch_id jika role berubah menjadi Super Admin atau Seller
const handleRoleChange = () => {
  if (form.value.role === "super_admin") {
    form.value.branch_id = ""; // Kosongkan karena mereka tidak terikat cabang spesifik
  }
};

const openModal = (item = null) => {
  if (item) {
    isEditMode.value = true;
    currentId.value = item.id;
    form.value = {
      username: item.username,
      password: "",
      role: item.role,
      branch_id: item.branch_id || "",
      full_name: item.full_name || "", // Ambil dari data lama
      phone_number: item.phone_number || "", // Ambil dari data lama
    };
  } else {
    isEditMode.value = false;
    currentId.value = null;
    form.value = {
      username: "",
      password: "",
      role: "cs",
      branch_id: "",
      full_name: "", // Kosongkan
      phone_number: "", // Kosongkan
    };
  }
  isModalOpen.value = true;
};

const closeModal = () => (isModalOpen.value = false);

const handleSubmit = async () => {
  try {
    const payload = { ...form.value };

    // Hapus password dari payload jika sedang edit dan tidak diisi
    if (isEditMode.value && !payload.password) {
      delete payload.password;
    }

    // Pastikan branch_id dikirim sebagai angka (jika ada)
    if (payload.branch_id) {
      payload.branch_id = parseInt(payload.branch_id);
    } else {
      payload.branch_id = null; // Kirim null jika role-nya Super Admin/Seller
    }

    if (isEditMode.value) {
      await api.put(`/users/${currentId.value}`, payload);
    } else {
      await api.post("/users/", payload);
    }

    closeModal();
    fetchData(); // Refresh data
  } catch (e) {
    alert(e.response?.data?.message || "Gagal menyimpan data akun.");
  }
};

const deleteUser = async (id) => {
  const currentUser = JSON.parse(localStorage.getItem("user_data"));
  if (id === currentUser.id) {
    alert("Anda tidak bisa menghapus akun Anda sendiri yang sedang aktif!");
    return;
  }

  if (confirm("Apakah Anda yakin ingin menghapus akses akun ini?")) {
    try {
      await api.delete(`/users/${id}`);
      fetchData();
    } catch (e) {
      alert("Gagal menghapus user.");
    }
  }
};

onMounted(() => {
  fetchData();
});
</script>
