<template>
  <PublicNavbar />
  <div class="min-h-screen pb-16 bg-gray-50 pt-24">
    <div
      v-if="isLoading"
      class="max-w-3xl px-4 py-20 mx-auto text-center sm:px-6 lg:px-8 animate-pulse"
    >
      <div class="w-3/4 h-8 mx-auto mb-4 bg-gray-200 rounded"></div>
      <div class="w-1/2 h-4 mx-auto bg-gray-200 rounded"></div>
      <div class="w-full h-64 mt-10 bg-gray-200 rounded-2xl"></div>
    </div>

    <div
      v-else-if="!article"
      class="max-w-3xl px-4 py-20 mx-auto text-center sm:px-6 lg:px-8"
    >
      <h2 class="text-2xl font-bold text-gray-900">Artikel tidak ditemukan</h2>
      <p class="mt-2 text-gray-500">
        Mungkin artikel ini sudah dihapus atau URL-nya salah.
      </p>
      <router-link
        to="/blog"
        class="inline-block px-6 py-2 mt-6 font-medium text-white transition-colors bg-blue-600 rounded-lg hover:bg-blue-700"
        >Kembali ke Blog</router-link
      >
    </div>

    <div v-else class="max-w-4xl px-4 mx-auto sm:px-6 lg:px-8">
      <div class="mb-8">
        <router-link
          to="/blog"
          class="inline-flex items-center gap-2 text-sm font-medium text-gray-500 transition-colors hover:text-blue-600"
        >
          <svg
            class="w-4 h-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M10 19l-7-7m0 0l7-7m-7 7h18"
            ></path>
          </svg>
          Kembali ke Daftar Artikel
        </router-link>
      </div>

      <article
        class="p-6 bg-white border border-gray-100 shadow-sm sm:p-10 rounded-3xl"
      >
        <header class="mb-10 text-center">
          <div
            class="flex items-center justify-center gap-3 mb-4 text-sm font-medium text-gray-500"
          >
            <span class="px-3 py-1 text-blue-700 bg-blue-100 rounded-full">{{
              article.created_at
            }}</span>
            <span>•</span>
            <span class="flex items-center gap-1">
              <svg
                class="w-4 h-4 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
              {{ readingTime }} Menit Baca
            </span>
          </div>

          <h1
            class="text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl md:text-5xl lg:leading-tight"
          >
            {{ article.title }}
          </h1>

          <div class="flex items-center justify-center gap-3 mt-8">
            <div
              class="flex items-center justify-center w-10 h-10 font-bold text-blue-700 uppercase bg-blue-100 rounded-full"
            >
              {{ (article.author_name || "A").charAt(0) }}
            </div>
            <div class="text-left">
              <p class="text-sm font-bold text-gray-900">
                {{ article.author_name || "Admin Abu Motor" }}
              </p>
              <p class="text-xs text-gray-500">Penulis Abu Motor</p>
            </div>
          </div>
        </header>

        <figure
          v-if="article.image_url"
          class="mb-12 overflow-hidden bg-gray-100 shadow-md rounded-2xl"
        >
          <img
            :src="getImageUrl(article.image_url)"
            :alt="article.title"
            class="object-cover w-full h-auto max-h-[500px] hover:scale-105 transition-transform duration-700"
          />
        </figure>

        <div
          class="mx-auto text-gray-700 prose prose-lg prose-blue max-w-none whitespace-pre-line leading-relaxed"
          v-html="article.content"
        ></div>

        <div
          class="py-6 mt-12 border-t border-b border-gray-100 sm:flex sm:items-center sm:justify-between"
        >
          <h3
            class="mb-4 text-sm font-bold text-gray-900 uppercase sm:mb-0 tracking-wider"
          >
            Bagikan Artikel Ini:
          </h3>
          <div class="flex flex-wrap items-center gap-3">
            <button
              @click="shareTo('whatsapp')"
              class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white transition-colors bg-green-500 rounded-lg hover:bg-green-600"
            >
              WhatsApp
            </button>
            <button
              @click="shareTo('facebook')"
              class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white transition-colors bg-blue-600 rounded-lg hover:bg-blue-700"
            >
              Facebook
            </button>
            <button
              @click="shareTo('twitter')"
              class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white transition-colors bg-sky-500 rounded-lg hover:bg-sky-600"
            >
              Twitter
            </button>
            <button
              @click="copyLink"
              class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 transition-colors bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              {{ copied ? "Tersalin!" : "Salin Link" }}
            </button>
          </div>
        </div>
      </article>

      <section v-if="relatedArticles.length > 0" class="mt-16">
        <h3 class="mb-8 text-2xl font-bold text-gray-900">
          Baca Juga Artikel Lainnya
        </h3>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
          <router-link
            v-for="rel in relatedArticles"
            :key="rel.id"
            :to="`/blog/${rel.slug}`"
            class="flex flex-col overflow-hidden transition-all duration-300 bg-white border border-gray-100 shadow-sm rounded-2xl hover:shadow-md group"
          >
            <div class="h-40 overflow-hidden bg-gray-100 relative">
              <img
                v-if="rel.image_url"
                :src="getImageUrl(rel.image_url)"
                class="object-cover w-full h-full transition-transform duration-500 group-hover:scale-105"
              />
            </div>
            <div class="flex flex-col flex-1 p-5">
              <span class="mb-2 text-xs font-semibold text-blue-600">{{
                rel.created_at
              }}</span>
              <h4
                class="text-base font-bold text-gray-900 transition-colors group-hover:text-blue-600 line-clamp-2"
              >
                {{ rel.title }}
              </h4>
            </div>
          </router-link>
        </div>
      </section>
    </div>
  </div>
  <PublicFooter />
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useRoute } from "vue-router";
import api, { BASE_URL } from "../../services/api";
import PublicNavbar from "../../components/PublicNavbar.vue";
import PublicFooter from "../../components/PublicFooter.vue";

const route = useRoute();
const article = ref(null);
const relatedArticles = ref([]);
const isLoading = ref(true);
const copied = ref(false);

const getImageUrl = (url) => {
  if (!url) return null;
  return `${BASE_URL}${url}`;
};

// Menghitung estimasi waktu baca (Asumsi kecepatan baca 200 kata/menit)
const readingTime = computed(() => {
  if (!article.value?.content) return 1;
  const words = article.value.content.trim().split(/\s+/).length;
  return Math.max(1, Math.ceil(words / 200));
});

const fetchArticleData = async (slug) => {
  isLoading.value = true;
  copied.value = false;

  try {
    // 1. Ambil Detail Artikel Utama
    const res = await api.get(`/articles/public/${slug}`);
    article.value = res.data.data;

    // Update Title Browser (SEO Basic)
    document.title = `${article.value.title} | Blog Abu Motor`;

    // 2. Ambil Artikel Terkait (Ambil 4 terbaru, filter agar artikel saat ini tidak muncul)
    const relatedRes = await api.get("/articles/public?limit=4");
    const allRecent = relatedRes.data.data || [];
    relatedArticles.value = allRecent
      .filter((a) => a.id !== article.value.id) // Buang artikel yang sedang dibaca
      .slice(0, 3); // Ambil maksimal 3 saja
  } catch (err) {
    console.error("Gagal memuat detail artikel", err);
    article.value = null;
  } finally {
    isLoading.value = false;
    window.scrollTo({ top: 0, behavior: "smooth" }); // Scroll ke atas saat artikel berganti
  }
};

// Fitur Bagikan Artikel
const shareTo = (platform) => {
  const url = encodeURIComponent(window.location.href);
  const text = encodeURIComponent(
    `Cek artikel menarik ini: ${article.value?.title}`,
  );

  let shareUrl = "";
  if (platform === "whatsapp")
    shareUrl = `https://api.whatsapp.com/send?text=${text} %0A%0A ${url}`;
  if (platform === "facebook")
    shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
  if (platform === "twitter")
    shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${text}`;

  if (shareUrl) window.open(shareUrl, "_blank", "width=600,height=400");
};

const copyLink = () => {
  navigator.clipboard.writeText(window.location.href);
  copied.value = true;
  setTimeout(() => {
    copied.value = false;
  }, 2000);
};

// Pantau perubahan URL (jika pengunjung klik dari "Artikel Terkait")
watch(
  () => route.params.slug,
  (newSlug) => {
    if (newSlug) fetchArticleData(newSlug);
  },
);

onMounted(() => {
  fetchArticleData(route.params.slug);
});
</script>
