<template>
  <div>
    <!-- HEADER & FILTER -->
    <div
      class="flex flex-col items-start justify-between gap-5 mb-6 xl:flex-row xl:items-center"
    >
      <!-- Judul -->
      <div class="shrink-0">
        <h1 class="text-2xl font-bold text-gray-900">
          Manajemen Stok Kendaraan
        </h1>
        <p class="mt-1 text-sm text-gray-500">
          Kelola katalog, harga modal, perbaikan, dan ketersediaan stok.
        </p>
      </div>

      <!-- Kumpulan Filter & Tombol (Sudah Responsif) -->
      <div
        class="flex flex-wrap items-center w-full gap-3 xl:w-auto justify-start xl:justify-end"
      >
        <!-- FILTER SUMBER KENDARAAN -->
        <select
          v-model="sourceFilter"
          @change="fetchMotorcycles"
          class="block w-full px-3 py-2.5 text-sm font-bold text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm cursor-pointer focus:ring-blue-500 focus:border-blue-500 sm:w-auto"
        >
          <option value="all">Semua Sumber</option>
          <option value="internal">Milik Abu Motor</option>
          <option value="external">Titipan Seller</option>
        </select>

        <!-- FILTER STATUS -->
        <select
          v-model="statusFilter"
          class="block w-full px-3 py-2.5 text-sm font-bold text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm cursor-pointer focus:ring-blue-500 focus:border-blue-500 sm:w-auto"
        >
          <option value="active">Katalog Aktif</option>
          <option value="archived">Arsip (Nonaktif)</option>
        </select>

        <!-- PENCARIAN -->
        <div class="relative w-full sm:flex-1 md:w-56 xl:w-64 shrink-0">
          <input
            v-model="searchQuery"
            @keyup.enter="fetchMotorcycles"
            type="text"
            placeholder="Cari model kendaraan (Enter)..."
            class="block w-full py-2.5 pl-3 pr-3 leading-5 placeholder-gray-500 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>

        <!-- TOMBOL TAMBAH -->
        <button
          v-if="['super_admin', 'cs', 'admin_cabang'].includes(userRole)"
          @click="openModal()"
          class="flex items-center justify-center w-full gap-2 px-5 py-2.5 text-sm font-medium text-white transition-colors bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700 sm:w-auto shrink-0 whitespace-nowrap"
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
              d="M12 4v16m8-8H4"
            />
          </svg>
          Tambah Kendaraan
        </button>
      </div>
    </div>

    <!-- TABEL INVENTORY -->
    <div
      class="overflow-hidden bg-white border border-gray-200 shadow-sm rounded-xl"
    >
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr></tr>
            <tr>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Unit
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Merek & Tipe
              </th>

              <!-- TAMBAHKAN KOLOM SUMBER DI SINI -->
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Sumber
              </th>

              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Status & Usia
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Harga OTR
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Stok
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
                Memuat data...
              </td>
            </tr>
            <tr
              v-else-if="filteredMotorcycles.length === 0"
              class="text-center"
            >
              <td colspan="6" class="px-6 py-12 text-sm text-gray-500">
                Tidak ada kendaraan yang ditemukan.
              </td>
            </tr>
            <tr
              v-else
              v-for="motor in filteredMotorcycles"
              :key="motor.id"
              class="transition-colors hover:bg-gray-50"
            >
              <!-- Kolom Foto & Unit -->
              <td class="flex items-center gap-4 px-6 py-4 whitespace-nowrap">
                <div
                  class="w-12 h-12 overflow-hidden border border-gray-200 rounded-md bg-gray-50 shrink-0"
                >
                  <img
                    v-if="motor.image_url"
                    :src="getImageUrl(motor.image_url)"
                    class="object-cover w-full h-full"
                  />
                </div>
                <div>
                  <div class="text-sm font-bold text-gray-900">
                    {{ motor.model_name }}
                  </div>
                  <div class="text-xs text-gray-500">{{ motor.sku_code }}</div>
                </div>
              </td>

              <!-- Kolom Merek & Tipe -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-bold text-gray-900">
                  {{ motor.brand }}
                </div>
                <div class="flex items-center gap-1 mt-1">
                  <span
                    class="px-2 py-0.5 text-[10px] font-bold text-blue-800 bg-blue-100 rounded uppercase"
                    >{{ motor.vehicle_type }}</span
                  >
                  <span
                    class="px-2 py-0.5 text-[10px] font-bold text-gray-600 bg-gray-100 rounded uppercase"
                    >{{ motor.condition }}</span
                  >
                </div>
              </td>
              <!-- KOLOM SUMBER -->
              <td class="px-6 py-4 whitespace-nowrap">
                <!-- Cek jika ada nama seller DAN namanya BUKAN "abu motor" atau "admin" -->
                <div
                  v-if="
                    motor.seller_name &&
                    !motor.seller_name.toLowerCase().includes('abu') &&
                    !motor.seller_name.toLowerCase().includes('admin')
                  "
                  class="flex flex-col items-start gap-1"
                >
                  <span
                    class="px-2 py-0.5 text-[10px] font-bold text-purple-800 bg-purple-100 border border-purple-200 rounded uppercase"
                    >Titipan Seller</span
                  >
                  <span class="text-xs font-medium text-gray-600"
                    >@{{ motor.seller_name }}</span
                  >
                </div>

                <!-- Jika tidak ada nama seller, ATAU yang input adalah admin/Abu Motor -->
                <div v-else class="flex flex-col items-start gap-1">
                  <span
                    class="px-2 py-0.5 text-[10px] font-bold text-blue-800 bg-blue-100 border border-blue-200 rounded uppercase"
                    >Internal</span
                  >
                  <span class="text-xs font-medium text-gray-600"
                    >Abu Motor</span
                  >
                </div>
              </td>

              <!-- Kolom Status & Peringatan Usia (>2 Bulan) -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-xs font-semibold text-gray-800 mb-1">
                  Masuk: {{ motor.incoming_date || "-" }}
                </div>
                <span
                  v-if="motor.is_overstock"
                  class="px-2 py-1 text-xs font-bold text-red-800 bg-red-100 rounded-md animate-pulse"
                >
                  ⚠ Wajib Jual (>2 Bulan)
                </span>
                <span
                  v-else
                  class="px-2 py-1 text-xs font-bold text-green-800 bg-green-100 rounded-md"
                  >Stok Aman</span
                >
              </td>

              <!-- Kolom Harga -->
              <td
                class="px-6 py-4 text-sm font-medium text-gray-900 whitespace-nowrap"
              >
                {{ formatCurrency(motor.price) }}
              </td>

              <!-- Kolom Stok -->
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="px-2.5 py-1 text-xs font-semibold rounded-full"
                  :class="
                    motor.stock > 0
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  "
                >
                  {{ motor.stock }} Unit
                </span>
              </td>

              <!-- Kolom Aksi -->
              <!-- Kolom Aksi -->
              <td
                class="px-6 py-4 text-sm font-medium text-right whitespace-nowrap"
              >
                <!-- Tombol Edit (Selalu Muncul) -->
                <button
                  v-if="
                    ['super_admin', 'cs', 'admin_cabang'].includes(userRole)
                  "
                  @click="openModal(motor)"
                  class="mr-3 text-blue-600 transition-colors hover:text-blue-900"
                >
                  Edit
                </button>

                <!-- Tombol Arsipkan (Jika masih aktif) -->
                <button
                  v-if="
                    motor.is_active &&
                    ['super_admin', 'cs', 'admin_cabang'].includes(userRole)
                  "
                  @click="handleDelete(motor.id)"
                  class="text-red-600 transition-colors hover:text-red-900"
                >
                  Arsipkan
                </button>

                <!-- Tombol Publish Ulang (Jika sedang diarsipkan) -->
                <button
                  v-if="
                    !motor.is_active &&
                    ['super_admin', 'cs', 'admin_cabang'].includes(userRole)
                  "
                  @click="handleRepublish(motor.id)"
                  class="text-green-600 transition-colors hover:text-green-900 font-bold"
                >
                  <svg
                    class="w-4 h-4 inline-block mr-1"
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
                  Publish Ulang
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL FORM -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 overflow-y-auto">
      <div
        class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:p-0"
      >
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75"
          @click="closeModal"
        ></div>
        <div
          class="inline-block w-full overflow-hidden text-left align-bottom transition-all transform bg-white shadow-xl rounded-xl sm:my-8 sm:align-middle sm:max-w-4xl"
        >
          <form @submit.prevent="handleSubmit">
            <div
              class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4 max-h-[80vh] overflow-y-auto"
            >
              <h3 class="pb-3 mb-6 text-xl font-bold text-gray-900 border-b">
                {{ isEditMode ? "Edit Kendaraan" : "Tambah Kendaraan Baru" }}
              </h3>

              <div class="space-y-6">
                <!-- BAGIAN 1: INFORMASI UTAMA -->
                <div
                  class="p-5 border border-gray-100 rounded-xl bg-slate-50/30"
                >
                  <h4
                    class="flex items-center gap-2 pb-3 mb-5 text-sm font-bold text-gray-800 uppercase border-b border-gray-200"
                  >
                    <svg
                      class="w-4 h-4 text-gray-500"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                      ></path>
                    </svg>
                    1. Informasi Utama
                  </h4>
                  <div class="grid grid-cols-1 gap-5 md:grid-cols-2">
                    <div v-if="userRole === 'super_admin'">
                      <label class="block text-sm font-semibold text-red-600"
                        >Cabang (Wajib untuk Owner)</label
                      >
                      <select
                        v-model="form.branch_id"
                        class="block w-full px-3 py-2.5 mt-1.5 border border-red-200 rounded-lg sm:text-sm bg-red-50/50 focus:ring-red-500 focus:border-red-500 transition-colors"
                      >
                        <option value="">-- Pilih Cabang --</option>
                        <option
                          v-for="b in masterBranches"
                          :key="b.id"
                          :value="b.id"
                        >
                          {{ b.name }}
                        </option>
                      </select>
                    </div>

                    <div>
                      <label class="block text-sm font-semibold text-gray-700"
                        >Tipe Kendaraan</label
                      >
                      <select
                        v-model="form.vehicle_type"
                        class="block w-full px-3 py-2.5 mt-1.5 font-bold text-blue-700 bg-blue-50/50 border border-blue-200 rounded-lg sm:text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors"
                      >
                        <option value="Motor">Sepeda Motor</option>
                        <option value="Mobil">Mobil</option>
                      </select>
                    </div>

                    <div class="grid grid-cols-2 gap-4">
                      <div>
                        <label class="block text-sm font-semibold text-gray-700"
                          >Kondisi</label
                        >
                        <select
                          v-model="form.condition"
                          class="block w-full px-3 py-2.5 mt-1.5 border border-gray-300 rounded-lg sm:text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors"
                        >
                          <option value="Baru">Baru</option>
                          <option value="Bekas">Bekas</option>
                        </select>
                      </div>
                      <div>
                        <label class="block text-sm font-semibold text-gray-700"
                          >Kode SKU</label
                        >
                        <input
                          v-model="form.sku_code"
                          type="text"
                          required
                          class="block w-full px-3 py-2.5 mt-1.5 border border-gray-200 rounded-lg bg-gray-100 text-gray-500 sm:text-sm"
                          :disabled="isEditMode"
                        />
                      </div>
                    </div>

                    <div>
                      <label class="block text-sm font-semibold text-gray-700"
                        >Merek Kendaraan</label
                      >
                      <select
                        v-model="form.brand_id"
                        required
                        class="block w-full px-3 py-2.5 mt-1.5 border border-gray-300 rounded-lg sm:text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors"
                      >
                        <option value="">-- Pilih Merek --</option>
                        <option
                          v-for="b in masterBrands"
                          :key="b.id"
                          :value="b.id"
                        >
                          {{ b.name }}
                        </option>
                      </select>
                    </div>

                    <div class="grid grid-cols-2 gap-4">
                      <div>
                        <label class="block text-sm font-semibold text-gray-700"
                          >Nama Model</label
                        >
                        <select
                          v-model="form.model_name"
                          required
                          class="block w-full px-3 py-2.5 mt-1.5 border border-gray-300 rounded-lg sm:text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors"
                          :disabled="!form.brand_id"
                        >
                          <option value="">-- Pilih Model --</option>
                          <option
                            v-for="m in availableModels"
                            :key="m.id"
                            :value="m.name"
                          >
                            {{ m.name }}
                          </option>
                        </select>
                      </div>
                      <div>
                        <label class="block text-sm font-semibold text-gray-700"
                          >Kategori</label
                        >
                        <select
                          v-model="form.category_id"
                          required
                          class="block w-full px-3 py-2.5 mt-1.5 border border-gray-300 rounded-lg sm:text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors"
                        >
                          <option value="">-- Pilih Kategori --</option>
                          <option
                            v-for="c in masterCategories"
                            :key="c.id"
                            :value="c.id"
                          >
                            {{ c.name }}
                          </option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- BAGIAN 2: KEUANGAN & MONITORING -->
                <div
                  class="p-5 border border-purple-100 rounded-xl bg-purple-50/20"
                >
                  <h4
                    class="flex items-center gap-2 pb-3 mb-5 text-sm font-bold text-purple-800 uppercase border-b border-purple-200/50"
                  >
                    <svg
                      class="w-4 h-4 text-purple-500"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                      ></path>
                    </svg>
                    2. Keuangan & Monitoring
                  </h4>
                  <div class="grid grid-cols-1 gap-5 md:grid-cols-3">
                    <div>
                      <label class="block text-sm font-semibold text-gray-700"
                        >Tanggal Masuk</label
                      >
                      <input
                        v-model="form.incoming_date"
                        type="date"
                        required
                        class="block w-full px-3 py-2.5 mt-1.5 border border-gray-300 rounded-lg sm:text-sm focus:ring-purple-500 focus:border-purple-500 transition-colors"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-semibold text-gray-700"
                        >Harga Modal (Rp)</label
                      >
                      <input
                        v-model="form.capital_price"
                        type="number"
                        min="0"
                        required
                        @wheel.prevent
                        class="block w-full px-3 py-2.5 mt-1.5 border border-gray-300 rounded-lg sm:text-sm focus:ring-purple-500 focus:border-purple-500 transition-colors"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-semibold text-gray-700"
                        >Biaya Perbaikan (Rp)</label
                      >
                      <input
                        v-model="form.repair_cost"
                        type="number"
                        min="0"
                        @wheel.prevent
                        class="block w-full px-3 py-2.5 mt-1.5 border border-gray-300 rounded-lg sm:text-sm focus:ring-purple-500 focus:border-purple-500 transition-colors"
                      />
                    </div>

                    <div class="md:col-span-2">
                      <label class="block text-sm font-bold text-blue-800"
                        >Harga Jual OTR (Rp)</label
                      >
                      <input
                        v-model="form.price"
                        type="number"
                        min="0"
                        required
                        @wheel.prevent
                        class="block w-full px-4 py-3 mt-1.5 font-bold text-lg text-blue-900 border-2 border-blue-200 rounded-lg bg-blue-50/40 focus:ring-blue-500 focus:border-blue-500 transition-all"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-bold text-gray-800"
                        >Stok Unit Tersedia</label
                      >
                      <input
                        v-model="form.stock"
                        type="number"
                        min="0"
                        required
                        @wheel.prevent
                        class="block w-full px-4 py-3 mt-1.5 font-bold text-lg border-2 border-gray-200 rounded-lg bg-white focus:ring-blue-500 focus:border-blue-500 transition-all"
                      />
                    </div>
                  </div>
                </div>

                <!-- BAGIAN 3: SPESIFIKASI & FOTO -->
                <div
                  class="p-5 border border-gray-100 rounded-xl bg-slate-50/30"
                >
                  <h4
                    class="flex items-center gap-2 pb-3 mb-5 text-sm font-bold text-gray-800 uppercase border-b border-gray-200"
                  >
                    <svg
                      class="w-4 h-4 text-gray-500"
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
                    3. Spesifikasi Teknis & Galeri
                  </h4>

                  <div
                    class="p-5 mb-8 bg-white border border-gray-200 shadow-sm rounded-xl"
                  >
                    <div class="grid grid-cols-1 gap-8 md:grid-cols-2">
                      <!-- FOTO UTAMA (STACK MAKS 1) -->
                      <div>
                        <label
                          class="block mb-2 text-sm font-bold text-gray-800"
                        >
                          Foto Utama
                          <span class="font-normal text-gray-500"
                            >(Maks 1 Gambar)</span
                          >
                        </label>
                        <div class="flex flex-wrap items-start gap-4">
                          <!-- Previews -->
                          <div
                            v-if="mainPhotoPreview"
                            class="relative group w-28 h-28"
                          >
                            <img
                              :src="mainPhotoPreview"
                              class="object-cover w-full h-full border-2 border-blue-300 shadow-md rounded-xl"
                            />
                            <button
                              type="button"
                              @click="removeMainPhoto"
                              class="absolute flex items-center justify-center w-8 h-8 text-white transition-all bg-red-500 border-2 border-white rounded-full shadow-lg opacity-0 -top-3 -right-3 group-hover:opacity-100 hover:bg-red-600 scale-90 group-hover:scale-100"
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
                                  stroke-width="3"
                                  d="M6 18L18 6M6 6l12 12"
                                ></path>
                              </svg>
                            </button>
                            <div
                              class="absolute bottom-0 w-full text-center bg-black/60 text-white text-[10px] py-1 rounded-b-xl font-bold tracking-wider"
                            >
                              UTAMA
                            </div>
                          </div>

                          <!-- Box Tambah -->
                          <label
                            @click="checkMainPhotoLimit"
                            class="flex flex-col items-center justify-center border-2 border-gray-300 border-dashed cursor-pointer w-28 h-28 rounded-xl hover:bg-blue-50 hover:border-blue-300 transition-colors"
                            :class="{
                              'opacity-50 cursor-not-allowed bg-gray-100':
                                mainPhotoPreview,
                            }"
                          >
                            <svg
                              class="w-8 h-8 mb-2 text-gray-400"
                              :class="{ 'text-blue-400': !mainPhotoPreview }"
                              fill="none"
                              stroke="currentColor"
                              viewBox="0 0 24 24"
                            >
                              <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                              ></path>
                            </svg>
                            <span
                              class="text-xs font-bold"
                              :class="
                                mainPhotoPreview
                                  ? 'text-gray-400'
                                  : 'text-blue-600'
                              "
                              >Upload</span
                            >
                            <input
                              type="file"
                              ref="mainPhotoInput"
                              @change="handleMainPhoto"
                              accept="image/*"
                              class="hidden"
                              :disabled="mainPhotoPreview"
                            />
                          </label>
                        </div>
                      </div>

                      <!-- FOTO GALERI (STACK MAKS 9) -->
                      <div>
                        <label
                          class="block mb-2 text-sm font-bold text-gray-800"
                        >
                          Foto Galeri Tambahan
                          <span class="font-normal text-gray-500"
                            >(Maks 9 Gambar)</span
                          >
                        </label>
                        <div class="flex flex-wrap items-start gap-4">
                          <!-- Box Previews -->
                          <div
                            v-for="(item, index) in galleryPhotosPreview"
                            :key="index"
                            class="relative group w-20 h-20"
                          >
                            <img
                              :src="item.url"
                              class="object-cover w-full h-full border-2 border-gray-200 shadow-sm rounded-xl"
                            />
                            <button
                              type="button"
                              @click="removeGalleryPhoto(index)"
                              class="absolute flex items-center justify-center w-6 h-6 text-white transition-all bg-red-500 border-2 border-white rounded-full shadow-lg opacity-0 -top-2 -right-2 group-hover:opacity-100 hover:bg-red-600 scale-90 group-hover:scale-100"
                            >
                              <svg
                                class="w-3 h-3"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                              >
                                <path
                                  stroke-linecap="round"
                                  stroke-linejoin="round"
                                  stroke-width="3"
                                  d="M6 18L18 6M6 6l12 12"
                                ></path>
                              </svg>
                            </button>
                            <!-- Indikator gambar baru -->
                            <div
                              v-if="!item.isExisting"
                              class="absolute bottom-0 w-full text-center bg-green-500/80 text-white text-[9px] py-0.5 rounded-b-xl font-bold"
                            >
                              Baru
                            </div>
                          </div>

                          <!-- Box Tambah Galeri -->
                          <label
                            @click="checkGalleryLimit"
                            class="flex flex-col items-center justify-center border-2 border-gray-300 border-dashed cursor-pointer w-20 h-20 rounded-xl hover:bg-gray-50 hover:border-gray-400 transition-colors"
                            :class="{
                              'opacity-50 cursor-not-allowed bg-gray-100':
                                galleryPhotosPreview.length >= 9,
                            }"
                          >
                            <svg
                              class="w-6 h-6 mb-1 text-gray-400"
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
                            <span class="text-[10px] font-bold text-gray-500"
                              >Tambah</span
                            >
                            <input
                              type="file"
                              ref="galleryInput"
                              @change="handleGalleryPhotos"
                              accept="image/*"
                              multiple
                              class="hidden"
                              :disabled="galleryPhotosPreview.length >= 9"
                            />
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Spesifikasi Lengkap -->
                  <div class="grid grid-cols-1 gap-5 md:grid-cols-3">
                    <div>
                      <label class="block text-sm font-semibold text-gray-700"
                        >Warna</label
                      >
                      <input
                        v-model="form.color"
                        type="text"
                        class="block w-full px-3 py-2.5 mt-1.5 border border-gray-300 rounded-lg sm:text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-semibold text-gray-700"
                        >Transmisi</label
                      >
                      <select
                        v-model="form.transmission"
                        class="block w-full px-3 py-2.5 mt-1.5 bg-white border border-gray-300 rounded-lg sm:text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors"
                      >
                        <option value="Otomatis">Otomatis (AT/CVT)</option>
                        <option value="Manual">Manual (MT)</option>
                      </select>
                    </div>
                    <div>
                      <label class="block text-sm font-semibold text-gray-700"
                        >Tahun Produksi</label
                      >
                      <input
                        v-model="form.year"
                        type="number"
                        min="1990"
                        @wheel.prevent
                        class="block w-full px-3 py-2.5 mt-1.5 border border-gray-300 rounded-lg sm:text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-semibold text-gray-700"
                        >Jarak Tempuh</label
                      >
                      <input
                        v-model="form.mileage"
                        type="text"
                        placeholder="Cont. 5000 km"
                        class="block w-full px-3 py-2.5 mt-1.5 border border-gray-300 rounded-lg sm:text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-semibold text-gray-700"
                        >Tipe Bodi</label
                      >
                      <input
                        v-model="form.body_type"
                        type="text"
                        placeholder="Cont. Hatchback"
                        class="block w-full px-3 py-2.5 mt-1.5 border border-gray-300 rounded-lg sm:text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-semibold text-gray-700"
                        >Kapasitas Mesin</label
                      >
                      <input
                        v-model="form.engine_capacity"
                        type="text"
                        placeholder="Cont. 150 cc"
                        class="block w-full px-3 py-2.5 mt-1.5 border border-gray-300 rounded-lg sm:text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors"
                      />
                    </div>
                  </div>

                  <div class="mt-5">
                    <label class="block text-sm font-semibold text-gray-700"
                      >Fitur Unggulan
                      <span class="font-normal text-gray-500"
                        >(Pisahkan koma)</span
                      ></label
                    >
                    <input
                      v-model="form.features"
                      type="text"
                      placeholder="Contoh: Lampu LED, Smart Key, ABS"
                      class="block w-full px-3 py-2.5 mt-1.5 border border-gray-300 rounded-lg sm:text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    />
                  </div>

                  <div class="mt-6">
                    <label
                      class="block mb-3 text-sm font-semibold text-gray-700"
                      >Kelengkapan Dokumen</label
                    >
                    <div class="grid grid-cols-2 gap-3 md:grid-cols-4">
                      <label
                        class="flex items-center p-3 transition-colors border border-gray-200 cursor-pointer rounded-xl bg-white hover:bg-blue-50 hover:border-blue-200"
                      >
                        <input
                          type="checkbox"
                          v-model="form.documents"
                          value="BPKB"
                          class="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span class="ml-3 text-sm font-medium text-gray-800"
                          >BPKB</span
                        >
                      </label>
                      <label
                        class="flex items-center p-3 transition-colors border border-gray-200 cursor-pointer rounded-xl bg-white hover:bg-blue-50 hover:border-blue-200"
                      >
                        <input
                          type="checkbox"
                          v-model="form.documents"
                          value="STNK"
                          class="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span class="ml-3 text-sm font-medium text-gray-800"
                          >STNK</span
                        >
                      </label>
                      <label
                        class="flex items-center p-3 transition-colors border border-gray-200 cursor-pointer rounded-xl bg-white hover:bg-blue-50 hover:border-blue-200"
                      >
                        <input
                          type="checkbox"
                          v-model="form.documents"
                          value="Faktur"
                          class="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span class="ml-3 text-sm font-medium text-gray-800"
                          >Faktur</span
                        >
                      </label>
                      <label
                        class="flex items-center p-3 transition-colors border border-gray-200 cursor-pointer rounded-xl bg-white hover:bg-blue-50 hover:border-blue-200"
                      >
                        <input
                          type="checkbox"
                          v-model="form.documents"
                          value="Buku Garansi"
                          class="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span class="ml-3 text-sm font-medium text-gray-800"
                          >Garansi</span
                        >
                      </label>
                    </div>
                  </div>

                  <div class="mt-5">
                    <label class="block text-sm font-semibold text-gray-700"
                      >Deskripsi Kendaraan</label
                    >
                    <textarea
                      v-model="form.description"
                      rows="4"
                      placeholder="Tuliskan keterangan tambahan kondisi kendaraan..."
                      class="block w-full px-3 py-3 mt-1.5 border border-gray-300 rounded-lg sm:text-sm focus:ring-blue-500 focus:border-blue-500 transition-colors resize-none"
                    ></textarea>
                  </div>
                </div>
              </div>
            </div>

            <div
              class="px-4 py-3 border-t border-gray-200 bg-gray-50 sm:px-6 sm:flex sm:flex-row-reverse"
            >
              <button
                type="submit"
                :disabled="isSaving"
                class="inline-flex justify-center w-full px-6 py-2 text-base font-medium text-white bg-blue-600 rounded-md shadow-sm hover:bg-blue-700 sm:ml-3 sm:w-auto sm:text-sm"
              >
                {{ isSaving ? "Menyimpan..." : "Simpan Data" }}
              </button>
              <button
                type="button"
                @click="closeModal"
                class="inline-flex justify-center w-full px-6 py-2 mt-3 text-base font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm sm:mt-0 sm:w-auto sm:text-sm"
              >
                Batal
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- MODAL KONFIRMASI CUSTOM -->
    <div v-if="isConfirmModalOpen" class="fixed inset-0 z-[60] overflow-y-auto">
      <div
        class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:p-0"
      >
        <div
          class="fixed inset-0 transition-opacity bg-gray-800 bg-opacity-75 backdrop-blur-sm"
          @click="closeConfirmModal"
        ></div>
        <div
          class="inline-block w-full max-w-md p-6 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
        >
          <div class="flex items-center gap-4 mb-5">
            <div
              class="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-full shrink-0"
            >
              <svg
                class="w-6 h-6 text-blue-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900">
                {{ confirmTitle }}
              </h3>
            </div>
          </div>
          <div
            class="p-4 mb-6 text-sm leading-relaxed text-gray-700 whitespace-pre-line border rounded-lg bg-gray-50 border-gray-200"
          >
            {{ confirmMessage }}
          </div>
          <div class="flex justify-end gap-3">
            <button
              @click="closeConfirmModal"
              class="w-full px-5 py-2.5 text-sm font-bold text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 sm:w-auto transition-colors"
            >
              Batal
            </button>
            <button
              @click="executeConfirmAction"
              :disabled="isConfirming"
              class="w-full px-5 py-2.5 text-sm font-bold text-white bg-blue-600 rounded-lg hover:bg-blue-700 sm:w-auto transition-colors disabled:opacity-70"
            >
              {{ isConfirming ? "Memproses..." : "Ya, Lanjutkan" }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from "vue";
import api from "../../services/api";

// ==========================================
// USER & ROLE STATE
// ==========================================
const userData = JSON.parse(localStorage.getItem("user_data") || "{}");
const userRole = ref(userData.role || "");

// ==========================================
// FILTER & SEARCH STATE
// ==========================================
const motorcycles = ref([]);
const isLoading = ref(false);
const searchQuery = ref("");
const statusFilter = ref("active");
const sourceFilter = ref("all");

// ==========================================
// MASTER DATA STATE
// ==========================================
const masterBrands = ref([]);
const masterCategories = ref([]);
const masterBranches = ref([]);

// ==========================================
// FORM & MODAL STATE
// ==========================================
const isModalOpen = ref(false);
const isEditMode = ref(false);
const isSaving = ref(false);
const currentId = ref(null);

// STATE FOTO STACKING
const selectedMainPhoto = ref(null);
const mainPhotoInput = ref(null);
const mainPhotoPreview = ref(null);

const galleryInput = ref(null);
// Format galleryPhotosPreview: [{ url: string, file: File|null, isExisting: boolean, existingUrl: string|null }]
const galleryPhotosPreview = ref([]);

const isConfirmModalOpen = ref(false);
const confirmTitle = ref("");
const confirmMessage = ref("");
const confirmAction = ref(null);
const isConfirming = ref(false);

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5001";

const form = ref({
  sku_code: "",
  branch_id: "",
  vehicle_type: "Motor",
  condition: "Bekas",
  brand_id: "",
  category_id: "",
  model_name: "",
  color: "",
  transmission: "Otomatis",
  year: new Date().getFullYear(),
  incoming_date: new Date().toISOString().split("T")[0],
  capital_price: 0,
  repair_cost: 0,
  price: 0,
  stock: 0,
  description: "",
  is_active: true,
  mileage: "0",
  body_type: "",
  engine_capacity: "",
  features: "",
  documents: [],
});

// Computed Data Filter Frontend
const filteredMotorcycles = computed(() => {
  return motorcycles.value.filter((motor) => {
    if (statusFilter.value === "active" && !motor.is_active) return false;
    if (statusFilter.value === "archived" && motor.is_active) return false;
    return true;
  });
});

const formatCurrency = (val) =>
  new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    minimumFractionDigits: 0,
  }).format(val);

const getImageUrl = (url) => (url ? `${BASE_URL}${url}` : null);

// ==========================================
// PENGAMBILAN DATA (API CALLS)
// ==========================================
const fetchMasterData = async () => {
  try {
    const [bRes, cRes, brRes] = await Promise.all([
      api.get("/master/brands"),
      api.get("/master/categories"),
      api.get("/master/branches"),
    ]);
    masterBrands.value = bRes.data.data;
    masterCategories.value = cRes.data.data;
    masterBranches.value = brRes.data.data;
  } catch (error) {
    console.error("Gagal load master data");
  }
};

const fetchMotorcycles = async () => {
  isLoading.value = true;
  try {
    const branchId = localStorage.getItem("selected_branch_id") || "";
    const response = await api.get(
      `/inventory/?q=${searchQuery.value}&branch_id=${branchId}&source=${sourceFilter.value}`,
    );
    motorcycles.value = response.data.data;
  } catch (error) {
    console.error("Gagal refresh data inventory", error);
  } finally {
    isLoading.value = false;
  }
};

const handleBranchChange = () => {
  fetchMotorcycles();
};

onMounted(() => {
  fetchMasterData();
  fetchMotorcycles();
  window.addEventListener("branchChanged", handleBranchChange);
});

onUnmounted(() => {
  window.removeEventListener("branchChanged", handleBranchChange);
});

// ==========================================
// FORM HANDLING & FOTO STACKING
// ==========================================
const checkMainPhotoLimit = (e) => {
  if (mainPhotoPreview.value) {
    e.preventDefault();
    alert(
      "Maksimal hanya upload 1 gambar utama. Jika ingin mengganti, klik tombol silang (X) pada gambar terlebih dahulu.",
    );
  }
};

const checkGalleryLimit = (e) => {
  if (galleryPhotosPreview.value.length >= 9) {
    e.preventDefault();
    alert(
      "Gambar tambahan maksimal 9. Hapus gambar lama jika ingin menambahkan yang baru.",
    );
  }
};

const handleMainPhoto = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedMainPhoto.value = file;
    mainPhotoPreview.value = URL.createObjectURL(file);
  }
  if (mainPhotoInput.value) mainPhotoInput.value.value = "";
};

const handleGalleryPhotos = (event) => {
  const files = Array.from(event.target.files);
  const availableSlots = 9 - galleryPhotosPreview.value.length;

  if (files.length > availableSlots) {
    alert(
      `Maksimal 9 gambar! Anda hanya memiliki sisa slot untuk ${availableSlots} gambar lagi. Beberapa gambar diabaikan.`,
    );
  }

  const filesToAdd = files.slice(0, availableSlots);
  filesToAdd.forEach((file) => {
    galleryPhotosPreview.value.push({
      url: URL.createObjectURL(file),
      file: file,
      isExisting: false,
      existingUrl: null,
    });
  });

  if (galleryInput.value) galleryInput.value.value = "";
};

const removeMainPhoto = () => {
  selectedMainPhoto.value = null;
  mainPhotoPreview.value = null;
};

const removeGalleryPhoto = (index) => {
  galleryPhotosPreview.value.splice(index, 1);
};

const generateSKU = () => {
  const prefix = form.value.vehicle_type === "Mobil" ? "CAR" : "MTR";
  return `${prefix}-${Math.floor(Math.random() * 90000) + 10000}`;
};

const openModal = (motor = null) => {
  isModalOpen.value = true;
  if (motor) {
    isEditMode.value = true;
    currentId.value = motor.id;

    // TAMPILKAN PREVIEW SAAT EDIT
    mainPhotoPreview.value = motor.image_url
      ? getImageUrl(motor.image_url)
      : null;

    if (motor.gallery && Array.isArray(motor.gallery)) {
      galleryPhotosPreview.value = motor.gallery.map((url) => ({
        url: getImageUrl(url),
        file: null,
        isExisting: true,
        existingUrl: url,
      }));
    } else {
      galleryPhotosPreview.value = [];
    }

    const matchedBrand = masterBrands.value.find((b) => b.name === motor.brand);
    const brandIdToSet = matchedBrand ? matchedBrand.id : "";

    const matchedCategory = masterCategories.value.find(
      (c) => c.name === motor.category,
    );
    const categoryIdToSet = matchedCategory ? matchedCategory.id : "";

    form.value = {
      ...motor,
      branch_id: motor.branch_id || "",
      vehicle_type: motor.vehicle_type || "Motor",
      condition: motor.condition || "Bekas",
      brand_id: brandIdToSet,
      category_id: categoryIdToSet,
      model_name: motor.model_name || "",
      transmission: motor.transmission || "Otomatis",
      year: motor.year || new Date().getFullYear(),
      mileage: motor.mileage || "0",
      body_type: motor.body_type || "",
      engine_capacity: motor.engine_capacity || "",
      features: motor.features || "",
      documents: motor.documents
        ? typeof motor.documents === "string"
          ? motor.documents.split(",")
          : motor.documents
        : [],
    };
  } else {
    isEditMode.value = false;
    currentId.value = null;
    selectedMainPhoto.value = null;
    mainPhotoPreview.value = null;
    galleryPhotosPreview.value = [];

    form.value = {
      sku_code: generateSKU(),
      branch_id: "",
      vehicle_type: "Motor",
      condition: "Bekas",
      brand_id: "",
      category_id: "",
      model_name: "",
      color: "",
      transmission: "Otomatis",
      year: new Date().getFullYear(),
      incoming_date: new Date().toISOString().split("T")[0],
      capital_price: 0,
      repair_cost: 0,
      price: 0,
      stock: 0,
      description: "",
      is_active: true,
      mileage: "0",
      body_type: "",
      engine_capacity: "",
      features: "",
      documents: [],
    };
  }
};

const closeModal = () => {
  isModalOpen.value = false;
  selectedMainPhoto.value = null;
  mainPhotoPreview.value = null;
  galleryPhotosPreview.value = [];
};

const handleSubmit = async () => {
  isSaving.value = true;
  try {
    const formData = new FormData();

    Object.keys(form.value).forEach((key) => {
      if (key === "documents" && Array.isArray(form.value[key])) {
        formData.append(key, form.value[key].join(","));
      } else if (form.value[key] !== null && form.value[key] !== undefined) {
        formData.append(key, form.value[key]);
      }
    });

    if (selectedMainPhoto.value) {
      formData.append("image", selectedMainPhoto.value);
    }

    const newGalleries = galleryPhotosPreview.value.filter(
      (item) => !item.isExisting && item.file,
    );
    newGalleries.forEach((item) => {
      formData.append("gallery", item.file);
    });

    const keptGalleries = galleryPhotosPreview.value
      .filter((item) => item.isExisting)
      .map((item) => item.existingUrl);
    formData.append("kept_galleries", JSON.stringify(keptGalleries));

    const config = {
      headers: { "Content-Type": "multipart/form-data" },
    };

    if (isEditMode.value) {
      await api.put(`/inventory/${currentId.value}`, formData, config);
    } else {
      await api.post("/inventory/", formData, config);
    }

    closeModal();
    fetchMotorcycles();
    alert("Berhasil disimpan!");
  } catch (error) {
    alert(error.response?.data?.message || "Gagal menyimpan data");
  } finally {
    isSaving.value = false;
  }
};

// ==========================================
// KONFIRMASI CUSTOM (HAPUS & PUBLISH)
// ==========================================
const closeConfirmModal = () => {
  isConfirmModalOpen.value = false;
  confirmAction.value = null;
};

const executeConfirmAction = async () => {
  if (typeof confirmAction.value === "function") {
    isConfirming.value = true;
    await confirmAction.value();
    isConfirming.value = false;
  }
};

const handleDelete = (id) => {
  confirmTitle.value = "Arsipkan Kendaraan";
  confirmMessage.value =
    "Apakah Anda yakin ingin mengarsipkan kendaraan ini? Kendaraan akan disembunyikan dari katalog publik dan stok menjadi 0.";

  confirmAction.value = async () => {
    try {
      await api.delete(`/inventory/${id}`);
      fetchMotorcycles();
      closeConfirmModal();
    } catch (err) {
      alert("Gagal mengarsipkan kendaraan.");
    }
  };

  isConfirmModalOpen.value = true;
};

const handleRepublish = (id) => {
  confirmTitle.value = "Publish Ulang Kendaraan";
  confirmMessage.value =
    "Kendaraan ini akan diaktifkan kembali dengan stok awal 1. Apakah Anda yakin ingin mempublikasikannya ulang ke katalog?";

  confirmAction.value = async () => {
    try {
      const formData = new FormData();
      formData.append("is_active", true);
      formData.append("stock", 1);

      await api.put(`/inventory/${id}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      statusFilter.value = "active";
      fetchMotorcycles();
      closeConfirmModal();
    } catch (err) {
      alert("Gagal mem-publish ulang kendaraan.");
    }
  };

  isConfirmModalOpen.value = true;
};

const availableModels = computed(() => {
  const selectedBrand = masterBrands.value.find(
    (b) => b.id === form.value.brand_id,
  );
  return selectedBrand ? selectedBrand.models : [];
});

watch(
  () => form.value.brand_id,
  () => {
    // Reset otomatis jika merek berubah
  },
);
</script>
