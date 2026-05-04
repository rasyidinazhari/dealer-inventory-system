<template>
  <div>
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Selamat datang, {{ userName }} 👋</h1>
      <p class="text-sm text-gray-500 mt-1">Berikut adalah ringkasan sistem dealer motor hari ini.</p>
    </div>

    <div v-if="isLoading" class="flex justify-center py-12">
      <div class="animate-pulse flex flex-col items-center">
        <div class="h-8 w-8 bg-blue-400 rounded-full mb-4"></div>
        <p class="text-gray-500">Memuat data dashboard...</p>
      </div>
    </div>

    <div v-else class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">Total Omzet</p>
              <h3 class="text-xl font-bold text-gray-900 mt-1">{{ formatCurrency(stats.totalRevenue) }}</h3>
            </div>
            <div class="p-3 bg-blue-50 text-blue-600 rounded-lg">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </div>
          </div>
        </div>

        <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">Unit Terjual</p>
              <h3 class="text-xl font-bold text-gray-900 mt-1">{{ stats.totalSales }} Unit</h3>
            </div>
            <div class="p-3 bg-orange-50 text-orange-600 rounded-lg">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path></svg>
            </div>
          </div>
        </div>

        <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">Sisa Stok Motor</p>
              <h3 class="text-xl font-bold text-gray-900 mt-1">{{ stats.totalStock }} Unit</h3>
            </div>
            <div class="p-3 bg-green-50 text-green-600 rounded-lg">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"></path></svg>
            </div>
          </div>
        </div>

        <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">Total Pelanggan</p>
              <h3 class="text-xl font-bold text-gray-900 mt-1">{{ stats.totalCustomers }} Orang</h3>
            </div>
            <div class="p-3 bg-purple-50 text-purple-600 rounded-lg">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h3 class="text-lg font-bold text-gray-900">Transaksi Terbaru</h3>
          <router-link to="/admin/sales" class="text-sm text-blue-600 hover:text-blue-800 font-medium">
            Lihat Semua &rarr;
          </router-link>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">No. Invoice</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Pelanggan</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Motor</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Tipe Bayar</th>
                <th scope="col" class="px-6 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider">Total</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="recentSales.length === 0" class="text-center">
                <td colspan="5" class="px-6 py-8 text-sm text-gray-500">Belum ada transaksi.</td>
              </tr>
              <tr v-else v-for="sale in recentSales" :key="sale.id" class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-3 whitespace-nowrap text-sm font-medium text-gray-900">{{ sale.invoice_number }}</td>
                <td class="px-6 py-3 whitespace-nowrap text-sm text-gray-700">{{ sale.customer_name }}</td>
                <td class="px-6 py-3 whitespace-nowrap text-sm text-gray-700">{{ sale.motorcycle_name }}</td>
                <td class="px-6 py-3 whitespace-nowrap">
                  <span class="px-2.5 py-1 inline-flex text-xs leading-5 font-semibold rounded-full uppercase"
                        :class="sale.payment_type === 'cash' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'">
                    {{ sale.payment_type }}
                  </span>
                </td>
                <td class="px-6 py-3 whitespace-nowrap text-sm text-gray-900 font-medium text-right">
                  {{ formatCurrency(sale.total_price) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../../services/api';

const userName = ref('');
const isLoading = ref(true);

// State untuk merangkum data
const stats = ref({
  totalRevenue: 0,
  totalSales: 0,
  totalStock: 0,
  totalCustomers: 0
});

const recentSales = ref([]);

// Format Rupiah
const formatCurrency = (value) => {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(value || 0);
};

const fetchDashboardData = async () => {
  isLoading.value = true;
  try {
    // Kita panggil 4 API secara paralel agar lebih cepat
    const [financeRes, salesRes, inventoryRes, customerRes] = await Promise.all([
      api.get('/finance/summary'),
      api.get('/sales/'),
      api.get('/inventory/'),
      api.get('/master/customers')
    ]);

    // Set Data Keuangan
    stats.value.totalRevenue = financeRes.data.data.summary.total_revenue;
    stats.value.totalSales = financeRes.data.data.summary.total_transactions;
    
    // Set Data Pelanggan
    stats.value.totalCustomers = customerRes.data.data.length;

    // Hitung Total Stok (Jumlahkan semua atribut stock dari setiap motor)
    const motors = inventoryRes.data.data;
    let sumStock = 0;
    motors.forEach(m => { sumStock += m.stock; });
    stats.value.totalStock = sumStock;

    // Ambil 5 Transaksi Terbaru (karena API /sales sudah diurutkan dari terbaru)
    recentSales.value = salesRes.data.data.slice(0, 5);

  } catch (error) {
    console.error("Gagal memuat data dashboard:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  // Ambil nama user dari localStorage
  const userData = localStorage.getItem('user_data');
  if (userData) {
    const user = JSON.parse(userData);
    userName.value = user.username;
  }
  
  fetchDashboardData();
});
</script>