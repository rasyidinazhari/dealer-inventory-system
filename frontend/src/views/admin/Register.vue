<template>
  <div
    class="flex items-center justify-center min-h-screen px-4 bg-gray-50 sm:px-6 lg:px-8"
  >
    <div
      class="w-full max-w-md p-8 space-y-8 bg-white border border-gray-100 shadow-lg rounded-2xl"
    >
      <div class="text-center">
        <h2 class="text-3xl font-extrabold text-gray-900">Daftar Akun</h2>
        <p class="mt-2 text-sm text-gray-600">
          Buat akun untuk menyimpan Wishlist dan mulai berjualan!
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="space-y-4 rounded-md shadow-sm">
          <div>
            <label class="block text-sm font-medium text-gray-700"
              >Nama Lengkap</label
            >
            <input
              v-model="form.full_name"
              type="text"
              required
              class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700"
              >Nomor WhatsApp</label
            >
            <input
              v-model="form.phone_number"
              type="text"
              required
              class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700"
              >Username</label
            >
            <input
              v-model="form.username"
              type="text"
              required
              class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
          <!-- Pilihan Cabang -->
          <div class="mt-4">
            <label class="block text-sm font-medium text-gray-700"
              >Pilih Cabang (Lokasi Titip Jual)</label
            >
            <select
              v-model="form.branch_id"
              required
              class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value="" disabled>-- Pilih Cabang Terdekat --</option>
              <option
                v-for="branch in branches"
                :key="branch.id"
                :value="branch.id"
              >
                {{ branch.name }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700"
              >Password</label
            >
            <input
              v-model="form.password"
              type="password"
              required
              class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="isLoading"
            class="flex justify-center w-full px-4 py-3 text-sm font-medium text-white transition-colors bg-blue-600 border border-transparent rounded-lg shadow-sm hover:bg-blue-700 disabled:opacity-50"
          >
            {{ isLoading ? "Mendaftarkan..." : "Daftar Sekarang" }}
          </button>
        </div>
      </form>

      <div class="text-center">
        <p class="text-sm text-gray-600">
          Sudah punya akun?
          <router-link
            to="/login"
            class="font-medium text-blue-600 hover:text-blue-500"
            >Masuk di sini</router-link
          >
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../../services/api"; // Sesuaikan path

const router = useRouter();
const isLoading = ref(false);
const form = ref({
  username: "",
  password: "",
  role: "seller",
  branch_id: "",
  full_name: "", // Pastikan ini ada
  phone_number: "", // Pastikan ini ada
});

const branches = ref([]);

onMounted(async () => {
  try {
    const response = await api.get("/master/branches");
    branches.value = response.data.data;
  } catch (error) {
    console.error("Gagal memuat cabang:", error);
  }
});

const handleRegister = async () => {
  isLoading.value = true;
  try {
    await api.post("/auth/register", form.value);
    alert("Registrasi berhasil! Silakan login dengan akun Anda.");
    router.push("/login");
  } catch (error) {
    alert(error.response?.data?.message || "Gagal melakukan registrasi.");
  } finally {
    isLoading.value = false;
  }
};
</script>
