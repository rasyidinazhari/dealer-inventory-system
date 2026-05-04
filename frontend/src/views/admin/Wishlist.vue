<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Wishlist Saya</h1>
        <p class="mt-1 text-sm text-gray-500">
          Daftar kendaraan yang Anda simpan untuk dibeli atau ditawarkan.
        </p>
      </div>
    </div>

    <div v-if="isLoading" class="flex justify-center py-12">
      <div class="animate-pulse text-gray-500 font-medium">
        Memuat wishlist...
      </div>
    </div>

    <div
      v-else-if="wishlists.length === 0"
      class="py-20 text-center bg-white border border-dashed border-gray-300 rounded-2xl"
    >
      <svg
        class="w-16 h-16 mx-auto mb-4 text-gray-300"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
        ></path>
      </svg>
      <h3 class="text-lg font-bold text-gray-900">
        Wishlist Anda Masih Kosong
      </h3>
      <p class="mt-2 text-gray-500">
        Jelajahi katalog kami dan simpan kendaraan impian Anda di sini.
      </p>
      <router-link
        to="/katalog"
        class="inline-block px-6 py-2.5 mt-6 font-bold text-white transition-colors bg-blue-600 rounded-lg hover:bg-blue-700"
        >Lihat Katalog</router-link
      >
    </div>

    <div
      v-else
      class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
    >
      <div
        v-for="item in wishlists"
        :key="item.wishlist_id"
        class="flex flex-col overflow-hidden transition-all duration-300 bg-white border border-gray-200 shadow-sm rounded-2xl hover:shadow-lg group"
      >
        <router-link
          :to="`/motor/${item.motorcycle_id}`"
          class="relative flex items-center justify-center h-48 overflow-hidden bg-gray-50 border-b border-gray-100"
        >
          <img
            v-if="item.image_url"
            :src="getImageUrl(item.image_url)"
            class="object-cover w-full h-full transition-transform duration-500 group-hover:scale-105"
          />
          <span
            class="absolute top-3 right-3 bg-white/90 backdrop-blur-sm px-2.5 py-1 rounded-md text-xs font-bold text-gray-800 uppercase tracking-wide"
            >{{ item.brand }}</span
          >
          <span
            v-if="item.stock === 0"
            class="absolute inset-0 flex items-center justify-center bg-black/50 text-white font-bold text-lg backdrop-blur-sm"
            >STOK HABIS</span
          >
        </router-link>

        <div class="flex flex-col flex-1 p-5">
          <h3
            class="mb-1 text-lg font-bold leading-tight text-gray-900 line-clamp-2"
          >
            {{ item.model_name }}
          </h3>
          <p class="mb-4 text-sm text-gray-500">
            Disimpan pada: {{ item.added_at.split(" ")[0] }}
          </p>
          <div class="mt-auto">
            <p class="text-xl font-black text-blue-600">
              {{ formatCurrency(item.price) }}
            </p>
          </div>
        </div>

        <div class="flex gap-2 px-5 pb-5">
          <button
            @click="removeWishlist(item.motorcycle_id)"
            class="flex items-center justify-center p-2.5 text-red-500 transition-colors bg-red-50 rounded-xl hover:bg-red-100 border border-red-100"
            title="Hapus dari Wishlist"
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
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              ></path>
            </svg>
          </button>
          <a
            :href="getWaLink(item)"
            target="_blank"
            class="flex-1 flex items-center justify-center gap-2 bg-gray-900 hover:bg-gray-800 text-white py-2.5 rounded-xl text-sm font-semibold transition-colors"
          >
            Tanya CS
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api, { BASE_URL } from "../../services/api";

const wishlists = ref([]);
const isLoading = ref(true);
const DEALER_WA_NUMBER = "6281222444951";

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

const getWaLink = (item) => {
  return `https://wa.me/${DEALER_WA_NUMBER}?text=${encodeURIComponent(`Halo CS Abu Motor, saya tertarik dengan kendaraan dari wishlist saya: *${item.brand} ${item.model_name}* (Harga: ${formatCurrency(item.price)}). Apakah masih tersedia?`)}`;
};

const fetchWishlists = async () => {
  isLoading.value = true;
  try {
    const res = await api.get("/wishlist/");
    wishlists.value = res.data.data;
  } catch (error) {
    console.error("Gagal mengambil wishlist", error);
  } finally {
    isLoading.value = false;
  }
};

const removeWishlist = async (motorId) => {
  if (!confirm("Hapus kendaraan ini dari wishlist Anda?")) return;
  try {
    await api.post("/wishlist/toggle", { motorcycle_id: motorId });
    fetchWishlists(); // Refresh list setelah dihapus
  } catch (error) {
    alert("Gagal menghapus wishlist.");
  }
};

onMounted(() => {
  fetchWishlists();
});
</script>
