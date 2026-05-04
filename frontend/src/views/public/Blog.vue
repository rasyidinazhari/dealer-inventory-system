<template>
  <PublicNavbar />
  <div class="bg-white min-h-screen pt-24 pb-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h1
          class="text-4xl font-extrabold text-gray-900 tracking-tight sm:text-5xl"
        >
          Blog Abu Motor
        </h1>
        <p class="mt-4 max-w-2xl mx-auto text-xl text-gray-500">
          Wawasan, tips perawatan, dan berita terbaru dari dunia otomotif roda
          dua.
        </p>
      </div>

      <div v-if="isLoading" class="flex justify-center py-20">
        <div class="animate-pulse text-gray-400 font-medium">
          Memuat artikel...
        </div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
        <article
          v-for="article in articles"
          :key="article.id"
          class="flex flex-col bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg transition-all duration-300"
        >
          <router-link :to="`/blog/${article.slug}`" class="block shrink-0">
            <img
              v-if="article.image_url"
              :src="getImageUrl(article.image_url)"
              class="w-full h-56 object-cover"
              :alt="article.title"
            />
            <div
              v-else
              class="w-full h-56 bg-gray-100 flex items-center justify-center"
            >
              <svg
                class="w-12 h-12 text-gray-300"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                ></path>
              </svg>
            </div>
          </router-link>
          <div class="flex-1 p-6 flex flex-col justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-blue-600 mb-2">
                {{ article.created_at }}
              </p>
              <router-link :to="`/blog/${article.slug}`" class="block mt-2">
                <h3 class="text-xl font-bold text-gray-900 hover:underline">
                  {{ article.title }}
                </h3>
                <p class="mt-3 text-base text-gray-500 line-clamp-3">
                  {{ article.content }}
                </p>
              </router-link>
            </div>
            <div class="mt-6 flex items-center">
              <div class="flex-shrink-0">
                <div
                  class="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold uppercase"
                >
                  {{ (article.author_name || "Admin").charAt(0) }}
                </div>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-gray-900">
                  {{ article.author_name || "Admin" }}
                </p>
                <p class="text-sm text-gray-500">Penulis</p>
              </div>
            </div>
          </div>
        </article>
      </div>
    </div>
  </div>
  <PublicFooter />
</template>

<script setup>
import { ref, onMounted } from "vue";
import api, { BASE_URL } from "../../services/api";
import PublicNavbar from "../../components/PublicNavbar.vue";
import PublicFooter from "../../components/PublicFooter.vue";

const articles = ref([]);
const isLoading = ref(true);

const getImageUrl = (url) => (url ? `${BASE_URL}${url}` : null);

onMounted(async () => {
  try {
    const res = await api.get("/articles/public?limit=50"); // Ambil banyak untuk halaman blog
    articles.value = res.data.data;
  } catch (err) {
    console.error(err);
  } finally {
    isLoading.value = false;
  }
});
</script>
