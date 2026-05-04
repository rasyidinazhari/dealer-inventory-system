<template>
  <div>
    <!-- HEADER & PENCARIAN -->
    <div
      class="flex flex-col items-start justify-between gap-4 mb-6 sm:flex-row sm:items-center"
    >
      <div>
        <h1 class="text-2xl font-bold text-gray-900">
          Penjualan & Kredit (POS)
        </h1>
        <p class="mt-1 text-sm text-gray-500">
          Kelola transaksi, negosiasi harga, dan syarat kredit.
        </p>
      </div>

      <div class="flex flex-col w-full gap-3 sm:flex-row sm:w-auto">
        <select
          v-model="paymentFilter"
          class="block w-full py-2.5 px-3 font-medium text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm sm:w-40 cursor-pointer"
        >
          <option value="All">Semua Tipe</option>
          <option value="Cash">Tunai (Cash)</option>
          <option value="Kredit">Kredit / Cicilan</option>
        </select>

        <div class="relative w-full sm:w-64">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Cari invoice, pelanggan..."
            class="block w-full py-2.5 pl-3 pr-3 leading-5 placeholder-gray-500 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>

        <button
          @click="openAddModal"
          class="flex items-center justify-center gap-2 px-5 py-2.5 text-sm font-bold text-white transition-colors bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700 shrink-0"
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
          Transaksi Baru
        </button>
      </div>
    </div>

    <!-- TABEL TRANSAKSI -->
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
                Invoice & Tanggal
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Pelanggan & Unit
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Tipe Pembayaran
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Total Harga (Deal)
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Status
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
            <tr v-if="isLoading" class="text-center">
              <td colspan="6" class="px-6 py-8 text-sm text-gray-500">
                Memuat data transaksi...
              </td>
            </tr>
            <tr v-else-if="filteredSales.length === 0" class="text-center">
              <td colspan="6" class="px-6 py-12 text-sm text-gray-500">
                Belum ada data transaksi.
              </td>
            </tr>
            <tr
              v-else
              v-for="sale in filteredSales"
              :key="sale.id"
              class="transition-colors hover:bg-gray-50"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-bold text-gray-900">
                  {{ sale.invoice_number }}
                </div>
                <div class="text-xs text-gray-500">
                  {{ formatDate(sale.sale_date) }}
                </div>
                <div
                  class="text-[10px] font-semibold text-blue-600 mt-1 uppercase"
                >
                  {{ sale.branch_name }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-bold text-gray-900">
                  {{ sale.customer_name }}
                </div>
                <div class="text-xs font-medium text-gray-600">
                  {{ sale.motor_name }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div
                  class="mt-1 text-sm font-bold"
                  :class="
                    sale.payment_type === 'Cash'
                      ? 'text-green-600'
                      : 'text-purple-600'
                  "
                >
                  {{ sale.payment_type.toUpperCase() }}
                </div>
                <div
                  v-if="sale.payment_type === 'Kredit'"
                  class="text-[10px] font-semibold text-gray-500 mt-0.5"
                >
                  DP: {{ formatCurrency(sale.dp_amount) }} |
                  {{ sale.tenor }} bln
                </div>
                <!-- Indikator KTP/KK Uploaded -->
                <div
                  v-if="sale.payment_type === 'Kredit'"
                  class="flex gap-1 mt-1"
                >
                  <span
                    v-if="sale.ktp_url"
                    class="px-1.5 py-0.5 text-[9px] font-bold text-white bg-green-500 rounded"
                    >KTP ✓</span
                  >
                  <span
                    v-if="sale.kk_url"
                    class="px-1.5 py-0.5 text-[9px] font-bold text-white bg-green-500 rounded"
                    >KK ✓</span
                  >
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-black text-gray-900">
                  {{ formatCurrency(sale.total_price) }}
                </div>
                <span
                  v-if="sale.is_deal_price"
                  class="px-2 py-0.5 mt-1 text-[10px] font-bold text-blue-800 bg-blue-100 rounded-full inline-block"
                  >Harga Nego (Deal)</span
                >
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="getStatusBadgeClass(sale.status)"
                  class="inline-flex px-3 py-1 text-xs font-bold leading-5 border rounded-full"
                >
                  {{ sale.status }}
                </span>
              </td>
              <td
                class="px-6 py-4 text-sm font-medium text-right whitespace-nowrap"
              >
                <button
                  v-if="
                    sale.payment_type === 'Kredit' &&
                    sale.status !== 'Disetujui' &&
                    sale.status !== 'Ditolak'
                  "
                  @click="openStatusModal(sale)"
                  class="bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 px-3 py-1.5 rounded-lg shadow-sm transition-colors text-xs font-bold flex items-center gap-1 ml-auto"
                >
                  <svg
                    class="w-4 h-4 text-blue-500"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
                    ></path>
                  </svg>
                  Update
                </button>
                <span
                  v-else-if="sale.payment_type === 'Cash'"
                  class="text-xs italic text-gray-400"
                  >Selesai</span
                >
                <span v-else class="text-xs italic text-gray-400">Final</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL TAMBAH TRANSAKSI (POS) -->
    <div v-if="isAddModalOpen" class="fixed inset-0 z-50 overflow-y-auto">
      <div
        class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:p-0"
      >
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75"
          @click="closeAddModal"
        ></div>
        <div
          class="inline-block w-full overflow-hidden text-left align-bottom transition-all transform bg-white shadow-xl rounded-xl sm:my-8 sm:align-middle sm:max-w-2xl"
        >
          <form @submit.prevent="handleSubmitSale">
            <div
              class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4 max-h-[85vh] overflow-y-auto"
            >
              <h3
                class="pb-3 mb-6 text-xl font-bold text-gray-900 border-b border-gray-200"
              >
                Point of Sales (Kasir)
              </h3>

              <div v-if="isFetchingForm" class="py-4 text-center text-gray-500">
                Memuat data master...
              </div>

              <div v-else class="space-y-6">
                <!-- 1. Pelanggan & Kendaraan (Bisa Diketik) -->
                <div
                  class="p-4 space-y-4 border border-gray-200 bg-gray-50 rounded-xl"
                >
                  <!-- PENCARIAN PELANGGAN -->
                  <div class="relative">
                    <label class="block mb-1 text-sm font-bold text-gray-700"
                      >Pilih Pelanggan (Ketik NIK/Nama)</label
                    >
                    <div class="relative">
                      <input
                        type="text"
                        v-model="customerSearchTerm"
                        @focus="showCustomerDropdown = true"
                        @blur="hideCustomerDropdown"
                        placeholder="Ketik untuk mencari pelanggan..."
                        class="block w-full px-3 py-2.5 bg-white border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        :class="{
                          'border-green-500 bg-green-50': form.customer_id,
                        }"
                      />
                      <!-- Indikator terpilih -->
                      <div
                        v-if="form.customer_id"
                        class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none"
                      >
                        <svg
                          class="w-5 h-5 text-green-500"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M5 13l4 4L19 7"
                          ></path>
                        </svg>
                      </div>
                    </div>

                    <!-- Dropdown Pelanggan -->
                    <ul
                      v-if="
                        showCustomerDropdown && filteredCustomers.length > 0
                      "
                      class="absolute z-10 w-full py-1 mt-1 overflow-auto bg-white border border-gray-200 rounded-md shadow-lg max-h-48"
                    >
                      <li
                        v-for="c in filteredCustomers"
                        :key="c.id"
                        @mousedown.prevent="selectCustomer(c)"
                        class="px-3 py-2 text-sm cursor-pointer hover:bg-blue-50 hover:text-blue-700"
                      >
                        <div class="font-bold">{{ c.name }}</div>
                        <div class="text-xs text-gray-500">
                          NIK: {{ c.nik }}
                        </div>
                      </li>
                    </ul>
                    <div
                      v-if="
                        showCustomerDropdown && filteredCustomers.length === 0
                      "
                      class="absolute z-10 w-full px-3 py-2 mt-1 text-sm text-gray-500 bg-white border border-gray-200 rounded-md shadow-lg"
                    >
                      Pelanggan tidak ditemukan.
                    </div>
                  </div>

                  <!-- PENCARIAN UNIT KENDARAAN -->
                  <div class="relative">
                    <label class="block mb-1 text-sm font-bold text-gray-700"
                      >Pilih Unit Kendaraan (Ketik Tipe/Merek)</label
                    >
                    <div class="relative">
                      <input
                        type="text"
                        v-model="motorSearchTerm"
                        @focus="showMotorDropdown = true"
                        @blur="hideMotorDropdown"
                        placeholder="Ketik untuk mencari unit tersedia..."
                        class="block w-full px-3 py-2.5 bg-white border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        :class="{
                          'border-green-500 bg-green-50': form.motorcycle_id,
                        }"
                      />
                      <!-- Indikator terpilih -->
                      <div
                        v-if="form.motorcycle_id"
                        class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none"
                      >
                        <svg
                          class="w-5 h-5 text-green-500"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M5 13l4 4L19 7"
                          ></path>
                        </svg>
                      </div>
                    </div>

                    <!-- Dropdown Kendaraan -->
                    <ul
                      v-if="showMotorDropdown && filteredMotors.length > 0"
                      class="absolute z-10 w-full py-1 mt-1 overflow-auto bg-white border border-gray-200 rounded-md shadow-lg max-h-48"
                    >
                      <li
                        v-for="m in filteredMotors"
                        :key="m.id"
                        @mousedown.prevent="selectMotor(m)"
                        class="px-3 py-2 text-sm cursor-pointer hover:bg-blue-50 hover:text-blue-700"
                      >
                        <div class="font-bold">{{ m.name }}</div>
                        <div class="flex justify-between text-xs text-gray-500">
                          <span>OTR: {{ formatCurrency(m.price) }}</span>
                          <span class="font-semibold text-blue-600"
                            >Stok: {{ m.stock }}</span
                          >
                        </div>
                      </li>
                    </ul>
                    <div
                      v-if="showMotorDropdown && filteredMotors.length === 0"
                      class="absolute z-10 w-full px-3 py-2 mt-1 text-sm text-gray-500 bg-white border border-gray-200 rounded-md shadow-lg"
                    >
                      Unit tidak ditemukan atau stok kosong.
                    </div>
                  </div>
                </div>

                <!-- 2. FITUR NEGOSIASI HARGA (HARGA DEAL) -->
                <div
                  v-if="form.motorcycle_id"
                  class="p-4 bg-blue-50/50 border border-blue-100 rounded-xl"
                >
                  <div class="flex items-center gap-3 mb-3">
                    <input
                      type="checkbox"
                      v-model="form.is_deal_price"
                      id="dealPrice"
                      class="w-5 h-5 text-blue-600 rounded focus:ring-blue-500"
                    />
                    <label
                      for="dealPrice"
                      class="font-bold text-blue-900 cursor-pointer text-sm"
                      >Gunakan Harga Negosiasi (Deal)</label
                    >
                  </div>

                  <div v-if="form.is_deal_price">
                    <label
                      class="block text-xs font-semibold text-gray-500 mb-1"
                      >Harga Asli:
                      <span class="line-through">{{
                        formatCurrency(selectedMotorPrice)
                      }}</span></label
                    >
                    <input
                      v-model="form.deal_price"
                      type="number"
                      min="0"
                      required
                      @wheel.prevent
                      class="block w-full px-4 py-3 font-bold text-lg border-2 border-blue-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Masukkan harga deal baru (Rp)"
                    />
                  </div>
                </div>

                <!-- 3. Metode Pembayaran -->
                <div class="grid grid-cols-2 gap-4">
                  <div
                    @click="form.payment_type = 'Cash'"
                    :class="
                      form.payment_type === 'Cash'
                        ? 'border-green-500 bg-green-50'
                        : 'border-gray-200 bg-white hover:bg-gray-50'
                    "
                    class="p-4 text-center transition-colors border-2 rounded-xl cursor-pointer"
                  >
                    <p
                      class="font-bold"
                      :class="
                        form.payment_type === 'Cash'
                          ? 'text-green-700'
                          : 'text-gray-500'
                      "
                    >
                      Tunai (Cash)
                    </p>
                  </div>
                  <div
                    @click="form.payment_type = 'Kredit'"
                    :class="
                      form.payment_type === 'Kredit'
                        ? 'border-purple-500 bg-purple-50'
                        : 'border-gray-200 bg-white hover:bg-gray-50'
                    "
                    class="p-4 text-center transition-colors border-2 rounded-xl cursor-pointer"
                  >
                    <p
                      class="font-bold"
                      :class="
                        form.payment_type === 'Kredit'
                          ? 'text-purple-700'
                          : 'text-gray-500'
                      "
                    >
                      Kredit / Cicilan
                    </p>
                  </div>
                </div>

                <!-- 4. Rincian Kredit & Upload Dokumen -->
                <div
                  v-if="form.payment_type === 'Kredit'"
                  class="p-5 space-y-5 border-2 border-purple-200 rounded-xl bg-purple-50/50"
                >
                  <h4
                    class="font-bold text-purple-900 text-sm border-b border-purple-200 pb-2"
                  >
                    Rincian Kredit & Dokumen
                  </h4>

                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <label class="block mb-1 text-sm font-bold text-gray-700"
                        >Nominal DP</label
                      >
                      <input
                        v-model="form.dp_amount"
                        type="number"
                        min="0"
                        :max="finalPrice"
                        required
                        @wheel.prevent
                        class="block w-full px-3 py-2 border border-purple-300 rounded-md focus:ring-purple-500 sm:text-sm"
                      />
                    </div>
                    <div>
                      <label class="block mb-1 text-sm font-bold text-gray-700"
                        >Tenor (Bulan)</label
                      >
                      <select
                        v-model="form.tenor"
                        required
                        class="block w-full px-3 py-2 bg-white border border-purple-300 rounded-md focus:ring-purple-500 sm:text-sm"
                      >
                        <option value="" disabled>-- Pilih Tenor --</option>
                        <option value="11">11 Bulan</option>
                        <option value="17">17 Bulan</option>
                        <option value="23">23 Bulan</option>
                        <option value="35">35 Bulan</option>
                      </select>
                    </div>
                  </div>

                  <div
                    v-if="form.tenor && form.dp_amount"
                    class="p-3 text-center bg-white border border-purple-200 rounded-lg shadow-sm"
                  >
                    <p
                      class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1"
                    >
                      Estimasi Cicilan (Flat 2%/bln)
                    </p>
                    <p class="text-2xl font-black text-purple-700">
                      {{ formatCurrency(estimatedInstallment) }}
                    </p>
                  </div>

                  <!-- UPLOAD DOKUMEN -->
                  <div class="pt-4 mt-2 border-t border-purple-200 space-y-4">
                    <div>
                      <label class="block text-sm font-bold text-gray-800"
                        >Upload KTP <span class="text-red-500">*</span></label
                      >
                      <input
                        type="file"
                        @change="handleKtpUpload"
                        accept="image/*,.pdf"
                        required
                        class="block w-full mt-1 text-sm text-gray-500 border border-gray-300 rounded-md file:mr-4 file:py-2 file:px-4 file:border-0 file:text-sm file:font-bold file:bg-purple-100 file:text-purple-700 hover:file:bg-purple-200"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-bold text-gray-800"
                        >Upload Kartu Keluarga (KK)
                        <span class="text-red-500">*</span></label
                      >
                      <input
                        type="file"
                        @change="handleKkUpload"
                        accept="image/*,.pdf"
                        required
                        class="block w-full mt-1 text-sm text-gray-500 border border-gray-300 rounded-md file:mr-4 file:py-2 file:px-4 file:border-0 file:text-sm file:font-bold file:bg-purple-100 file:text-purple-700 hover:file:bg-purple-200"
                      />
                    </div>
                  </div>
                </div>

                <!-- TOTAL FINAL -->
                <div
                  class="flex items-center justify-between p-5 mt-4 bg-gray-900 border border-gray-800 rounded-xl shadow-lg"
                >
                  <span class="text-sm font-bold text-gray-300"
                    >TOTAL HARGA:</span
                  >
                  <span class="text-3xl font-black text-green-400">{{
                    formatCurrency(finalPrice)
                  }}</span>
                </div>
              </div>
            </div>

            <div
              class="px-4 py-4 border-t border-gray-200 bg-gray-50 sm:px-6 sm:flex sm:flex-row-reverse"
            >
              <button
                type="submit"
                :disabled="
                  isSaving ||
                  isFetchingForm ||
                  !form.customer_id ||
                  !form.motorcycle_id
                "
                class="inline-flex justify-center w-full px-6 py-2 text-base font-bold text-white transition-colors bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
              >
                {{ isSaving ? "Menyimpan..." : "Simpan Transaksi" }}
              </button>
              <button
                type="button"
                @click="closeAddModal"
                class="inline-flex justify-center w-full px-6 py-2 mt-3 text-base font-medium text-gray-700 transition-colors bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50 sm:mt-0 sm:w-auto sm:text-sm"
              >
                Batal
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- MODAL UPDATE STATUS KREDIT -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 overflow-y-auto">
      <div
        class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:p-0"
      >
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75"
          @click="closeModal"
        ></div>
        <div
          class="inline-block w-full overflow-hidden text-left align-bottom transition-all transform bg-white shadow-xl rounded-xl sm:my-8 sm:align-middle sm:max-w-md"
        >
          <form @submit.prevent="handleUpdateStatus">
            <div class="px-4 pt-5 pb-4 bg-white sm:p-6 sm:pb-4">
              <h3 class="pb-3 mb-4 text-lg font-bold text-gray-900 border-b">
                Update Status Kredit
              </h3>
              <div
                class="p-4 mb-5 border border-gray-200 rounded-lg bg-gray-50"
              >
                <p class="text-xs text-gray-500 mb-1">
                  Invoice:
                  <span class="font-bold text-gray-900">{{
                    selectedSale?.invoice_number
                  }}</span>
                </p>
                <p class="text-xs text-gray-500">
                  Pelanggan:
                  <span class="font-bold text-gray-900">{{
                    selectedSale?.customer_name
                  }}</span>
                </p>
              </div>
              <div>
                <label class="block mb-2 text-sm font-bold text-gray-700"
                  >Pilih Status Baru</label
                >
                <select
                  v-model="newStatus"
                  required
                  class="block w-full border-2 border-blue-200 rounded-lg py-2.5 px-3 sm:text-sm font-bold bg-white focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="" disabled>-- Pilih Status --</option>
                  <option value="Pengajuan">1. Pengajuan Awal</option>
                  <option value="Verifikasi Data">2. Verifikasi Dokumen</option>
                  <option value="Proses">3. Sedang Diproses Leasing</option>
                  <option value="Disetujui">4. ✅ Disetujui (Final)</option>
                  <option value="Ditolak">5. ❌ Ditolak (Final)</option>
                </select>
              </div>
            </div>
            <div
              class="px-4 py-3 border-t border-gray-200 bg-gray-50 sm:px-6 sm:flex sm:flex-row-reverse"
            >
              <button
                type="submit"
                :disabled="isSaving"
                class="inline-flex justify-center w-full px-6 py-2 font-bold text-white bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
              >
                Simpan Status
              </button>
              <button
                type="button"
                @click="closeModal"
                class="inline-flex justify-center w-full px-6 py-2 mt-3 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 sm:mt-0 sm:w-auto sm:text-sm"
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
import { ref, onMounted, onUnmounted, computed } from "vue";
import api from "../../services/api";

const sales = ref([]);
const isLoading = ref(true);

// State Modal Status
const isModalOpen = ref(false);
const selectedSale = ref(null);
const newStatus = ref("");

// State Modal Tambah Transaksi
const isAddModalOpen = ref(false);
const isFetchingForm = ref(false);
const isSaving = ref(false);
const customers = ref([]);
const motors = ref([]);

const form = ref({
  customer_id: "",
  motorcycle_id: "",
  payment_type: "Cash",
  is_deal_price: false,
  deal_price: 0,
  dp_amount: 0,
  tenor: "",
});

// File Uploads
const ktpFile = ref(null);
const kkFile = ref(null);
const handleKtpUpload = (e) => (ktpFile.value = e.target.files[0]);
const handleKkUpload = (e) => (kkFile.value = e.target.files[0]);

const selectedMotorPrice = ref(0);

const finalPrice = computed(() => {
  return form.value.is_deal_price && form.value.deal_price > 0
    ? form.value.deal_price
    : selectedMotorPrice.value;
});

const formatCurrency = (value) => {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    minimumFractionDigits: 0,
  }).format(value || 0);
};

const formatDate = (dateString) => {
  if (!dateString) return "-";
  return new Date(dateString).toLocaleDateString("id-ID", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
};

const updateSelectedMotor = () => {
  const motor = motors.value.find((m) => m.id === form.value.motorcycle_id);
  selectedMotorPrice.value = motor ? motor.price : 0;
  // Reset deal price jika motor ganti
  form.value.deal_price = selectedMotorPrice.value;
};

// Estimasi cicilan
const estimatedInstallment = computed(() => {
  if (form.value.payment_type !== "Kredit" || !form.value.tenor) return 0;
  const pokokHutang = finalPrice.value - form.value.dp_amount;
  if (pokokHutang <= 0) return 0;

  const bungaPerBulan = pokokHutang * 0.02; // 2% flat
  const cicilanPokok = pokokHutang / parseInt(form.value.tenor);
  return Math.round(cicilanPokok + bungaPerBulan);
});

const getStatusBadgeClass = (status) => {
  switch (status) {
    case "Selesai":
    case "Disetujui":
      return "bg-green-100 text-green-800 border-green-200";
    case "Pengajuan":
      return "bg-yellow-100 text-yellow-800 border-yellow-200";
    case "Verifikasi Data":
      return "bg-blue-100 text-blue-800 border-blue-200";
    case "Proses":
      return "bg-purple-100 text-purple-800 border-purple-200";
    case "Ditolak":
      return "bg-red-100 text-red-800 border-red-200";
    default:
      return "bg-gray-100 text-gray-800 border-gray-200";
  }
};

// ==========================================
// LOGIKA COMBOBOX PENCARIAN (PELANGGAN & MOTOR)
// ==========================================
const customerSearchTerm = ref("");
const showCustomerDropdown = ref(false);

const motorSearchTerm = ref("");
const showMotorDropdown = ref(false);

// Filter Pelanggan Berdasarkan Inputan
const filteredCustomers = computed(() => {
  if (!customerSearchTerm.value) return customers.value;
  const q = customerSearchTerm.value.toLowerCase();
  return customers.value.filter(
    (c) => c.name.toLowerCase().includes(q) || c.nik.toLowerCase().includes(q),
  );
});

// Filter Motor Berdasarkan Inputan
const filteredMotors = computed(() => {
  if (!motorSearchTerm.value) return motors.value;
  const q = motorSearchTerm.value.toLowerCase();
  return motors.value.filter((m) => m.name.toLowerCase().includes(q));
});

// Aksi Saat Item Dipilih
const selectCustomer = (customer) => {
  form.value.customer_id = customer.id;
  customerSearchTerm.value = `${customer.name} (NIK: ${customer.nik})`;
  showCustomerDropdown.value = false;
};

const selectMotor = (motor) => {
  form.value.motorcycle_id = motor.id;
  motorSearchTerm.value = `${motor.name}`;
  showMotorDropdown.value = false;
  updateSelectedMotor(); // Hitung ulang harga
};

// Fungsi Helper untuk menyembunyikan dropdown dengan delay sedikit
// agar klik pada list bisa terdaftar sebelum dropdown hilang
const hideCustomerDropdown = () => {
  setTimeout(() => (showCustomerDropdown.value = false), 150);
};
const hideMotorDropdown = () => {
  setTimeout(() => (showMotorDropdown.value = false), 150);
};

// Modifikasi Fungsi openAddModal agar mereset searchTerm
const openAddModal = async () => {
  isAddModalOpen.value = true;
  isFetchingForm.value = true;
  form.value = {
    customer_id: "",
    motorcycle_id: "",
    payment_type: "Cash",
    is_deal_price: false,
    deal_price: 0,
    dp_amount: 0,
    tenor: "",
  };

  // Reset Pencarian
  customerSearchTerm.value = "";
  motorSearchTerm.value = "";
  showCustomerDropdown.value = false;
  showMotorDropdown.value = false;

  selectedMotorPrice.value = 0;
  ktpFile.value = null;
  kkFile.value = null;

  try {
    const branchId = localStorage.getItem("selected_branch_id") || "";
    const response = await api.get(`/sales/form-data?branch_id=${branchId}`);
    customers.value = response.data.data.customers;
    motors.value = response.data.data.motors;
  } catch (error) {
    alert("Gagal mengambil data pelanggan/motor");
  } finally {
    isFetchingForm.value = false;
  }
};
// ==========================================

const fetchSales = async () => {
  isLoading.value = true;
  try {
    const branchId = localStorage.getItem("selected_branch_id") || "";
    const response = await api.get(`/sales/?branch_id=${branchId}`);
    sales.value = response.data.data;
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};

// Auto Refresh ketika Super Admin ganti cabang di Navbar
const handleBranchChange = () => fetchSales();

onMounted(() => {
  fetchSales();
  window.addEventListener("branchChanged", handleBranchChange);
});
onUnmounted(() => {
  window.removeEventListener("branchChanged", handleBranchChange);
});

const closeAddModal = () => (isAddModalOpen.value = false);

const handleSubmitSale = async () => {
  isSaving.value = true;
  try {
    const formData = new FormData();
    formData.append("customer_id", form.value.customer_id);
    formData.append("motorcycle_id", form.value.motorcycle_id);
    formData.append("payment_type", form.value.payment_type);

    // Fitur Nego
    formData.append("is_deal_price", form.value.is_deal_price);
    if (form.value.is_deal_price) {
      formData.append("deal_price", form.value.deal_price);
    }

    // Fitur Kredit
    if (form.value.payment_type === "Kredit") {
      formData.append("dp_amount", form.value.dp_amount);
      formData.append("tenor", form.value.tenor);
      formData.append("installment_amount", estimatedInstallment.value);

      if (ktpFile.value) formData.append("ktp_image", ktpFile.value);
      if (kkFile.value) formData.append("kk_image", kkFile.value);
    }

    await api.post("/sales/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    closeAddModal();
    fetchSales();
    alert("Transaksi berhasil disimpan! Stok berkurang.");
  } catch (error) {
    alert(error.response?.data?.message || "Gagal menyimpan transaksi");
  } finally {
    isSaving.value = false;
  }
};

const openStatusModal = (sale) => {
  selectedSale.value = sale;
  newStatus.value = sale.status;
  isModalOpen.value = true;
};
const closeModal = () => (isModalOpen.value = false);

const handleUpdateStatus = async () => {
  isSaving.value = true;
  try {
    await api.put(`/sales/${selectedSale.value.id}/status`, {
      status: newStatus.value,
    });
    closeModal();
    fetchSales();
  } catch (error) {
    alert("Gagal mengubah status");
  } finally {
    isSaving.value = false;
  }
};

const searchQuery = ref("");
const paymentFilter = ref("All");

const filteredSales = computed(() => {
  let result = sales.value;
  if (paymentFilter.value !== "All") {
    result = result.filter((sale) => sale.payment_type === paymentFilter.value);
  }
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter((sale) => {
      return (
        sale.invoice_number.toLowerCase().includes(query) ||
        sale.customer_name.toLowerCase().includes(query) ||
        sale.motor_name.toLowerCase().includes(query) ||
        sale.status.toLowerCase().includes(query)
      );
    });
  }
  return result;
});
</script>
