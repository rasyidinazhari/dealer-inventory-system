<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <div
      class="flex flex-col items-start justify-between gap-4 mb-6 sm:flex-row sm:items-center"
    >
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Profil Saya</h1>
        <p class="mt-1 text-sm text-gray-500">
          Kelola informasi pribadi, kontak, dan keamanan akun Anda.
        </p>
      </div>
    </div>

    <div v-if="isLoading" class="py-12 text-center text-gray-500 animate-pulse">
      Memuat data profil...
    </div>

    <form v-else @submit.prevent="handleUpdateProfile" class="space-y-6">
      <!-- KOTAK 1: INFORMASI PRIBADI -->
      <div class="p-6 bg-white border border-gray-200 shadow-sm rounded-xl">
        <h3 class="mb-5 text-lg font-bold text-gray-900 border-b pb-3">
          Informasi Pribadi
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-semibold text-gray-700"
              >Username</label
            >
            <input
              :value="form.username"
              type="text"
              disabled
              class="block w-full px-3 py-2 mt-1 text-gray-500 bg-gray-100 border border-gray-300 rounded-md sm:text-sm cursor-not-allowed"
            />
            <p class="mt-1 text-xs text-gray-400">
              *Username tidak dapat diubah.
            </p>
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700"
              >Pilih Cabang Penitipan</label
            >
            <select
              v-model="form.branch_id"
              required
              class="block w-full px-3 py-2 mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm cursor-pointer"
            >
              <option value="" disabled>-- Pilih Cabang Terdekat --</option>
              <option v-for="b in branches" :key="b.id" :value="b.id">
                {{ b.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700"
              >Nama Lengkap</label
            >
            <input
              v-model="form.full_name"
              type="text"
              required
              placeholder="Contoh: Budi Santoso"
              class="block w-full px-3 py-2 mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700"
              >Nomor WhatsApp</label
            >
            <input
              v-model="form.phone_number"
              type="text"
              required
              placeholder="Contoh: 08123456789"
              class="block w-full px-3 py-2 mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
        </div>
      </div>

      <!-- KOTAK 2: KEAMANAN (GANTI PASSWORD) -->
      <div class="p-6 bg-white border border-gray-200 shadow-sm rounded-xl">
        <h3
          class="mb-5 text-lg font-bold text-gray-900 border-b pb-3 flex items-center gap-2"
        >
          <svg
            class="w-5 h-5 text-gray-500"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
            ></path>
          </svg>
          Keamanan & Kata Sandi
        </h3>

        <p class="text-sm text-gray-500 mb-4">
          Biarkan kosong jika Anda tidak ingin mengubah kata sandi.
        </p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="md:col-span-2">
            <label class="block text-sm font-semibold text-gray-700"
              >Kata Sandi Lama</label
            >
            <input
              v-model="passwords.old_password"
              type="password"
              placeholder="••••••••"
              class="block w-full md:w-1/2 px-3 py-2 mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700"
              >Kata Sandi Baru</label
            >
            <input
              v-model="passwords.new_password"
              type="password"
              placeholder="••••••••"
              class="block w-full px-3 py-2 mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700"
              >Konfirmasi Kata Sandi Baru</label
            >
            <input
              v-model="passwords.confirm_password"
              type="password"
              placeholder="••••••••"
              class="block w-full px-3 py-2 mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              :class="{
                'border-red-500 focus:border-red-500 focus:ring-red-500':
                  passwordMismatch,
              }"
            />
            <p
              v-if="passwordMismatch"
              class="mt-1 text-xs font-bold text-red-500"
            >
              Kata sandi baru tidak cocok!
            </p>
          </div>
        </div>
      </div>

      <div class="flex justify-end gap-3 pt-2">
        <button
          type="submit"
          :disabled="isSaving || passwordMismatch"
          class="px-6 py-3 text-sm font-bold text-white transition-colors bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700 disabled:opacity-50"
        >
          {{ isSaving ? "Menyimpan..." : "Simpan Perubahan" }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import api from "../../services/api";

const isLoading = ref(true);
const isSaving = ref(false);
const branches = ref([]);

const form = ref({
  username: "",
  full_name: "",
  phone_number: "",
  branch_id: "",
});

const passwords = ref({
  old_password: "",
  new_password: "",
  confirm_password: "",
});

const passwordMismatch = computed(() => {
  if (passwords.value.new_password || passwords.value.confirm_password) {
    return passwords.value.new_password !== passwords.value.confirm_password;
  }
  return false;
});

const fetchInitialData = async () => {
  isLoading.value = true;
  try {
    const [profileRes, branchRes] = await Promise.all([
      api.get("/users/profile"),
      api.get("/master/branches"),
    ]);

    form.value = {
      username: profileRes.data.data.username,
      full_name: profileRes.data.data.full_name,
      phone_number: profileRes.data.data.phone_number,
      branch_id: profileRes.data.data.branch_id,
    };
    branches.value = branchRes.data.data;
  } catch (error) {
    alert("Gagal memuat data profil");
  } finally {
    isLoading.value = false;
  }
};

const handleUpdateProfile = async () => {
  // Validasi jika user mengisi password baru tapi tidak mengisi password lama
  if (passwords.value.new_password && !passwords.value.old_password) {
    alert(
      "Silakan masukkan Kata Sandi Lama Anda untuk memverifikasi perubahan.",
    );
    return;
  }

  isSaving.value = true;
  try {
    const payload = {
      full_name: form.value.full_name,
      phone_number: form.value.phone_number,
      branch_id: form.value.branch_id,
    };

    if (passwords.value.old_password && passwords.value.new_password) {
      payload.old_password = passwords.value.old_password;
      payload.new_password = passwords.value.new_password;
    }

    const response = await api.put("/users/profile", payload);

    // Update nama di local storage agar UI sidebar ikut update (opsional)
    const userData = JSON.parse(localStorage.getItem("user_data"));
    userData.full_name = payload.full_name;
    localStorage.setItem("user_data", JSON.stringify(userData));

    alert(response.data.message);

    // Reset form password
    passwords.value = {
      old_password: "",
      new_password: "",
      confirm_password: "",
    };

    // Paksa reload halaman agar nama profil di sidebar ter-update otomatis
    window.location.reload();
  } catch (error) {
    alert(error.response?.data?.message || "Gagal memperbarui profil");
  } finally {
    isSaving.value = false;
  }
};

onMounted(() => {
  fetchInitialData();
});
</script>
