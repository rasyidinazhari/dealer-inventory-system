<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-gray-800">
        Manajemen Merek, Model & Kategori
      </h1>
    </div>

    <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
      <!-- BAGIAN MEREK (BRANDS) -->
      <div class="p-6 bg-white border border-gray-200 shadow-sm rounded-xl">
        <h2 class="mb-4 text-lg font-semibold text-gray-800">
          Daftar Merek Kendaraan
        </h2>

        <form @submit.prevent="addBrand" class="flex gap-2 mb-6">
          <input
            v-model="newBrand"
            type="text"
            placeholder="Contoh: Honda, Toyota..."
            class="flex-1 px-4 py-2 text-sm border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
            required
          />
          <button
            type="submit"
            :disabled="isSubmittingBrand"
            class="px-4 py-2 text-sm font-medium text-white transition-colors bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {{ isSubmittingBrand ? "Menyimpan..." : "Tambah" }}
          </button>
        </form>

        <div class="overflow-hidden border border-gray-200 rounded-lg">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase"
                >
                  ID
                </th>
                <th
                  class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase"
                >
                  Nama Merek
                </th>
                <th
                  class="px-6 py-3 text-xs font-medium tracking-wider text-right text-gray-500 uppercase"
                >
                  Aksi
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="brands.length === 0">
                <td
                  colspan="3"
                  class="px-6 py-4 text-sm text-center text-gray-500"
                >
                  Belum ada data merek.
                </td>
              </tr>
              <tr
                v-for="brand in brands"
                :key="brand.id"
                class="hover:bg-gray-50"
              >
                <td class="px-6 py-4 text-sm text-gray-500 whitespace-nowrap">
                  {{ brand.id }}
                </td>
                <td
                  class="px-6 py-4 text-sm font-medium text-gray-900 whitespace-nowrap"
                >
                  {{ brand.name }}
                </td>
                <td
                  class="px-6 py-4 text-sm font-medium text-right whitespace-nowrap"
                >
                  <button
                    @click="openEditModal('brand', brand)"
                    class="mr-3 text-blue-600 hover:text-blue-900"
                  >
                    Edit
                  </button>
                  <button
                    @click="openDeleteModal('brand', brand)"
                    class="text-red-600 hover:text-red-900"
                  >
                    Hapus
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- BAGIAN KATEGORI (CATEGORIES) -->
      <div class="p-6 bg-white border border-gray-200 shadow-sm rounded-xl">
        <h2 class="mb-4 text-lg font-semibold text-gray-800">
          Daftar Kategori Kendaraan
        </h2>

        <form @submit.prevent="addCategory" class="flex gap-2 mb-6">
          <input
            v-model="newCategory"
            type="text"
            placeholder="Contoh: Matic, SUV, Sedan..."
            class="flex-1 px-4 py-2 text-sm border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
            required
          />
          <button
            type="submit"
            :disabled="isSubmittingCategory"
            class="px-4 py-2 text-sm font-medium text-white transition-colors bg-green-600 rounded-lg hover:bg-green-700 disabled:opacity-50"
          >
            {{ isSubmittingCategory ? "Menyimpan..." : "Tambah" }}
          </button>
        </form>

        <div class="overflow-hidden border border-gray-200 rounded-lg">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase"
                >
                  ID
                </th>
                <th
                  class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase"
                >
                  Nama Kategori
                </th>
                <th
                  class="px-6 py-3 text-xs font-medium tracking-wider text-right text-gray-500 uppercase"
                >
                  Aksi
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="categories.length === 0">
                <td
                  colspan="3"
                  class="px-6 py-4 text-sm text-center text-gray-500"
                >
                  Belum ada data kategori.
                </td>
              </tr>
              <tr
                v-for="cat in categories"
                :key="cat.id"
                class="hover:bg-gray-50"
              >
                <td class="px-6 py-4 text-sm text-gray-500 whitespace-nowrap">
                  {{ cat.id }}
                </td>
                <td
                  class="px-6 py-4 text-sm font-medium text-gray-900 whitespace-nowrap"
                >
                  {{ cat.name }}
                </td>
                <td
                  class="px-6 py-4 text-sm font-medium text-right whitespace-nowrap"
                >
                  <button
                    @click="openEditModal('category', cat)"
                    class="mr-3 text-blue-600 hover:text-blue-900"
                  >
                    Edit
                  </button>
                  <button
                    @click="openDeleteModal('category', cat)"
                    class="text-red-600 hover:text-red-900"
                  >
                    Hapus
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- BAGIAN MODEL KENDARAAN (FULL WIDTH) -->
      <div
        class="p-6 bg-white border border-gray-200 shadow-sm rounded-xl lg:col-span-2"
      >
        <h2 class="mb-4 text-lg font-semibold text-gray-800">
          Daftar Model Kendaraan (Sub-Merek)
        </h2>

        <form
          @submit.prevent="addModel"
          class="flex flex-col gap-2 mb-6 sm:flex-row"
        >
          <select
            v-model="newModelBrandId"
            class="px-4 py-2 text-sm border border-gray-300 rounded-lg sm:w-1/3 focus:ring-blue-500"
            required
          >
            <option value="">-- Pilih Merek --</option>
            <option v-for="b in brands" :key="b.id" :value="b.id">
              {{ b.name }}
            </option>
          </select>
          <input
            v-model="newModelName"
            type="text"
            placeholder="Nama Model (Contoh: Vario 150, Nmax...)"
            class="flex-1 px-4 py-2 text-sm border border-gray-300 rounded-lg focus:ring-blue-500"
            required
          />
          <button
            type="submit"
            :disabled="isSubmittingModel"
            class="px-6 py-2 text-sm font-medium text-white transition-colors bg-purple-600 rounded-lg hover:bg-purple-700 disabled:opacity-50"
          >
            {{ isSubmittingModel ? "Menyimpan..." : "Tambah Model" }}
          </button>
        </form>

        <div class="overflow-hidden border border-gray-200 rounded-lg">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase"
                >
                  Merek
                </th>
                <th
                  class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase"
                >
                  Model Kendaraan
                </th>
                <th
                  class="px-6 py-3 text-xs font-medium tracking-wider text-right text-gray-500 uppercase"
                >
                  Aksi
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <template v-for="brand in brands" :key="'grp-' + brand.id">
                <tr
                  v-for="model in brand.models"
                  :key="model.id"
                  class="hover:bg-gray-50"
                >
                  <td
                    class="px-6 py-4 text-sm font-bold text-gray-900 whitespace-nowrap"
                  >
                    {{ brand.name }}
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500 whitespace-nowrap">
                    {{ model.name }}
                  </td>
                  <td
                    class="px-6 py-4 text-sm font-medium text-right whitespace-nowrap"
                  >
                    <!-- SUDAH MENGGUNAKAN MODAL CUSTOM -->
                    <button
                      @click="openEditModal('model', model)"
                      class="mr-3 text-blue-600 hover:text-blue-900"
                    >
                      Edit
                    </button>
                    <button
                      @click="openDeleteModal('model', model)"
                      class="text-red-600 hover:text-red-900"
                    >
                      Hapus
                    </button>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- MODAL EDIT CUSTOM -->
    <div v-if="editModal.isOpen" class="fixed inset-0 z-50 overflow-y-auto">
      <div
        class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:p-0"
      >
        <div
          class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
          @click="closeEditModal"
        ></div>
        <div
          class="inline-block w-full max-w-md overflow-hidden text-left align-bottom transition-all transform bg-white shadow-xl rounded-xl sm:my-8 sm:align-middle"
        >
          <form @submit.prevent="submitEdit">
            <div class="px-4 pt-5 pb-4 bg-white sm:p-6 sm:pb-4">
              <h3 class="text-lg font-medium leading-6 text-gray-900">
                Edit
                {{
                  editModal.type === "brand"
                    ? "Merek"
                    : editModal.type === "category"
                      ? "Kategori"
                      : "Model"
                }}
              </h3>
              <div class="mt-4">
                <input
                  v-model="editModal.name"
                  type="text"
                  class="block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  required
                />
              </div>
            </div>
            <div
              class="px-4 py-3 bg-gray-50 sm:px-6 sm:flex sm:flex-row-reverse"
            >
              <button
                type="submit"
                :disabled="isProcessing"
                class="inline-flex justify-center w-full px-4 py-2 text-base font-medium text-white transition-colors bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
              >
                {{ isProcessing ? "Menyimpan..." : "Simpan Perubahan" }}
              </button>
              <button
                type="button"
                @click="closeEditModal"
                class="inline-flex justify-center w-full px-4 py-2 mt-3 text-base font-medium text-gray-700 transition-colors bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
              >
                Batal
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- MODAL HAPUS CUSTOM -->
    <div v-if="deleteModal.isOpen" class="fixed inset-0 z-50 overflow-y-auto">
      <div
        class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:p-0"
      >
        <div
          class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
          @click="closeDeleteModal"
        ></div>
        <div
          class="inline-block w-full max-w-md overflow-hidden text-left align-bottom transition-all transform bg-white shadow-xl rounded-xl sm:my-8 sm:align-middle"
        >
          <div class="px-4 pt-5 pb-4 bg-white sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div
                class="flex items-center justify-center flex-shrink-0 w-12 h-12 mx-auto bg-red-100 rounded-full sm:mx-0 sm:h-10 sm:w-10"
              >
                <svg
                  class="w-6 h-6 text-red-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </div>
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                <h3 class="text-lg font-medium leading-6 text-gray-900">
                  Hapus Data
                </h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    Apakah Anda yakin ingin menghapus
                    <strong>{{ deleteModal.name }}</strong
                    >? Data yang dihapus tidak dapat dikembalikan.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="px-4 py-3 bg-gray-50 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              @click="submitDelete"
              :disabled="isProcessing"
              class="inline-flex justify-center w-full px-4 py-2 text-base font-medium text-white transition-colors bg-red-600 border border-transparent rounded-md shadow-sm hover:bg-red-700 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
            >
              {{ isProcessing ? "Menghapus..." : "Ya, Hapus" }}
            </button>
            <button
              type="button"
              @click="closeDeleteModal"
              class="inline-flex justify-center w-full px-4 py-2 mt-3 text-base font-medium text-gray-700 transition-colors bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Batal
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../../services/api"; // Sesuaikan path jika berbeda

// State Merek
const brands = ref([]);
const newBrand = ref("");
const isSubmittingBrand = ref(false);

// State Kategori
const categories = ref([]);
const newCategory = ref("");
const isSubmittingCategory = ref(false);

// State Model
const newModelBrandId = ref("");
const newModelName = ref("");
const isSubmittingModel = ref(false);

// State Modal Custom
const isProcessing = ref(false);

const editModal = ref({
  isOpen: false,
  type: "", // 'brand', 'category', atau 'model'
  id: null,
  name: "",
});

const deleteModal = ref({
  isOpen: false,
  type: "",
  id: null,
  name: "",
});

const fetchData = async () => {
  try {
    const [brandRes, catRes] = await Promise.all([
      api.get("/master/brands"),
      api.get("/master/categories"),
    ]);
    brands.value = brandRes.data.data;
    categories.value = catRes.data.data;
  } catch (error) {
    console.error("Gagal mengambil data master", error);
    alert("Gagal memuat data Merek & Kategori.");
  }
};

onMounted(() => {
  fetchData();
});

// --- Fungsi Tambah ---
const addBrand = async () => {
  if (!newBrand.value.trim()) return;
  isSubmittingBrand.value = true;
  try {
    await api.post("/master/brands", { name: newBrand.value });
    newBrand.value = "";
    await fetchData();
  } catch (error) {
    alert(error.response?.data?.message || "Gagal menambah merek.");
  } finally {
    isSubmittingBrand.value = false;
  }
};

const addCategory = async () => {
  if (!newCategory.value.trim()) return;
  isSubmittingCategory.value = true;
  try {
    await api.post("/master/categories", { name: newCategory.value });
    newCategory.value = "";
    await fetchData();
  } catch (error) {
    alert(error.response?.data?.message || "Gagal menambah kategori.");
  } finally {
    isSubmittingCategory.value = false;
  }
};

const addModel = async () => {
  if (!newModelName.value.trim() || !newModelBrandId.value) return;
  isSubmittingModel.value = true;
  try {
    await api.post("/master/models", {
      brand_id: newModelBrandId.value,
      name: newModelName.value,
    });
    newModelName.value = "";
    await fetchData();
  } catch (error) {
    alert("Gagal menambah model.");
  } finally {
    isSubmittingModel.value = false;
  }
};

// --- Fungsi Kontrol Modal Edit ---
const openEditModal = (type, item) => {
  editModal.value = {
    isOpen: true,
    type: type,
    id: item.id,
    name: item.name,
  };
};

const closeEditModal = () => {
  editModal.value.isOpen = false;
};

const submitEdit = async () => {
  if (!editModal.value.name.trim()) return;
  isProcessing.value = true;

  try {
    if (editModal.value.type === "brand") {
      await api.put(`/master/brands/${editModal.value.id}`, {
        name: editModal.value.name,
      });
    } else if (editModal.value.type === "category") {
      await api.put(`/master/categories/${editModal.value.id}`, {
        name: editModal.value.name,
      });
    } else if (editModal.value.type === "model") {
      await api.put(`/master/models/${editModal.value.id}`, {
        name: editModal.value.name,
      });
    }
    await fetchData();
    closeEditModal();
  } catch (error) {
    alert("Gagal mengedit data.");
  } finally {
    isProcessing.value = false;
  }
};

// --- Fungsi Kontrol Modal Hapus ---
const openDeleteModal = (type, item) => {
  deleteModal.value = {
    isOpen: true,
    type: type,
    id: item.id,
    name: item.name,
  };
};

const closeDeleteModal = () => {
  deleteModal.value.isOpen = false;
};

const submitDelete = async () => {
  isProcessing.value = true;

  try {
    if (deleteModal.value.type === "brand") {
      await api.delete(`/master/brands/${deleteModal.value.id}`);
    } else if (deleteModal.value.type === "category") {
      await api.delete(`/master/categories/${deleteModal.value.id}`);
    } else if (deleteModal.value.type === "model") {
      await api.delete(`/master/models/${deleteModal.value.id}`);
    }
    await fetchData();
    closeDeleteModal();
  } catch (error) {
    alert("Gagal menghapus. Data mungkin sedang digunakan oleh kendaraan.");
  } finally {
    isProcessing.value = false;
  }
};
</script>
