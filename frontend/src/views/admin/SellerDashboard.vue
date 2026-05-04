<template>
  <div>
    <div
      class="flex flex-col items-start justify-between gap-4 mb-6 sm:flex-row sm:items-center"
    >
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Dasbor Titip Jual</h1>
        <p class="mt-1 text-sm text-gray-500">
          Pantau status pengajuan kendaraan Anda di Abu Motor.
        </p>
      </div>

      <button
        @click="openModal"
        class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-lg text-sm font-bold flex items-center gap-2 shadow-sm transition-colors"
      >
        <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
          <path
            fill-rule="evenodd"
            d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
            clip-rule="evenodd"
          />
        </svg>
        Ajukan Titip Jual
      </button>
    </div>

    <!-- TABEL LIST KENDARAAN SELLER -->
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
                Unit Kendaraan
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Tgl Pengajuan
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Harga Dasar (Permintaan)
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-xs font-semibold tracking-wider text-left text-gray-500 uppercase"
              >
                Status Validasi
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
              <td colspan="5" class="px-6 py-8 text-sm text-gray-500">
                Memuat data...
              </td>
            </tr>
            <tr v-else-if="motors.length === 0" class="text-center">
              <td colspan="5" class="px-6 py-12">
                <p class="text-sm font-medium text-gray-500">
                  Anda belum pernah mengajukan titip jual kendaraan.
                </p>
              </td>
            </tr>
            <tr
              v-else
              v-for="motor in motors"
              :key="motor.id"
              class="hover:bg-gray-50"
            >
              <td class="flex items-center gap-4 px-6 py-4 whitespace-nowrap">
                <div
                  class="flex items-center justify-center w-12 h-12 overflow-hidden border border-gray-200 rounded-md bg-gray-50 shrink-0"
                >
                  <img
                    v-if="motor.image_url"
                    :src="getImageUrl(motor.image_url)"
                    class="object-cover w-full h-full"
                  />
                  <span v-else class="text-xs text-gray-400">No Pic</span>
                </div>
                <div>
                  <div class="text-sm font-bold text-gray-900">
                    {{ motor.brand }} {{ motor.model_name }}
                  </div>
                  <div class="flex items-center gap-1 mt-1">
                    <span
                      :class="
                        motor.vehicle_type === 'Mobil'
                          ? 'bg-indigo-100 text-indigo-800'
                          : 'bg-blue-100 text-blue-800'
                      "
                      class="px-2 py-0.5 text-[10px] font-bold uppercase rounded"
                      >{{ motor.vehicle_type }}</span
                    >
                    <span
                      class="px-2 py-0.5 text-[10px] font-bold text-gray-600 bg-gray-100 uppercase rounded"
                      >{{ motor.condition }}</span
                    >
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500 whitespace-nowrap">
                {{ motor.created_at }}
              </td>
              <td
                class="px-6 py-4 text-sm font-bold text-gray-900 whitespace-nowrap"
              >
                {{ formatCurrency(motor.base_price) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  v-if="motor.approval_status === 'pending'"
                  class="px-3 py-1 text-xs font-bold text-yellow-800 bg-yellow-100 border border-yellow-200 rounded-full"
                  >⏳ Sedang Direview</span
                >
                <span
                  v-else-if="motor.approval_status === 'approved'"
                  class="px-3 py-1 text-xs font-bold text-green-800 bg-green-100 border border-green-200 rounded-full"
                >
                  Disetujui (Tayang)</span
                >
                <div v-else class="flex flex-col items-start gap-1.5">
                  <span
                    class="px-3 py-1 text-xs font-bold text-red-800 bg-red-100 border border-red-200 rounded-full"
                  >
                    Ditolak</span
                  >
                  <button
                    @click="openReasonModal(motor)"
                    class="flex items-center gap-1 ml-1 text-[11px] font-bold text-red-600 transition-colors hover:text-red-800 group"
                  >
                    <svg
                      class="w-3.5 h-3.5"
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
                    <span class="underline group-hover:no-underline"
                      >Lihat Alasan</span
                    >
                  </button>
                </div>
              </td>
              <td
                class="px-6 py-4 text-sm font-medium text-right whitespace-nowrap"
              >
                <button
                  v-if="motor.approval_status !== 'approved'"
                  @click="handleDelete(motor.id)"
                  class="flex items-center justify-end gap-1 ml-auto font-bold text-red-600 transition-colors hover:text-red-900"
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
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    ></path>
                  </svg>
                  Batal
                </button>
                <span
                  v-else
                  class="text-xs italic text-gray-400"
                  title="Hubungi admin untuk menarik kendaraan dari katalog"
                  >Terkunci</span
                >
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL PENGAJUAN (UPDATE DENGAN MASTER DATA & MULTI FOTO) -->
    <div v-if="isModalOpen" class="fixed inset-0 z-40 overflow-y-auto">
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
              class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4 max-h-[80vh] overflow-y-auto"
            >
              <h3 class="pb-3 mb-6 text-xl font-bold text-gray-900 border-b">
                Form Pengajuan Titip Jual Kendaraan
              </h3>

              <div
                v-if="isFetchingMaster"
                class="py-10 text-center text-gray-500 animate-pulse"
              >
                Menyiapkan Form...
              </div>

              <div v-else class="space-y-6">
                <!-- 1. Tipe & Kondisi -->
                <div
                  class="grid grid-cols-1 gap-4 md:grid-cols-2 p-4 bg-blue-50 border border-blue-100 rounded-lg"
                >
                  <div>
                    <label class="block text-sm font-bold text-blue-900"
                      >Tipe Kendaraan</label
                    >
                    <select
                      v-model="form.vehicle_type"
                      @change="resetCategory"
                      class="block w-full px-3 py-2 mt-1 font-bold text-blue-700 bg-white border border-blue-300 rounded-md sm:text-sm"
                    >
                      <option value="Motor">Sepeda Motor</option>
                      <option value="Mobil">Mobil</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-bold text-blue-900"
                      >Kondisi</label
                    >
                    <select
                      v-model="form.condition"
                      class="block w-full px-3 py-2 mt-1 bg-white border border-blue-300 rounded-md sm:text-sm"
                    >
                      <option value="Baru">Baru</option>
                      <option value="Bekas">Bekas</option>
                    </select>
                  </div>
                </div>

                <!-- 2. Master Data (Merek, Model, Kategori) -->
                <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
                  <!-- PENCARIAN MEREK -->
                  <div class="relative">
                    <label class="block text-sm font-medium text-gray-700"
                      >Merek Kendaraan</label
                    >
                    <div class="relative mt-1">
                      <input
                        type="text"
                        v-model="brandSearchTerm"
                        @focus="showBrandDropdown = true"
                        @blur="hideBrandDropdown"
                        placeholder="Ketik merek (cth: Honda)..."
                        class="block w-full px-3 py-2 bg-white border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        :class="{
                          'border-green-500 bg-green-50': form.brand_id,
                        }"
                      />
                      <!-- Indikator terpilih -->
                      <div
                        v-if="form.brand_id"
                        class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none"
                      >
                        <svg
                          class="w-4 h-4 text-green-500"
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

                    <!-- Dropdown Merek -->
                    <ul
                      v-if="showBrandDropdown && filteredBrands.length > 0"
                      class="absolute z-10 w-full py-1 mt-1 overflow-auto bg-white border border-gray-200 rounded-md shadow-lg max-h-48"
                    >
                      <li
                        v-for="b in filteredBrands"
                        :key="b.id"
                        @mousedown.prevent="selectBrand(b)"
                        class="px-3 py-2 text-sm cursor-pointer hover:bg-blue-50 hover:text-blue-700 font-medium"
                      >
                        {{ b.name }}
                      </li>
                    </ul>
                    <div
                      v-if="showBrandDropdown && filteredBrands.length === 0"
                      class="absolute z-10 w-full px-3 py-2 mt-1 text-sm text-gray-500 bg-white border border-gray-200 rounded-md shadow-lg"
                    >
                      Merek tidak ditemukan.
                    </div>
                  </div>

                  <!-- PENCARIAN MODEL -->
                  <div class="relative">
                    <label class="block text-sm font-medium text-gray-700"
                      >Nama Model</label
                    >
                    <div class="relative mt-1">
                      <input
                        type="text"
                        v-model="modelSearchTerm"
                        @focus="showModelDropdown = true"
                        @blur="hideModelDropdown"
                        placeholder="Ketik model..."
                        class="block w-full px-3 py-2 bg-white border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        :class="{
                          'border-green-500 bg-green-50': form.model_name,
                        }"
                        :disabled="!form.brand_id"
                      />
                      <div
                        v-if="form.model_name"
                        class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none"
                      >
                        <svg
                          class="w-4 h-4 text-green-500"
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

                    <!-- Dropdown Model -->
                    <ul
                      v-if="showModelDropdown && filteredModels.length > 0"
                      class="absolute z-10 w-full py-1 mt-1 overflow-auto bg-white border border-gray-200 rounded-md shadow-lg max-h-48"
                    >
                      <li
                        v-for="m in filteredModels"
                        :key="m.id"
                        @mousedown.prevent="selectModel(m)"
                        class="px-3 py-2 text-sm cursor-pointer hover:bg-blue-50 hover:text-blue-700 font-medium"
                      >
                        {{ m.name }}
                      </li>
                    </ul>
                    <div
                      v-if="
                        showModelDropdown &&
                        filteredModels.length === 0 &&
                        form.brand_id
                      "
                      class="absolute z-10 w-full px-3 py-2 mt-1 text-sm text-gray-500 bg-white border border-gray-200 rounded-md shadow-lg"
                    >
                      Model tidak ditemukan.
                    </div>
                  </div>

                  <!-- KATEGORI -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700"
                      >Kategori</label
                    >
                    <select
                      v-model="form.category_id"
                      required
                      class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md sm:text-sm bg-white"
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

                <!-- 3. Spesifikasi Teknis -->
                <div class="grid grid-cols-1 gap-4 md:grid-cols-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700"
                      >Warna Dominan</label
                    >
                    <input
                      v-model="form.color"
                      type="text"
                      class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md sm:text-sm"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700"
                      >Tahun</label
                    >
                    <input
                      v-model="form.year"
                      type="number"
                      min="1990"
                      required
                      class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md sm:text-sm"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700"
                      >Jarak Tempuh</label
                    >
                    <input
                      v-model="form.mileage"
                      type="text"
                      required
                      placeholder="Cth: 15.000 km"
                      class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md sm:text-sm"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700"
                      >Kapasitas (CC)</label
                    >
                    <input
                      v-model="form.engine_capacity"
                      type="text"
                      placeholder="Cth: 155 cc"
                      class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md sm:text-sm"
                    />
                  </div>
                </div>

                <!-- 4. Kelengkapan -->
                <div class="p-4 border border-gray-200 rounded-lg bg-gray-50">
                  <label class="block mb-3 text-sm font-bold text-gray-900"
                    >Kelengkapan Dokumen (Centang yang ada)</label
                  >
                  <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <label class="flex items-center space-x-3"
                      ><input
                        type="checkbox"
                        v-model="form.documents"
                        value="BPKB"
                        class="w-5 h-5 text-blue-600 rounded"
                      /><span class="text-sm font-medium">BPKB</span></label
                    >
                    <label class="flex items-center space-x-3"
                      ><input
                        type="checkbox"
                        v-model="form.documents"
                        value="STNK"
                        class="w-5 h-5 text-blue-600 rounded"
                      /><span class="text-sm font-medium">STNK</span></label
                    >
                    <label class="flex items-center space-x-3"
                      ><input
                        type="checkbox"
                        v-model="form.documents"
                        value="Faktur"
                        class="w-5 h-5 text-blue-600 rounded"
                      /><span class="text-sm font-medium">Faktur</span></label
                    >
                    <!-- <label class="flex items-center space-x-3"
                      ><input
                        type="checkbox"
                        v-model="form.documents"
                        value="Buku Garansi"
                        class="w-5 h-5 text-blue-600 rounded"
                      /><span class="text-sm font-medium">Garansi</span></label
                    > -->
                  </div>
                </div>

                <!-- 5. Harga & Multi Upload (Stacking UI) -->
                <div
                  class="grid grid-cols-1 gap-6 p-4 border border-green-200 rounded-lg md:grid-cols-2 bg-green-50"
                >
                  <div class="md:col-span-2">
                    <label class="block mb-1 text-sm font-bold text-green-900"
                      >Harga Dasar (Permintaan Anda)</label
                    >
                    <input
                      v-model="form.base_price"
                      type="number"
                      min="0"
                      required
                      class="block w-full border-2 border-green-300 rounded-md py-2.5 px-3 font-bold text-gray-900 text-lg focus:border-green-500 focus:ring-green-500"
                    />
                    <p class="mt-1 text-xs text-green-700">
                      Uang yang akan Anda terima jika kendaraan terjual. Harga
                      Jual ke konsumen akan disesuaikan oleh Dealer.
                    </p>
                  </div>

                  <!-- FOTO UTAMA (STACK MAKS 1) -->
                  <div>
                    <label class="block mb-2 text-sm font-bold text-green-900">
                      Foto Utama <span class="text-red-500">*</span>
                      <span class="font-normal text-green-700"
                        >(Maks 1 Gambar)</span
                      >
                    </label>
                    <div class="flex flex-wrap items-start gap-4">
                      <!-- Preview -->
                      <div
                        v-if="mainPhotoPreview"
                        class="relative group w-28 h-28"
                      >
                        <img
                          :src="mainPhotoPreview"
                          class="object-cover w-full h-full border-2 border-green-400 shadow-md rounded-xl"
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
                        class="flex flex-col items-center justify-center border-2 border-green-400 border-dashed cursor-pointer w-28 h-28 rounded-xl hover:bg-green-100 transition-colors bg-white"
                        :class="{
                          'opacity-50 cursor-not-allowed': mainPhotoPreview,
                        }"
                      >
                        <svg
                          class="w-8 h-8 mb-2"
                          :class="
                            mainPhotoPreview
                              ? 'text-gray-400'
                              : 'text-green-500'
                          "
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
                              : 'text-green-700'
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
                          :required="!mainPhotoPreview"
                        />
                      </label>
                    </div>
                  </div>

                  <!-- FOTO GALERI (STACK MAKS 9) -->
                  <div>
                    <label class="block mb-2 text-sm font-bold text-green-900">
                      Foto Detail Tambahan
                      <span class="font-normal text-green-700"
                        >(Maks 9 Gambar)</span
                      >
                    </label>
                    <div class="flex flex-wrap items-start gap-3">
                      <!-- Box Previews -->
                      <div
                        v-for="(item, index) in galleryPhotosPreview"
                        :key="index"
                        class="relative group w-20 h-20"
                      >
                        <img
                          :src="item.url"
                          class="object-cover w-full h-full border border-green-300 shadow-sm rounded-lg"
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
                      </div>

                      <!-- Box Tambah Galeri -->
                      <label
                        @click="checkGalleryLimit"
                        class="flex flex-col items-center justify-center border-2 border-green-300 border-dashed cursor-pointer w-20 h-20 rounded-lg hover:bg-green-100 transition-colors bg-white"
                        :class="{
                          'opacity-50 cursor-not-allowed':
                            galleryPhotosPreview.length >= 9,
                        }"
                      >
                        <svg
                          class="w-6 h-6 mb-1 text-green-400"
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
                        <span class="text-[10px] font-bold text-green-700"
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

                <div>
                  <label class="block text-sm font-medium text-gray-700"
                    >Deskripsi Tambahan</label
                  >
                  <textarea
                    v-model="form.description"
                    rows="3"
                    placeholder="Ceritakan lecet pemakaian, part modifikasi, dll..."
                    class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md sm:text-sm"
                  ></textarea>
                </div>
              </div>
            </div>

            <div
              class="px-4 py-3 border-t border-gray-200 bg-gray-50 sm:px-6 sm:flex sm:flex-row-reverse"
            >
              <button
                type="submit"
                :disabled="isSaving || isFetchingMaster"
                class="inline-flex justify-center w-full px-6 py-2 text-base font-bold text-white bg-blue-600 rounded-md shadow-sm hover:bg-blue-700 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-70"
              >
                {{ isSaving ? "Mengirim..." : "Kirim Pengajuan" }}
              </button>
              <button
                type="button"
                @click="closeModal"
                class="inline-flex justify-center w-full px-6 py-2 mt-3 text-base font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 sm:mt-0 sm:w-auto sm:text-sm"
              >
                Batal
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- MODAL PENOLAKAN TETAP SAMA -->
    <div v-if="isReasonModalOpen" class="fixed inset-0 z-[60] overflow-y-auto">
      <div
        class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:p-0"
      >
        <div
          class="fixed inset-0 transition-opacity bg-gray-800 bg-opacity-75 backdrop-blur-sm"
          @click="closeReasonModal"
        ></div>
        <div
          class="inline-block w-full max-w-md p-6 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
        >
          <div class="flex items-center gap-4 mb-5">
            <div
              class="flex items-center justify-center w-12 h-12 bg-red-100 rounded-full shrink-0"
            >
              <svg
                class="w-6 h-6 text-red-600"
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
              <h3 class="text-lg font-bold text-gray-900">Alasan Penolakan</h3>
              <p class="text-sm text-gray-500">Pesan dari Admin Abu Motor</p>
            </div>
          </div>
          <div
            class="p-4 mb-6 text-sm leading-relaxed text-red-800 whitespace-pre-line border rounded-lg bg-red-50 border-red-100"
          >
            {{ currentRejectionReason }}
          </div>
          <div class="flex justify-end gap-3">
            <button
              @click="closeReasonModal"
              class="w-full px-5 py-2.5 text-sm font-bold text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Tutup Pesan
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import api from "../../services/api";

const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5001";
const motors = ref([]);
const isLoading = ref(true);

const isModalOpen = ref(false);
const isSaving = ref(false);
const isFetchingMaster = ref(false);

const isReasonModalOpen = ref(false);
const currentRejectionReason = ref("");

// STATE UNTUK UPLOAD FOTO
const selectedMainPhoto = ref(null);
const mainPhotoInput = ref(null);
const mainPhotoPreview = ref(null);

const galleryInput = ref(null);
// Di Dashboard Seller (Create Only), kita tidak butuh pengecekan isExisting
// Cukup simpan object { url: string, file: File }
const galleryPhotosPreview = ref([]);

// MASTER DATA (Diambil dari Backend)
const masterBrands = ref([]);
const masterCategories = ref([]);

const brandSearchTerm = ref("");
const showBrandDropdown = ref(false);

const modelSearchTerm = ref("");
const showModelDropdown = ref(false);

const form = ref({
  vehicle_type: "Motor",
  condition: "Bekas",
  brand_id: "",
  model_name: "",
  category_id: "",
  color: "",
  year: new Date().getFullYear(),
  transmission: "Otomatis",
  mileage: "",
  engine_capacity: "",
  documents: [],
  base_price: 0,
  description: "",
});

const filteredBrands = computed(() => {
  if (!brandSearchTerm.value) return masterBrands.value;
  const q = brandSearchTerm.value.toLowerCase();
  return masterBrands.value.filter((b) => b.name.toLowerCase().includes(q));
});

// Computed Merek -> Model (Reaktif)
const availableModels = computed(() => {
  const selectedBrand = masterBrands.value.find(
    (b) => b.id === form.value.brand_id,
  );
  return selectedBrand ? selectedBrand.models : [];
});

const filteredModels = computed(() => {
  if (!modelSearchTerm.value) return availableModels.value;
  const q = modelSearchTerm.value.toLowerCase();
  return availableModels.value.filter((m) => m.name.toLowerCase().includes(q));
});

// Aksi Saat Diklik
const selectBrand = (brand) => {
  form.value.brand_id = brand.id;
  brandSearchTerm.value = brand.name;
  showBrandDropdown.value = false;

  // Otomatis reset model jika merek diganti
  form.value.model_name = "";
  modelSearchTerm.value = "";
};

const selectModel = (model) => {
  form.value.model_name = model.name;
  modelSearchTerm.value = model.name;
  showModelDropdown.value = false;
};

// Delay untuk menyembunyikan dropdown agar klik terdaftar
const hideBrandDropdown = () =>
  setTimeout(() => (showBrandDropdown.value = false), 150);
const hideModelDropdown = () =>
  setTimeout(() => (showModelDropdown.value = false), 150);

const resetCategory = () => {
  form.value.category_id = "";
};

const formatCurrency = (value) =>
  new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    minimumFractionDigits: 0,
  }).format(value || 0);
const getImageUrl = (url) =>
  url ? `${BASE_URL}${url}?t=${new Date().getTime()}` : null;

const fetchMotors = async () => {
  isLoading.value = true;
  try {
    const response = await api.get("/inventory/seller/motors");
    motors.value = response.data.data;
  } catch (error) {
    console.error("Gagal mengambil data:", error);
  } finally {
    isLoading.value = false;
  }
};

const fetchMasterData = async () => {
  isFetchingMaster.value = true;
  try {
    const [brandRes, catRes] = await Promise.all([
      api.get("/master/brands"),
      api.get("/master/categories"),
    ]);
    masterBrands.value = brandRes.data.data;
    masterCategories.value = catRes.data.data;
  } catch (error) {
    alert("Gagal memuat data master kendaraan");
  } finally {
    isFetchingMaster.value = false;
  }
};

const checkMainPhotoLimit = (e) => {
  if (mainPhotoPreview.value) {
    e.preventDefault();
    alert(
      "Maksimal hanya upload 1 foto utama. Jika ingin mengganti, klik tombol silang (X) pada gambar terlebih dahulu.",
    );
  }
};

const checkGalleryLimit = (e) => {
  if (galleryPhotosPreview.value.length >= 9) {
    e.preventDefault();
    alert(
      "Foto tambahan maksimal 9 lembar. Hapus gambar lama jika ingin menambahkan yang baru.",
    );
  }
};

const handleMainPhoto = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedMainPhoto.value = file;
    mainPhotoPreview.value = URL.createObjectURL(file);
  }
  if (mainPhotoInput.value) mainPhotoInput.value.value = ""; // Reset input
};

const handleGalleryPhotos = (event) => {
  const files = Array.from(event.target.files);
  const availableSlots = 9 - galleryPhotosPreview.value.length;

  if (files.length > availableSlots) {
    alert(
      `Maksimal 9 gambar! Anda hanya bisa memilih ${availableSlots} gambar lagi.`,
    );
  }

  const filesToAdd = files.slice(0, availableSlots);
  filesToAdd.forEach((file) => {
    galleryPhotosPreview.value.push({
      url: URL.createObjectURL(file),
      file: file,
    });
  });

  if (galleryInput.value) galleryInput.value.value = ""; // Reset input
};

const removeMainPhoto = () => {
  selectedMainPhoto.value = null;
  mainPhotoPreview.value = null;
};

const removeGalleryPhoto = (index) => {
  galleryPhotosPreview.value.splice(index, 1);
};

const openModal = () => {
  isModalOpen.value = true;
  form.value = {
    vehicle_type: "Motor",
    condition: "Bekas",
    brand_id: "",
    model_name: "",
    category_id: "",
    color: "",
    year: new Date().getFullYear(),
    transmission: "Otomatis",
    mileage: "",
    engine_capacity: "",
    documents: [],
    base_price: 0,
    description: "",
  };

  // Reset Pencarian Merek & Model
  brandSearchTerm.value = "";
  modelSearchTerm.value = "";
  showBrandDropdown.value = false;
  showModelDropdown.value = false;

  // Bersihkan Tumpukan Foto
  selectedMainPhoto.value = null;
  mainPhotoPreview.value = null;
  galleryPhotosPreview.value = [];

  if (masterBrands.value.length === 0) fetchMasterData();
};

const closeModal = () => {
  isModalOpen.value = false;
  // Bersihkan Preview saat Batal
  selectedMainPhoto.value = null;
  mainPhotoPreview.value = null;
  galleryPhotosPreview.value = [];
};

const handleSubmit = async () => {
  // Cek wajib upload foto utama
  if (!selectedMainPhoto.value) {
    alert("Mohon upload Foto Utama kendaraan Anda terlebih dahulu.");
    return;
  }

  isSaving.value = true;
  try {
    const formData = new FormData();
    Object.keys(form.value).forEach((key) => {
      if (key === "documents") formData.append(key, form.value[key].join(","));
      else formData.append(key, form.value[key]);
    });

    // 1. Kirim Foto Utama
    formData.append("image", selectedMainPhoto.value);

    // 2. Kirim Tumpukan Foto Galeri Baru
    galleryPhotosPreview.value.forEach((item) => {
      formData.append("gallery", item.file);
    });

    await api.post("/inventory/seller/motors", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    closeModal();
    fetchMotors();
    alert("Pengajuan berhasil! Silakan tunggu Admin melakukan validasi.");
  } catch (error) {
    alert(error.response?.data?.message || "Gagal mengirim pengajuan");
  } finally {
    isSaving.value = false;
  }
};

const openReasonModal = (motor) => {
  currentRejectionReason.value =
    motor.rejection_reason ||
    "Tidak ada alasan spesifik yang dicantumkan oleh Admin.";
  isReasonModalOpen.value = true;
};
const closeReasonModal = () => {
  isReasonModalOpen.value = false;
  currentRejectionReason.value = "";
};

const handleDelete = async (id) => {
  if (
    confirm(
      "Apakah Anda yakin ingin membatalkan dan menghapus pengajuan ini secara permanen?",
    )
  ) {
    try {
      await api.delete(`/inventory/seller/motors/${id}`);
      fetchMotors();
    } catch (error) {
      alert(error.response?.data?.message || "Gagal membatalkan pengajuan");
    }
  }
};

onMounted(() => fetchMotors());
</script>
