<template>
  <div>
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Data Mitra (Affiliate)</h1>
        <p class="text-sm text-gray-500 mt-1">Kelola agen penjualan dan komisi mereka.</p>
      </div>
      
      <div class="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
        <div class="relative w-full sm:w-64">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
          </div>
          <input v-model="searchQuery" type="text" placeholder="Cari Nama atau Kode..." class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm shadow-sm">
        </div>
        <button @click="openModal()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-medium flex items-center justify-center gap-2 shadow-sm shrink-0">
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" /></svg>
          Tambah Mitra
        </button>
      </div>
    </div>

    <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Kode Referral</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Nama Mitra</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">No. HP / WA</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Saldo Komisi</th>
              <th class="px-6 py-3 text-right text-xs font-semibold text-gray-500 uppercase">Aksi</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="isLoading" class="text-center"><td colspan="5" class="px-6 py-6 text-sm text-gray-500">Memuat data...</td></tr>
            <tr v-else-if="filteredAffiliates.length === 0" class="text-center"><td colspan="5" class="px-6 py-8 text-sm text-gray-500">Tidak ada mitra yang cocok.</td></tr>
            <tr v-else v-for="a in filteredAffiliates" :key="a.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-indigo-600">{{ a.referral_code }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">{{ a.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{{ a.phone_number || '-' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">{{ formatCurrency(a.commission_balance) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button @click="openModal(a)" class="text-blue-600 hover:text-blue-900 mr-3">Edit</button>
                <button @click="deleteAffiliate(a.id)" class="text-red-600 hover:text-red-900">Hapus</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen px-4">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75" @click="closeModal"></div>
        <div class="relative bg-white rounded-xl shadow-xl w-full max-w-md p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">{{ isEditMode ? 'Edit' : 'Tambah' }} Mitra</h3>
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div><label class="block text-sm font-medium text-gray-700">Nama Mitra</label><input v-model="form.name" required type="text" class="mt-1 w-full border border-gray-300 rounded-md py-2 px-3"></div>
            <div><label class="block text-sm font-medium text-gray-700">Kode Referral (Unik)</label><input v-model="form.referral_code" required type="text" class="mt-1 w-full border border-gray-300 rounded-md py-2 px-3 uppercase"></div>
            <div><label class="block text-sm font-medium text-gray-700">No HP/WA</label><input v-model="form.phone_number" type="text" class="mt-1 w-full border border-gray-300 rounded-md py-2 px-3"></div>
            <div class="flex justify-end gap-2 pt-4 border-t">
              <button type="button" @click="closeModal" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg">Batal</button>
              <button type="submit" class="px-4 py-2 bg-indigo-600 text-white rounded-lg">{{ isEditMode ? 'Update' : 'Simpan' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../../services/api';

const affiliates = ref([]);
const isLoading = ref(false);
const searchQuery = ref('');

const isModalOpen = ref(false);
const isEditMode = ref(false);
const currentId = ref(null);
const form = ref({ name: '', referral_code: '', phone_number: '' });

const formatCurrency = (val) => new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(val || 0);

const filteredAffiliates = computed(() => {
  if (!searchQuery.value) return affiliates.value;
  const q = searchQuery.value.toLowerCase();
  return affiliates.value.filter(a => a.name.toLowerCase().includes(q) || a.referral_code.toLowerCase().includes(q));
});

const fetchData = async () => {
  isLoading.value = true;
  try { affiliates.value = (await api.get('/master/affiliates')).data.data; } 
  catch (e) { console.error(e); } 
  finally { isLoading.value = false; }
};

const openModal = (item = null) => {
  if (item) { isEditMode.value = true; currentId.value = item.id; form.value = { ...item }; } 
  else { isEditMode.value = false; currentId.value = null; form.value = { name: '', referral_code: '', phone_number: '' }; }
  isModalOpen.value = true;
};
const closeModal = () => isModalOpen.value = false;

const handleSubmit = async () => {
  try {
    form.value.referral_code = form.value.referral_code.toUpperCase();
    if (isEditMode.value) await api.put(`/master/affiliates/${currentId.value}`, form.value);
    else await api.post('/master/affiliates', form.value);
    closeModal(); fetchData();
  } catch (e) { alert('Gagal menyimpan data.'); }
};

const deleteAffiliate = async (id) => {
  if(confirm('Hapus mitra ini?')) {
    try { await api.delete(`/master/affiliates/${id}`); fetchData(); } 
    catch (e) { alert('Gagal menghapus mitra.'); }
  }
};

onMounted(fetchData);
</script>