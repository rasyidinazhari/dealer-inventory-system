<template>
  <div class="flex items-center justify-center min-h-screen p-4 bg-gray-50">
    <div
      class="w-full max-w-md p-8 bg-white border border-gray-100 shadow-sm rounded-2xl"
    >
      <div class="mb-8 text-center">
        <h1 class="mb-2 text-2xl font-bold text-gray-900">Login Sistem</h1>
        <p class="text-sm text-gray-500">Silakan masuk dengan akun anda</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div
          v-if="errorMessage"
          class="p-3 text-sm text-center text-red-600 border border-red-100 rounded-lg bg-red-50"
        >
          {{ errorMessage }}
        </div>

        <div>
          <label
            for="username"
            class="block mb-2 text-sm font-medium text-gray-700"
            >Username</label
          >
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
            placeholder="Masukkan username"
            :disabled="isLoading"
          />
        </div>

        <div>
          <label
            for="password"
            class="block mb-2 text-sm font-medium text-gray-700"
            >Password</label
          >
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
            placeholder="••••••••"
            :disabled="isLoading"
          />
        </div>

        <button
          type="submit"
          :disabled="isLoading"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg transition-colors flex justify-center items-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
        >
          <span v-if="isLoading">Memproses...</span>
          <span v-else>Masuk ke Dashboard</span>
        </button>
      </form>

      <!-- TAMBAHAN LINK REGISTRASI -->
      <div class="mt-6 text-sm text-center text-gray-600">
        Belum punya akun?
        <router-link
          to="/register"
          class="font-medium text-blue-600 transition-colors hover:text-blue-500"
        >
          Daftar di sini
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import api from "../../services/api";

const router = useRouter();

const form = reactive({
  username: "",
  password: "",
});

const isLoading = ref(false);
const errorMessage = ref("");

const handleLogin = async () => {
  isLoading.value = true;
  errorMessage.value = "";

  try {
    const response = await api.post("/auth/login", {
      username: form.username,
      password: form.password,
    });

    if (response.data.status === "success") {
      const { access_token, user } = response.data.data;

      localStorage.setItem("access_token", access_token);
      localStorage.setItem("user_data", JSON.stringify(user));

      const userRole = user.role;

      // Pengecekan role agar langsung dilempar ke halaman yang tepat
      if (
        userRole === "super_admin" ||
        userRole === "cs" ||
        userRole === "admin_cabang"
      ) {
        router.push({ name: "Inventory" });
      } else if (userRole === "seller") {
        // Otomatis ke panel seller jika dia baru registrasi dan login
        router.push("/admin/seller-dashboard");
      } else if (userRole === "finance") {
        router.push({ name: "Finance" });
      } else {
        router.push("/");
      }
    }
  } catch (error) {
    if (error.response && error.response.data.message) {
      errorMessage.value = error.response.data.message;
    } else {
      errorMessage.value =
        "Terjadi kesalahan pada server. Pastikan backend menyala.";
    }
  } finally {
    isLoading.value = false;
  }
};
</script>
