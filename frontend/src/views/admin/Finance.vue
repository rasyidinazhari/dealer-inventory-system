<template>
  <div class="space-y-6">
    <!-- HEADER & FILTER -->
    <div
      class="flex flex-col items-start justify-between gap-5 mb-8 xl:flex-row xl:items-center"
    >
      <div class="shrink-0">
        <h1 class="text-2xl font-bold text-gray-900">Laporan Keuangan</h1>
        <p class="mt-1 text-sm text-gray-500">
          Pantau pendapatan kotor, laba bersih, dan arus kas dealer.
        </p>
      </div>

      <!-- Gunakan flex-wrap agar filter turun ke baris baru jika layar sempit -->
      <div class="flex flex-wrap items-center w-full gap-3 xl:w-auto">
        <!-- Filter Bulan -->
        <select
          v-model="filter.month"
          @change="fetchFinanceData"
          class="block py-2.5 pl-4 pr-10 font-medium text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm cursor-pointer"
        >
          <option value="">Semua Bulan</option>
          <option v-for="(m, index) in months" :key="index" :value="index + 1">
            {{ m }}
          </option>
        </select>

        <!-- Filter Tahun (Tambahkan pr-10 agar angka tidak tertabrak panah) -->
        <select
          v-model="filter.year"
          @change="fetchFinanceData"
          class="block py-2.5 pl-4 pr-10 font-medium text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm cursor-pointer"
        >
          <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
        </select>

        <button
          @click="generatePDF"
          :disabled="finances.length === 0"
          class="flex items-center justify-center gap-2 px-5 py-2.5 text-sm font-bold text-gray-700 transition-colors bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50 disabled:opacity-50"
        >
          <svg
            class="w-4 h-4 text-red-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          Cetak PDF
        </button>

        <button
          @click="fetchFinanceData"
          class="flex items-center justify-center gap-2 px-5 py-2.5 text-sm font-bold text-white transition-colors bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700"
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
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
            ></path>
          </svg>
          Refresh
        </button>
      </div>
    </div>

    <!-- SUMMARY CARDS (Ubah jadi 2 Kolom: sm:grid-cols-2) -->
    <div
      v-if="isLoading"
      class="grid grid-cols-1 gap-6 sm:grid-cols-2 animate-pulse"
    >
      <div v-for="i in 4" :key="i" class="h-32 bg-gray-200 rounded-2xl"></div>
    </div>

    <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2">
      <!-- Card 1: Pendapatan Kotor -->
      <div
        class="flex flex-col p-6 bg-white border border-gray-100 shadow-sm rounded-2xl"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider">
            Total Omset (Gross)
          </h3>
          <div class="p-2 text-blue-600 bg-blue-100 rounded-lg shrink-0">
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              ></path>
            </svg>
          </div>
        </div>
        <!-- Hilangkan truncate, besarkan kembali ukurannya -->
        <p class="text-3xl font-black text-gray-900 md:text-4xl">
          {{ formatCurrency(summary.gross_revenue) }}
        </p>
        <p class="mt-2 text-sm font-medium text-gray-500">
          Total uang masuk dari penjualan.
        </p>
      </div>

      <!-- Card 2: Laba Bersih -->
      <div
        class="flex flex-col p-6 bg-gradient-to-br from-green-500 to-green-600 border border-green-100 shadow-md rounded-2xl text-white transform hover:-translate-y-1 transition-transform"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-sm font-bold text-green-100 uppercase tracking-wider">
            Laba Bersih (Net Profit)
          </h3>
          <div
            class="p-2 text-green-100 bg-white/20 rounded-lg backdrop-blur-sm shrink-0"
          >
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
              ></path>
            </svg>
          </div>
        </div>
        <p class="text-3xl font-black text-white md:text-4xl">
          {{ formatCurrency(summary.net_profit) }}
        </p>
        <p class="mt-2 text-sm font-medium text-green-100">
          Setelah potong modal & perbaikan.
        </p>
      </div>

      <!-- Card 3: Biaya / Pengeluaran -->
      <div
        class="flex flex-col p-6 bg-white border border-gray-100 shadow-sm rounded-2xl"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider">
            Total Modal & Servis
          </h3>
          <div class="p-2 text-red-600 bg-red-100 rounded-lg shrink-0">
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              ></path>
            </svg>
          </div>
        </div>
        <p class="text-3xl font-black text-gray-900 md:text-4xl">
          {{ formatCurrency(summary.total_costs) }}
        </p>
        <p class="mt-2 text-sm font-medium text-gray-500">
          Harga beli + biaya perbaikan unit.
        </p>
      </div>

      <!-- Card 4: Total Transaksi -->
      <div
        class="flex flex-col p-6 bg-white border border-gray-100 shadow-sm rounded-2xl"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider">
            Unit Terjual
          </h3>
          <div class="p-2 text-purple-600 bg-purple-100 rounded-lg shrink-0">
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              ></path>
            </svg>
          </div>
        </div>
        <p class="text-3xl font-black text-gray-900 md:text-4xl">
          {{ summary.total_sales_count }}
          <span class="text-xl font-bold text-gray-500">Unit</span>
        </p>
        <p class="mt-2 text-sm font-medium text-gray-500">
          Total transaksi selesai & disetujui.
        </p>
      </div>
    </div>

    <!-- TABEL RINCIAN KEUANGAN -->
    <div
      class="overflow-hidden bg-white border border-gray-200 shadow-sm rounded-xl"
    >
      <div class="px-6 py-5 border-b border-gray-100 bg-gray-50">
        <h3 class="text-lg font-bold text-gray-900">
          Rincian Laba per Transaksi
        </h3>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-white">
            <tr>
              <th
                scope="col"
                class="px-6 py-4 text-xs font-bold tracking-wider text-left text-gray-500 uppercase"
              >
                Invoice & Tanggal
              </th>
              <th
                scope="col"
                class="px-6 py-4 text-xs font-bold tracking-wider text-left text-gray-500 uppercase"
              >
                Kendaraan
              </th>
              <th
                scope="col"
                class="px-6 py-4 text-xs font-bold tracking-wider text-right text-gray-500 uppercase"
              >
                HPP (Modal + Servis)
              </th>
              <th
                scope="col"
                class="px-6 py-4 text-xs font-bold tracking-wider text-right text-gray-500 uppercase"
              >
                Harga Terjual
              </th>
              <th
                scope="col"
                class="px-6 py-4 text-xs font-bold tracking-wider text-right text-gray-900 uppercase bg-green-50"
              >
                Laba Bersih
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-100">
            <tr v-if="isLoading" class="text-center">
              <td colspan="5" class="px-6 py-8 text-sm text-gray-500">
                Menghitung data keuangan...
              </td>
            </tr>
            <tr v-else-if="finances.length === 0" class="text-center">
              <td colspan="5" class="px-6 py-12 text-sm text-gray-500">
                Tidak ada transaksi pada periode ini.
              </td>
            </tr>

            <tr
              v-else
              v-for="item in finances"
              :key="item.id"
              class="transition-colors hover:bg-gray-50"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-bold text-gray-900">
                  {{ item.invoice_number }}
                </div>
                <div class="text-xs text-gray-500 mt-1">
                  {{ formatDate(item.sale_date) }}
                </div>
                <div class="text-[10px] font-bold text-blue-600 mt-1">
                  {{ item.branch_name }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-bold text-gray-900">
                  {{ item.motor_name }}
                </div>
                <div class="text-xs text-gray-500 mt-1">
                  Status:
                  <span class="font-semibold text-green-600">{{
                    item.status
                  }}</span>
                </div>
              </td>
              <td class="px-6 py-4 text-right whitespace-nowrap">
                <div class="text-sm text-gray-500 line-through">
                  {{ formatCurrency(item.capital_price) }}
                </div>
                <div class="text-xs text-red-500 mt-0.5">
                  + Perbaikan: {{ formatCurrency(item.repair_cost) }}
                </div>
                <div class="text-sm font-bold text-gray-800 mt-1">
                  {{ formatCurrency(item.capital_price + item.repair_cost) }}
                </div>
              </td>
              <td
                class="px-6 py-4 text-sm font-bold text-right text-gray-900 whitespace-nowrap"
              >
                {{ formatCurrency(item.total_price) }}
                <span
                  v-if="item.is_deal_price"
                  class="block text-[10px] text-blue-600 mt-1"
                  >Harga Nego</span
                >
              </td>
              <td class="px-6 py-4 text-right whitespace-nowrap bg-green-50/30">
                <div class="text-sm font-black text-green-600">
                  {{ formatCurrency(item.net_profit) }}
                </div>
                <div class="text-[10px] font-bold text-gray-400 mt-1 uppercase">
                  {{ item.payment_type }}
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import api from "../../services/api";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

const finances = ref([]);
const summary = ref({
  gross_revenue: 0,
  total_costs: 0,
  net_profit: 0,
  total_sales_count: 0,
});
const isLoading = ref(true);

const months = [
  "Januari",
  "Februari",
  "Maret",
  "April",
  "Mei",
  "Juni",
  "Juli",
  "Agustus",
  "September",
  "Oktober",
  "November",
  "Desember",
];
const currentYear = new Date().getFullYear();
const years = [currentYear, currentYear - 1, currentYear - 2];

const filter = ref({
  month: new Date().getMonth() + 1, // Default ke bulan ini
  year: currentYear,
});

const formatCurrency = (value) =>
  new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    minimumFractionDigits: 0,
  }).format(value || 0);

const formatDate = (dateString) => {
  if (!dateString) return "-";
  return new Date(dateString).toLocaleDateString("id-ID", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
};

const fetchFinanceData = async () => {
  isLoading.value = true;
  try {
    // Ambil branch_id dari filter navbar Super Admin (jika ada)
    const branchId = localStorage.getItem("selected_branch_id") || "";

    // Tembak ke API /api/finance/ (Pastikan backend finance.py kamu sudah siap)
    const response = await api.get(
      `/finance/?branch_id=${branchId}&month=${filter.value.month}&year=${filter.value.year}`,
    );

    finances.value = response.data.data;
    summary.value = response.data.summary;
  } catch (error) {
    console.error("Gagal mengambil data keuangan", error);
    // Fallback error (Hapus alert ini kalau dirasa mengganggu)
  } finally {
    isLoading.value = false;
  }
};

// Listen jika Super Admin mengganti cabang di Navbar atas
const handleBranchChange = () => fetchFinanceData();

onMounted(() => {
  fetchFinanceData();
  window.addEventListener("branchChanged", handleBranchChange);
});

onUnmounted(() => {
  window.removeEventListener("branchChanged", handleBranchChange);
});

// FUNGSI GENERATE PDF
// FUNGSI GENERATE PDF
const generatePDF = () => {
  const doc = new jsPDF();

  // PERBAIKAN: Pastikan ini selalu menjadi String/Teks
  const dateStr = filter.value.month
    ? `${months[filter.value.month - 1]} ${filter.value.year}`
    : `Tahun ${filter.value.year}`; // Tambahkan kata "Tahun" agar otomatis jadi String

  // Header Laporan
  doc.setFontSize(18);

  doc.text("LAPORAN KEUANGAN ABU MOTOR", 14, 20);
  doc.setFontSize(11);
  doc.text(`Periode: ${dateStr}`, 14, 28);
  doc.text(`Dicetak pada: ${new Date().toLocaleString("id-ID")}`, 14, 34);

  // Ringkasan Metrics
  autoTable(doc, {
    startY: 40,
    head: [["Deskripsi", "Total Nilai"]],
    body: [
      ["Total Omset (Gross)", formatCurrency(summary.value.gross_revenue)],
      ["Total Modal & Servis", formatCurrency(summary.value.total_costs)],
      ["Laba Bersih (Net Profit)", formatCurrency(summary.value.net_profit)],
      ["Unit Terjual", `${summary.value.total_sales_count} Unit`],
    ],
    theme: "grid",
    headStyles: { fillColor: [37, 99, 235] },
  });

  // Rincian Transaksi
  const tableData = finances.value.map((item) => [
    item.invoice_number,
    item.motor_name,
    formatCurrency(item.capital_price + item.repair_cost),
    formatCurrency(item.total_price),
    formatCurrency(item.net_profit),
  ]);

  doc.text("Rincian Transaksi:", 14, doc.lastAutoTable.finalY + 10);

  // Tabel Rincian
  autoTable(doc, {
    startY: doc.lastAutoTable.finalY + 15,
    head: [["Invoice", "Unit", "HPP", "Harga Jual", "Laba"]],
    body: tableData,
    headStyles: { fillColor: [22, 163, 74] },
  });

  // Download File (Gunakan regex / /g untuk me-replace semua spasi jika ada)
  doc.save(`Laporan-Keuangan-AbuMotor-${dateStr.replace(/ /g, "-")}.pdf`);
};
</script>
