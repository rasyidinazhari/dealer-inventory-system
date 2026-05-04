<template>
  <div>
    <div
      class="flex flex-col items-start justify-between gap-4 mb-6 sm:flex-row sm:items-center"
    >
      <div>
        <h1 class="text-2xl font-bold text-gray-900">
          Manajemen Artikel / Blog
        </h1>
        <p class="mt-1 text-sm text-gray-500">
          Tulis artikel SEO-friendly untuk meningkatkan traffic website.
        </p>
      </div>
      <button
        @click="openAddModal"
        class="flex items-center gap-2 px-4 py-2 text-sm font-bold text-white bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700"
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
        Tulis Artikel Baru
      </button>
    </div>

    <div
      class="overflow-hidden bg-white border border-gray-200 shadow-sm rounded-xl"
    >
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Cover & Judul
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Penulis
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-center text-gray-500 uppercase"
              >
                Status
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Tanggal
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-right text-gray-500 uppercase"
              >
                Aksi
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="isLoading">
              <td colspan="5" class="px-6 py-8 text-center text-gray-500">
                Memuat artikel...
              </td>
            </tr>
            <tr v-else-if="articles.length === 0">
              <td colspan="5" class="px-6 py-8 text-center text-gray-500">
                Belum ada artikel.
              </td>
            </tr>
            <tr
              v-else
              v-for="article in articles"
              :key="article.id"
              class="transition-colors hover:bg-gray-50"
            >
              <td class="flex items-center gap-4 px-6 py-4 whitespace-nowrap">
                <img
                  v-if="article.image_url"
                  :src="getImageUrl(article.image_url)"
                  class="object-cover w-16 h-12 rounded-md bg-gray-100"
                  alt="Cover"
                />
                <div
                  v-else
                  class="flex items-center justify-center w-16 h-12 bg-gray-200 rounded-md"
                >
                  <svg
                    class="w-6 h-6 text-gray-400"
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
                <div>
                  <div class="text-sm font-bold text-gray-900 truncate w-48">
                    {{ article.title }}
                  </div>
                  <div class="text-xs text-blue-500">/{{ article.slug }}</div>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-700 whitespace-nowrap">
                {{ article.author_name }}
              </td>
              <td class="px-6 py-4 text-center whitespace-nowrap">
                <span
                  v-if="article.is_published"
                  class="px-2.5 py-1 text-xs font-semibold text-green-800 bg-green-100 rounded-full"
                  >Publik</span
                >
                <span
                  v-else
                  class="px-2.5 py-1 text-xs font-semibold text-gray-800 bg-gray-100 rounded-full"
                  >Draft</span
                >
              </td>
              <td class="px-6 py-4 text-sm text-gray-500 whitespace-nowrap">
                {{ article.created_at }}
              </td>
              <td
                class="px-6 py-4 text-sm font-medium text-right whitespace-nowrap"
              >
                <div class="flex items-center justify-end gap-3">
                  <a
                    :href="`/blog/${article.slug}`"
                    target="_blank"
                    class="text-blue-600 hover:text-blue-900 font-bold"
                    >Lihat</a
                  >
                  <button
                    @click="openEditModal(article)"
                    class="text-amber-500 hover:text-amber-700 font-bold"
                  >
                    Edit
                  </button>
                  <button
                    @click="handleDelete(article.id)"
                    class="text-red-600 hover:text-red-900 font-bold"
                  >
                    Hapus
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 z-50 overflow-y-auto">
      <div
        class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:p-0"
      >
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75"
          @click="closeModal"
        ></div>
        <div
          class="inline-block w-full overflow-hidden text-left align-bottom transition-all transform bg-white shadow-xl rounded-xl sm:my-8 sm:align-middle sm:max-w-3xl"
        >
          <form @submit.prevent="handleSubmit">
            <div
              class="px-4 pt-5 pb-4 bg-white sm:p-6 sm:pb-4 max-h-[80vh] overflow-y-auto"
            >
              <h3 class="pb-3 mb-4 text-xl font-bold text-gray-900 border-b">
                {{ isEditing ? "Edit Artikel" : "Tulis Artikel Baru" }}
              </h3>
              <div class="space-y-4">
                <div>
                  <label class="block mb-1 text-sm font-bold text-gray-700"
                    >Judul Artikel (H1)</label
                  >
                  <input
                    v-model="form.title"
                    type="text"
                    required
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label class="block mb-1 text-sm font-bold text-gray-700"
                    >Gambar Cover / Thumbnail (Opsional)</label
                  >
                  <input
                    type="file"
                    @change="handleFileUpload"
                    accept="image/*"
                    class="block w-full text-sm text-gray-500 border border-gray-300 rounded-md file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                  />
                </div>
                <div>
                  <label class="block mb-1 text-sm font-bold text-gray-700"
                    >Isi Konten Artikel</label
                  >
                  <textarea
                    v-model="form.content"
                    required
                    rows="10"
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    placeholder="Tulis konten blog di sini... (Mendukung paragraf dan spasi)"
                  ></textarea>
                </div>
                <div class="flex items-center gap-2 mt-4">
                  <input
                    v-model="form.is_published"
                    type="checkbox"
                    id="publish"
                    class="w-4 h-4 text-blue-600 rounded"
                  />
                  <label
                    for="publish"
                    class="text-sm font-medium text-gray-700 cursor-pointer"
                    >Langsung Terbitkan ke Publik</label
                  >
                </div>
              </div>
            </div>
            <div
              class="px-4 py-3 bg-gray-50 sm:px-6 sm:flex sm:flex-row-reverse border-t"
            >
              <button
                type="submit"
                :disabled="isSaving"
                class="w-full px-6 py-2 text-sm font-bold text-white bg-blue-600 rounded-lg sm:ml-3 sm:w-auto hover:bg-blue-700 disabled:opacity-50"
              >
                {{ isSaving ? "Menyimpan..." : "Simpan Artikel" }}
              </button>
              <button
                type="button"
                @click="closeModal"
                class="w-full px-6 py-2 mt-3 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg sm:mt-0 sm:w-auto hover:bg-gray-50"
              >
                Batal
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../../services/api";

const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5001";
const articles = ref([]);
const isLoading = ref(true);
const isModalOpen = ref(false);
const isSaving = ref(false);

// State khusus untuk Edit
const isEditing = ref(false);
const editId = ref(null);
const selectedImage = ref(null);

const form = ref({ title: "", content: "", is_published: true });

const getImageUrl = (url) => (url ? `${BASE_URL}${url}` : null);

const fetchArticles = async () => {
  try {
    const res = await api.get("/articles/admin");
    articles.value = res.data.data;
  } catch (err) {
    console.error(err);
  } finally {
    isLoading.value = false;
  }
};

// Fungsi Buka Modal Tambah Baru
const openAddModal = () => {
  isEditing.value = false;
  editId.value = null;
  form.value = { title: "", content: "", is_published: true };
  selectedImage.value = null;
  isModalOpen.value = true;
};

// Fungsi Buka Modal Edit
const openEditModal = (article) => {
  isEditing.value = true;
  editId.value = article.id;
  form.value = {
    title: article.title,
    content: article.content,
    is_published: article.is_published,
  };
  selectedImage.value = null;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const handleFileUpload = (e) => {
  selectedImage.value = e.target.files[0];
};

const handleSubmit = async () => {
  isSaving.value = true;
  try {
    const formData = new FormData();
    formData.append("title", form.value.title);
    formData.append("content", form.value.content);
    formData.append("is_published", form.value.is_published);
    if (selectedImage.value) formData.append("image", selectedImage.value);

    // Jika sedang edit, gunakan PUT ke /articles/:id. Jika tidak, POST ke /articles/
    if (isEditing.value) {
      await api.put(`/articles/${editId.value}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("Artikel berhasil diperbarui!");
    } else {
      await api.post("/articles/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("Artikel berhasil diterbitkan!");
    }

    closeModal();
    fetchArticles();
  } catch (err) {
    alert("Gagal menyimpan artikel. Pastikan file gambar valid jika ada.");
  } finally {
    isSaving.value = false;
  }
};

const handleDelete = async (id) => {
  if (!confirm("Apakah Anda yakin ingin menghapus artikel ini permanen?"))
    return;
  try {
    await api.delete(`/articles/${id}`);
    fetchArticles();
  } catch (err) {
    alert("Gagal menghapus artikel");
  }
};

onMounted(() => fetchArticles());
</script>
