<template>
  <nav class="sticky top-0 z-50 bg-white border-b border-gray-100 shadow-sm">
    <div class="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
      <!-- HEADER UTAMA (Selalu Tampil) -->
      <div class="flex items-center justify-between h-16 gap-4">
        <!-- Logo -->
        <router-link to="/" class="flex items-center shrink-0">
          <img
            src="/abumotor-logo.png"
            alt="Abu Motor Logo"
            class="w-20 md:w-24"
          />
        </router-link>

        <!-- Search Bar (Pindah ke luar agar tampil di mobile & desktop) -->
        <form
          @submit.prevent="handleSearch"
          class="relative flex-1 max-w-lg md:mx-auto"
        >
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Cari kendaraan..."
            class="w-full py-2 pl-4 pr-10 text-sm transition-all border border-gray-300 rounded-full focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 bg-gray-50 md:bg-white"
          />
          <button
            type="submit"
            class="absolute text-gray-400 right-3 top-1/2 -translate-y-1/2 hover:text-blue-600"
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
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              ></path>
            </svg>
          </button>
        </form>

        <!-- Menu Desktop (Link Kanan) -->
        <div class="hidden gap-6 md:flex shrink-0 items-center">
          <div class="flex items-center gap-5 mr-4">
            <router-link
              to="/"
              class="text-sm font-medium text-gray-600 transition-colors hover:text-blue-600"
              exact-active-class="font-bold text-blue-600"
              >Home</router-link
            >
            <router-link
              to="/katalog"
              class="text-sm font-medium text-gray-600 transition-colors hover:text-blue-600"
              active-class="font-bold text-blue-600"
              >Katalog</router-link
            >
            <router-link
              to="/blog"
              class="text-sm font-medium text-gray-600 transition-colors hover:text-blue-600"
              active-class="font-bold text-blue-600"
              >Blog</router-link
            >
            <router-link
              to="/kontak"
              class="text-sm font-medium text-gray-600 transition-colors hover:text-blue-600"
              active-class="font-bold text-blue-600"
              >Kontak</router-link
            >
          </div>

          <a
            :href="waLinkGeneral"
            target="_blank"
            class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white transition-colors bg-green-500 rounded-lg shadow-sm hover:bg-green-600"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path
                d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 00-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .1 5.392.1 11.947c0 2.096.546 4.142 1.584 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.945-5.393 11.945-11.95a11.813 11.813 0 00-3.53-8.406z"
              />
            </svg>
            Konsultasi
          </a>

          <!-- TOMBOL LOGIN / DASHBOARD DESKTOP -->
          <router-link
            v-if="!isLoggedIn"
            to="/login"
            class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 transition-colors bg-gray-100 rounded-lg hover:text-blue-600 hover:bg-gray-200"
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
                d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"
              ></path>
            </svg>
            Login
          </router-link>
          <router-link
            v-else
            :to="dashboardRoute"
            class="flex items-center gap-2 px-3 py-1.5 transition-colors border border-blue-200 bg-blue-50 rounded-full hover:bg-blue-100 group"
          >
            <div
              class="flex items-center justify-center font-bold text-white bg-blue-600 rounded-full w-7 h-7"
            >
              {{
                currentUser.username
                  ? currentUser.username.charAt(0).toUpperCase()
                  : "U"
              }}
            </div>
            <div class="flex flex-col pr-2 text-left">
              <span
                class="text-xs font-bold leading-tight text-blue-900 group-hover:text-blue-700"
                >{{ currentUser.username }}</span
              >
              <span
                class="text-[9px] font-medium leading-tight text-blue-500 uppercase"
                >Dasbor</span
              >
            </div>
          </router-link>
        </div>

        <!-- Tombol Hamburger Mobile -->
        <div class="flex items-center md:hidden shrink-0">
          <button
            @click="isMobileMenuOpen = !isMobileMenuOpen"
            class="p-2 text-gray-600 hover:text-gray-900 focus:outline-none"
          >
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                v-if="!isMobileMenuOpen"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              ></path>
              <path
                v-else
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

    <!-- MOBILE MENU DROPDOWN -->
    <transition name="fade">
      <div
        v-if="isMobileMenuOpen"
        class="absolute left-0 w-full bg-white border-b border-gray-100 shadow-lg md:hidden top-16"
      >
        <div class="px-4 pt-2 pb-6 space-y-2">
          <!-- Search dihapus dari sini karena sudah ditaruh di luar -->
          <router-link
            to="/"
            @click="isMobileMenuOpen = false"
            class="block px-4 py-3 text-base font-medium text-gray-700 rounded-lg hover:bg-blue-50 hover:text-blue-600"
            >Home</router-link
          >
          <router-link
            to="/katalog"
            @click="isMobileMenuOpen = false"
            class="block px-4 py-3 text-base font-medium text-gray-700 rounded-lg hover:bg-blue-50 hover:text-blue-600"
            >Katalog</router-link
          >
          <router-link
            to="/blog"
            @click="isMobileMenuOpen = false"
            class="block px-4 py-3 text-base font-medium text-gray-700 rounded-lg hover:bg-blue-50 hover:text-blue-600"
            >Blog</router-link
          >
          <router-link
            to="/kontak"
            @click="isMobileMenuOpen = false"
            class="block px-4 py-3 text-base font-medium text-gray-700 rounded-lg hover:bg-blue-50 hover:text-blue-600"
            >Kontak</router-link
          >

          <div class="flex flex-col gap-2 pt-4 mt-2 border-t border-gray-100">
            <a
              :href="waLinkGeneral"
              target="_blank"
              class="flex items-center justify-center w-full gap-2 px-4 py-3 text-base font-medium text-white bg-green-500 rounded-lg hover:bg-green-600"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path
                  d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 00-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .1 5.392.1 11.947c0 2.096.546 4.142 1.584 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.945-5.393 11.945-11.95a11.813 11.813 0 00-3.53-8.406z"
                />
              </svg>
              Konsultasi Langsung
            </a>

            <!-- TOMBOL LOGIN / DASHBOARD MOBILE -->
            <router-link
              v-if="!isLoggedIn"
              to="/login"
              @click="isMobileMenuOpen = false"
              class="flex items-center justify-center w-full gap-2 px-4 py-3 text-base font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
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
                  d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"
                ></path>
              </svg>
              Login
            </router-link>
            <router-link
              v-else
              :to="dashboardRoute"
              @click="isMobileMenuOpen = false"
              class="flex items-center justify-center w-full gap-3 px-4 py-3 text-base font-bold text-blue-700 border border-blue-200 bg-blue-50 rounded-lg hover:bg-blue-100"
            >
              <div
                class="flex items-center justify-center text-sm font-bold text-white bg-blue-600 rounded-full w-6 h-6"
              >
                {{
                  currentUser.username
                    ? currentUser.username.charAt(0).toUpperCase()
                    : "U"
                }}
              </div>
              Buka Dasbor
            </router-link>
          </div>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const isMobileMenuOpen = ref(false);
const searchQuery = ref("");
const DEALER_WA_NUMBER = "6281222444951";

// === STATE SESI LOGIN ===
const isLoggedIn = ref(false);
const currentUser = ref({});

onMounted(() => {
  const token = localStorage.getItem("access_token");
  const userDataString = localStorage.getItem("user_data");

  if (token && userDataString) {
    isLoggedIn.value = true;
    currentUser.value = JSON.parse(userDataString);
  }
});

const dashboardRoute = computed(() => {
  if (!isLoggedIn.value) return "/login";
  return currentUser.value.role === "seller"
    ? "/admin/seller-dashboard"
    : "/admin/inventory";
});

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push(`/katalog?q=${encodeURIComponent(searchQuery.value.trim())}`);
    searchQuery.value = "";
    isMobileMenuOpen.value = false;
  }
};

const waLinkGeneral = computed(() => {
  const text = encodeURIComponent(
    "Halo Abu Motor, saya melihat website Anda dan ingin bertanya mengenai promo dan pembelian kendaraan.",
  );
  return `https://wa.me/${DEALER_WA_NUMBER}?text=${text}`;
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
