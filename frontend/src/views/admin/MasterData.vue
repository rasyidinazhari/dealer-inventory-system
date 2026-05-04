<template>
  <div class="space-y-10">
    
    <section>
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4 gap-4">
        <div>
          <h2 class="text-xl font-bold text-gray-900">Data Pelanggan (Customers)</h2>
          <p class="text-sm text-gray-500">Daftar pelanggan yang pernah bertransaksi.</p>
        </div>
        
        <div class="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
          <div class="relative w-full sm:w-64">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            </div>
            <input 
              v-model="searchCustomer" 
              type="text" 
              placeholder="Cari NIK atau Nama..." 
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm shadow-sm"
            >
          </div>

          <button @click="openCustomerModal()" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium flex items-center justify-center gap-2 shadow-sm">
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" /></svg>
            Tambah
          </button>
        </div>
      </div>

      <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">NIK</th>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Nama Lengkap</th>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">No. HP / WA</th>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Alamat</th>
                <th class="px-6 py-3 text-right text-xs font-semibold text-gray-500 uppercase">Aksi</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="isLoadingCustomers" class="text-center"><td colspan="5" class="px-6 py-6 text-sm text-gray-500">Memuat data...</td></tr>
              <tr v-else-if="filteredCustomers.length === 0" class="text-center">
                <td colspan="5" class="px-6 py-8">
                  <p class="text-sm text-gray-500">Tidak ada pelanggan yang cocok dengan pencarian "<span class="text-gray-900">{{ searchCustomer }}</span>"</p>
                </td>
              </tr>
              <tr v-else v-for="c in filteredCustomers" :key="c.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ c.nik }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{{ c.full_name }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{{ c.phone_number }}</td>
                <td class="px-6 py-4 text-sm text-gray-500 truncate max-w-xs">{{ c.address }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button @click="openCustomerModal(c)" class="text-blue-600 hover:text-blue-900 mr-3">Edit</button>
                  <button @click="deleteCustomer(c.id)" class="text-red-600 hover:text-red-900">Hapus</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <hr class="border-gray-200">

    <section>
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4 gap-4">
        <div>
          <h2 class="text-xl font-bold text-gray-900">Data Mitra (Affiliates)</h2>
          <p class="text-sm text-gray-500">Kelola agen/mitra yang membantu penjualan.</p>
        </div>
        
        <div class="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
          <div class="relative w-full sm:w-64">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            </div>
            <input 
              v-model="searchAffiliate" 
              type="text" 
              placeholder="Cari Nama atau Kode..." 
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm shadow-sm"
            >
          </div>

          <button @click="openAffiliateModal()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-medium flex items-center justify-center gap-2 shadow-sm">
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" /></svg>
            Tambah
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
              <tr v-if="isLoadingAffiliates" class="text-center"><td colspan="5" class="px-6 py-6 text-sm text-gray-500">Memuat data...</td></tr>
              <tr v-else-if="filteredAffiliates.length === 0" class="text-center">
                <td colspan="5" class="px-6 py-8">
                  <p class="text-sm text-gray-500">Tidak ada mitra yang cocok dengan pencarian "<span class="text-gray-900">{{ searchAffiliate }}</span>"</p>
                </td>
              </tr>
              <tr v-else v-for="a in filteredAffiliates" :key="a.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-indigo-600">{{ a.referral_code }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">{{ a.name }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{{ a.phone_number || '-' }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">{{ formatCurrency(a.commission_balance) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button @click="openAffiliateModal(a)" class="text-blue-600 hover:text-blue-900 mr-3">Edit</button>
                  <button @click="deleteAffiliate(a.id)" class="text-red-600 hover:text-red-900">Hapus</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <div v-if="isCustomerModalOpen" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen px-4">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75" @click="isCustomerModalOpen = false"></div>
        <div class="relative bg-white rounded-xl shadow-xl w-full max-w-md p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">{{ isEditCustomer ? 'Edit' : 'Tambah' }} Pelanggan</h3>
          <form @submit.prevent="saveCustomer" class="space-y-4">
            <div><label class="block text-sm font-medium text-gray-700">NIK KTP</label><input v-model="customerForm.nik" required type="text" class="mt-1 w-full border border-gray-300 rounded-md py-2 px-3"></div>
            <div><label class="block text-sm font-medium text-gray-700">Nama Lengkap</label><input v-model="customerForm.full_name" required type="text" class="mt-1 w-full border border-gray-300 rounded-md py-2 px-3"></div>
            <div><label class="block text-sm font-medium text-gray-700">No HP/WA</label><input v-model="customerForm.phone_number" required type="text" class="mt-1 w-full border border-gray-300 rounded-md py-2 px-3"></div>
            <div><label class="block text-sm font-medium text-gray-700">Alamat</label><textarea v-model="customerForm.address" rows="2" class="mt-1 w-full border border-gray-300 rounded-md py-2 px-3"></textarea></div>
            <div class="flex justify-end gap-2 pt-4 border-t">
              <button type="button" @click="isCustomerModalOpen = false" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg">Batal</button>
              <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-lg">{{ isEditCustomer ? 'Update' : 'Simpan' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="isAffiliateModalOpen" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen px-4">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75" @click="isAffiliateModalOpen = false"></div>
        <div class="relative bg-white rounded-xl shadow-xl w-full max-w-md p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">{{ isEditAffiliate ? 'Edit' : 'Tambah' }} Mitra</h3>
          <form @submit.prevent="saveAffiliate" class="space-y-4">
            <div><label class="block text-sm font-medium text-gray-700">Nama Mitra</label><input v-model="affiliateForm.name" required type="text" class="mt-1 w-full border border-gray-300 rounded-md py-2 px-3"></div>
            <div><label class="block text-sm font-medium text-gray-700">Kode Referral (Unik)</label><input v-model="affiliateForm.referral_code" required type="text" class="mt-1 w-full border border-gray-300 rounded-md py-2 px-3 uppercase"></div>
            <div><label class="block text-sm font-medium text-gray-700">No HP/WA</label><input v-model="affiliateForm.phone_number" type="text" class="mt-1 w-full border border-gray-300 rounded-md py-2 px-3"></div>
            <div class="flex justify-end gap-2 pt-4 border-t">
              <button type="button" @click="isAffiliateModalOpen = false" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg">Batal</button>
              <button type="submit" class="px-4 py-2 bg-indigo-600 text-white rounded-lg">{{ isEditAffiliate ? 'Update' : 'Simpan' }}</button>
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

// =======================
// STATE & PENCARIAN
// =======================
const customers = ref([]);
const affiliates = ref([]);
const isLoadingCustomers = ref(false);
const isLoadingAffiliates = ref(false);

const searchCustomer = ref('');
const searchAffiliate = ref('');

const formatCurrency = (value) => {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(value || 0);
};

// =======================
// LOGIKA PENCARIAN (COMPUTED)
// =======================
const filteredCustomers = computed(() => {
  if (!searchCustomer.value) return customers.value;
  const query = searchCustomer.value.toLowerCase();
  return customers.value.filter(c => 
    c.full_name.toLowerCase().includes(query) || 
    c.nik.toLowerCase().includes(query) ||
    (c.phone_number && c.phone_number.includes(query))
  );
});

const filteredAffiliates = computed(() => {
  if (!searchAffiliate.value) return affiliates.value;
  const query = searchAffiliate.value.toLowerCase();
  return affiliates.value.filter(a => 
    a.name.toLowerCase().includes(query) || 
    a.referral_code.toLowerCase().includes(query) ||
    (a.phone_number && a.phone_number.includes(query))
  );
});

// =======================
// CUSTOMER CRUD
// =======================
const isCustomerModalOpen = ref(false);
const isEditCustomer = ref(false);
const currentCustomerId = ref(null);
const customerForm = ref({ nik: '', full_name: '', phone_number: '', address: '' });

const fetchCustomers = async () => {
  isLoadingCustomers.value = true;
  try {
    const res = await api.get('/master/customers');
    customers.value = res.data.data;
  } catch (error) { console.error(error); } 
  finally { isLoadingCustomers.value = false; }
};

const openCustomerModal = (c = null) => {
  if (c) {
    isEditCustomer.value = true;
    currentCustomerId.value = c.id;
    customerForm.value = { ...c };
  } else {
    isEditCustomer.value = false;
    currentCustomerId.value = null;
    customerForm.value = { nik: '', full_name: '', phone_number: '', address: '' };
  }
  isCustomerModalOpen.value = true;
};

const saveCustomer = async () => {
  try {
    if (isEditCustomer.value) await api.put(`/master/customers/${currentCustomerId.value}`, customerForm.value);
    else await api.post('/master/customers', customerForm.value);
    isCustomerModalOpen.value = false;
    fetchCustomers();
  } catch (error) { alert('Gagal menyimpan pelanggan.'); }
};

const deleteCustomer = async (id) => {
  if(confirm('Hapus pelanggan ini?')) {
    try { await api.delete(`/master/customers/${id}`); fetchCustomers(); } 
    catch (e) { alert('Gagal menghapus pelanggan.'); }
  }
};

// =======================
// AFFILIATE CRUD
// =======================
const isAffiliateModalOpen = ref(false);
const isEditAffiliate = ref(false);
const currentAffiliateId = ref(null);
const affiliateForm = ref({ name: '', referral_code: '', phone_number: '' });

const fetchAffiliates = async () => {
  isLoadingAffiliates.value = true;
  try {
    const res = await api.get('/master/affiliates');
    affiliates.value = res.data.data;
  } catch (error) { console.error(error); } 
  finally { isLoadingAffiliates.value = false; }
};

const openAffiliateModal = (a = null) => {
  if (a) {
    isEditAffiliate.value = true;
    currentAffiliateId.value = a.id;
    affiliateForm.value = { ...a };
  } else {
    isEditAffiliate.value = false;
    currentAffiliateId.value = null;
    affiliateForm.value = { name: '', referral_code: '', phone_number: '' };
  }
  isAffiliateModalOpen.value = true;
};

const saveAffiliate = async () => {
  try {
    // Pastikan kode referral kapital
    affiliateForm.value.referral_code = affiliateForm.value.referral_code.toUpperCase();
    if (isEditAffiliate.value) await api.put(`/master/affiliates/${currentAffiliateId.value}`, affiliateForm.value);
    else await api.post('/master/affiliates', affiliateForm.value);
    isAffiliateModalOpen.value = false;
    fetchAffiliates();
  } catch (error) { alert('Gagal menyimpan mitra.'); }
};

const deleteAffiliate = async (id) => {
  if(confirm('Hapus mitra ini?')) {
    try { await api.delete(`/master/affiliates/${id}`); fetchAffiliates(); } 
    catch (e) { alert('Gagal menghapus mitra.'); }
  }
};

// =======================
// INITIALIZATION
// =======================
onMounted(() => {
  fetchCustomers();
  fetchAffiliates();
});
</script>