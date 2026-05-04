<template>
  <div class="min-h-screen bg-gray-50 font-sans flex flex-col">
    <PublicNavbar />

    <div v-if="isLoading" class="flex-1 flex justify-center items-center py-20">
      <div class="animate-pulse flex flex-col items-center">
        <div class="h-12 w-12 bg-blue-200 rounded-full mb-4"></div>
        <p class="text-gray-500 font-medium">Memuat detail motor...</p>
      </div>
    </div>

    <main
      v-else-if="motor"
      class="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full"
    >
      <nav class="flex text-sm text-gray-500 mb-6" aria-label="Breadcrumb">
        <ol class="inline-flex items-center space-x-1 md:space-x-3">
          <li class="inline-flex items-center">
            <router-link to="/" class="hover:text-blue-600 transition-colors"
              >Home</router-link
            >
          </li>
          <li>
            <div class="flex items-center">
              <svg
                class="w-4 h-4 text-gray-400 mx-1"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                  clip-rule="evenodd"
                ></path>
              </svg>
              <router-link
                to="/katalog"
                class="hover:text-blue-600 transition-colors"
                >Katalog</router-link
              >
            </div>
          </li>
          <li aria-current="page">
            <div class="flex items-center">
              <svg
                class="w-4 h-4 text-gray-400 mx-1"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                  clip-rule="evenodd"
                ></path>
              </svg>
              <span class="text-gray-800 font-medium">{{
                motor.model_name
              }}</span>
            </div>
          </li>
        </ol>
      </nav>

      <div
        class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden"
      >
        <div class="grid grid-cols-1 md:grid-cols-2 gap-0 md:gap-8">
          <!-- BAGIAN KIRI: GALERI FOTO -->
          <div
            class="bg-gray-50 p-6 md:p-8 border-b md:border-b-0 md:border-r border-gray-100 relative flex flex-col"
          >
            <!-- Badges -->
            <div class="absolute top-4 left-4 flex gap-2 z-10">
              <span
                class="bg-blue-600 text-white px-3 py-1 rounded-md text-xs font-bold uppercase tracking-wide shadow-sm"
                >{{ motor.category || "Motor" }}</span
              >
              <span
                v-if="motor.stock > 0"
                class="bg-green-500 text-white px-3 py-1 rounded-md text-xs font-bold uppercase tracking-wide shadow-sm"
                >Stok Tersedia</span
              >
              <span
                v-else
                class="bg-red-500 text-white px-3 py-1 rounded-md text-xs font-bold uppercase tracking-wide shadow-sm"
                >Stok Habis</span
              >
            </div>

            <!-- Foto Utama Besar -->
            <div
              class="flex-1 flex items-center justify-center min-h-[300px] mb-6 bg-white rounded-2xl border border-gray-100 p-4 shadow-sm"
            >
              <img
                v-if="activeImage"
                :src="getImageUrl(activeImage)"
                :alt="motor.model_name"
                class="w-full h-auto object-contain max-h-[400px] drop-shadow-xl transition-opacity duration-300"
              />
              <svg
                v-else
                class="w-32 h-32 text-gray-300"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                ></path>
              </svg>
            </div>

            <!-- Thumbnails List (Bisa di-scroll menyamping) -->
            <div
              v-if="allPhotos.length > 1"
              class="flex gap-3 overflow-x-auto pb-2 hide-scrollbar"
            >
              <button
                v-for="(photo, index) in allPhotos"
                :key="index"
                @click="activeImage = photo"
                class="shrink-0 w-20 h-20 rounded-xl border-2 overflow-hidden transition-all duration-200 focus:outline-none"
                :class="
                  activeImage === photo
                    ? 'border-blue-600 shadow-md ring-2 ring-blue-600/20'
                    : 'border-transparent hover:border-blue-300 opacity-60 hover:opacity-100'
                "
              >
                <img
                  :src="getImageUrl(photo)"
                  class="w-full h-full object-cover"
                />
              </button>
            </div>
          </div>

          <div class="p-6 md:p-10 flex flex-col justify-center">
            <div class="flex items-center gap-2 mb-2">
              <p
                class="text-sm font-bold text-gray-500 uppercase tracking-widest"
              >
                {{ motor.brand }}
              </p>
              <span
                v-if="motor.branch_name"
                class="px-2 py-0.5 text-[10px] font-bold text-blue-700 bg-blue-100 rounded-full uppercase tracking-wider"
                >{{ motor.branch_name }}</span
              >
              <span
                class="px-2 py-0.5 text-[10px] font-bold text-gray-600 bg-gray-100 rounded-full uppercase tracking-wider"
                >{{ motor.condition || "Bekas" }}</span
              >
            </div>

            <h1
              class="text-3xl md:text-4xl font-extrabold text-gray-900 mb-4 leading-tight"
            >
              {{ motor.model_name }}
            </h1>

            <div class="mb-6">
              <p class="text-sm text-gray-500 mb-1">Harga OTR</p>
              <p class="text-4xl font-black text-blue-600">
                {{ formatCurrency(motor.price) }}
              </p>
            </div>

            <div class="flex flex-wrap items-center gap-4 mb-8">
              <div
                class="flex items-center gap-2 bg-gray-50 px-4 py-2 rounded-lg border border-gray-200"
              >
                <span
                  class="w-4 h-4 rounded-full border border-gray-300 shadow-inner"
                  :style="{ backgroundColor: getBasicColor(motor.color) }"
                ></span>
                <span class="text-sm font-medium text-gray-700">{{
                  motor.color || "-"
                }}</span>
              </div>
              <div
                class="text-sm text-gray-600 bg-gray-50 px-4 py-2 rounded-lg border border-gray-200"
              >
                <span class="font-medium">SKU:</span> {{ motor.sku_code }}
              </div>
            </div>

            <!-- ACTION BUTTONS -->
            <div class="flex flex-col gap-3">
              <a
                :href="waLink"
                target="_blank"
                class="w-full flex items-center justify-center gap-3 bg-green-500 hover:bg-green-600 text-white px-8 py-4 rounded-xl font-bold transition-colors shadow-lg shadow-green-200 text-lg"
              >
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path
                    d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 00-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .1 5.392.1 11.947c0 2.096.546 4.142 1.584 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.945-5.393 11.945-11.95a11.813 11.813 0 00-3.53-8.406z"
                  />
                </svg>
                Tanya ke CS Sekarang
              </a>

              <div class="flex gap-3">
                <button
                  @click="toggleWishlist"
                  :class="
                    isWishlisted
                      ? 'bg-red-50 border-red-200 text-red-500'
                      : 'border-gray-200 hover:bg-gray-50 text-gray-600'
                  "
                  class="flex-1 flex items-center justify-center gap-2 border-2 px-4 py-3 rounded-xl font-bold transition-colors"
                >
                  <svg
                    :class="isWishlisted ? 'fill-current' : 'fill-none'"
                    class="w-5 h-5"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                    ></path>
                  </svg>
                  {{ isWishlisted ? "Tersimpan" : "Simpan" }}
                </button>
                <button
                  @click="shareVehicle"
                  class="flex-1 flex items-center justify-center gap-2 border-2 border-gray-200 hover:bg-blue-50 hover:border-blue-200 hover:text-blue-600 text-gray-600 px-4 py-3 rounded-xl font-bold transition-colors"
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
                      d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"
                    ></path>
                  </svg>
                  Bagikan
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 space-y-8">
          <div
            class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8"
          >
            <h2 class="text-xl font-bold text-gray-900 mb-6 border-b pb-4">
              Detail Spesifikasi
            </h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-4">
              <div class="flex justify-between py-2 border-b border-gray-50">
                <span class="text-gray-500">Merek</span
                ><span class="font-medium text-gray-900">{{
                  motor.brand || "-"
                }}</span>
              </div>
              <div class="flex justify-between py-2 border-b border-gray-50">
                <span class="text-gray-500">Model</span
                ><span class="font-medium text-gray-900">{{
                  motor.model_name || "-"
                }}</span>
              </div>
              <div class="flex justify-between py-2 border-b border-gray-50">
                <span class="text-gray-500">Warna</span
                ><span class="font-medium text-gray-900">{{
                  motor.color || "-"
                }}</span>
              </div>
              <div class="flex justify-between py-2 border-b border-gray-50">
                <span class="text-gray-500">Transmisi</span
                ><span class="font-medium text-gray-900">{{
                  motor.transmission || "-"
                }}</span>
              </div>
              <div class="flex justify-between py-2 border-b border-gray-50">
                <span class="text-gray-500">Tahun Produksi</span
                ><span class="font-medium text-gray-900">{{
                  motor.year || "-"
                }}</span>
              </div>
              <div class="flex justify-between py-2 border-b border-gray-50">
                <span class="text-gray-500">Jarak Tempuh</span
                ><span class="font-medium text-gray-900"
                  >{{ motor.mileage || "-" }} km</span
                >
              </div>
              <div class="flex justify-between py-2 border-b border-gray-50">
                <span class="text-gray-500">Tipe Bodi</span
                ><span class="font-medium text-gray-900">{{
                  motor.body_type || motor.category || "-"
                }}</span>
              </div>
              <div class="flex justify-between py-2 border-b border-gray-50">
                <span class="text-gray-500">Kapasitas Mesin</span
                ><span class="font-medium text-gray-900"
                  >{{ motor.engine_capacity || "-" }} cc</span
                >
              </div>
            </div>
            <div
              v-if="motor.features"
              class="mt-6 pt-4 border-t border-gray-100"
            >
              <span class="text-gray-500 block mb-2">Fitur Unggulan</span>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="(feature, index) in motor.features.split(',')"
                  :key="index"
                  class="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-sm font-medium border border-blue-100"
                  >{{ feature.trim() }}</span
                >
              </div>
            </div>
          </div>

          <div
            class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8"
          >
            <h2 class="text-xl font-bold text-gray-900 mb-4">
              Deskripsi Kendaraan
            </h2>
            <div
              class="prose max-w-none text-gray-600 leading-relaxed whitespace-pre-line"
            >
              {{
                motor.description ||
                "Tidak ada deskripsi tambahan untuk kendaraan ini."
              }}
            </div>
          </div>
        </div>

        <div class="space-y-6">
          <div class="bg-gray-900 text-white rounded-2xl shadow-sm p-6 md:p-8">
            <h2 class="text-lg font-bold mb-6 flex items-center gap-2">
              <svg
                class="w-5 h-5 text-blue-400"
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
              Kelengkapan Dokumen
            </h2>
            <ul v-if="motor.documents" class="space-y-4">
              <li
                v-for="(doc, index) in motor.documents.split(',')"
                :key="index"
                class="flex items-start gap-3"
              >
                <svg
                  class="w-5 h-5 text-green-400 shrink-0 mt-0.5"
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
                <span class="text-gray-300 text-sm leading-snug">
                  {{
                    doc.trim() === "BPKB"
                      ? "BPKB (Buku Pemilik Kendaraan Bermotor)"
                      : doc.trim() === "STNK"
                        ? "STNK (Surat Tanda Nomor Kendaraan)"
                        : doc.trim() === "Faktur"
                          ? "Faktur Pembelian Resmi"
                          : doc.trim() === "Buku Garansi"
                            ? "Buku Garansi & Servis"
                            : doc.trim()
                  }}
                </span>
              </li>
            </ul>
            <div
              v-else
              class="text-gray-400 text-sm italic bg-gray-800 p-4 rounded-lg border border-gray-700"
            >
              Informasi kelengkapan dokumen belum diunggah. Silakan tanyakan
              langsung ke CS kami.
            </div>
          </div>

          <div
            class="bg-blue-100 rounded-2xl shadow-sm border border-blue-100 p-6 md:p-8 relative overflow-hidden"
          >
            <div
              class="absolute top-0 right-0 w-32 h-32 bg-blue-50 rounded-bl-full -z-10"
            ></div>

            <h2
              class="text-xl font-bold text-gray-900 mb-1 flex items-center gap-2"
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
                  d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                ></path>
              </svg>
              Simulasi Kredit
            </h2>
            <p class="text-sm text-gray-500 mb-6">
              Hitung perkiraan cicilan bulanan Anda.
            </p>

            <div class="space-y-5">
              <div>
                <div class="flex justify-between items-end mb-2">
                  <label class="block text-sm font-medium text-gray-700"
                    >Uang Muka (DP)</label
                  >
                  <span class="text-blue-600 font-bold"
                    >{{ dpPercentage }}%</span
                  >
                </div>
                <input
                  v-model="dpPercentage"
                  type="range"
                  min="15"
                  max="50"
                  step="5"
                  class="w-full h-2 bg-blue-300 rounded-lg appearance-none cursor-pointer accent-blue-600"
                />
                <p class="text-right text-xs text-gray-500 mt-1">
                  {{ formatCurrency(dpAmount) }}
                </p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2"
                  >Tenor (Bulan)</label
                >
                <div class="grid grid-cols-3 gap-2">
                  <button
                    v-for="t in [11, 23, 35]"
                    :key="t"
                    @click="selectedTenor = t"
                    type="button"
                    :class="
                      selectedTenor === t
                        ? 'bg-blue-600 text-white border-blue-600'
                        : 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50'
                    "
                    class="border py-2 rounded-lg text-sm font-semibold transition-colors focus:outline-none"
                  >
                    {{ t }} bln
                  </button>
                </div>
              </div>

              <div
                class="bg-blue-50 p-4 rounded-xl border border-blue-100 mt-4"
              >
                <p
                  class="text-xs text-blue-800 font-medium uppercase tracking-wider mb-1"
                >
                  Estimasi Cicilan
                </p>
                <p class="text-2xl font-black text-blue-700">
                  {{ formatCurrency(monthlyInstallment)
                  }}<span class="text-sm font-medium text-blue-600"> /bln</span>
                </p>
                <p class="text-[10px] text-gray-500 mt-2 leading-tight">
                  *Estimasi menggunakan suku bunga 1.5% per bulan. Angka aktual
                  dapat berubah sesuai ketentuan leasing.
                </p>
              </div>

              <a
                :href="waLinkWithSimulation"
                target="_blank"
                class="w-full flex justify-center items-center gap-2 bg-gray-900 hover:bg-gray-800 text-white py-3 rounded-xl text-sm font-semibold transition-colors shadow-md mt-2"
              >
                Ajukan Kredit Sekarang
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
                    d="M14 5l7 7m0 0l-7 7m7-7H3"
                  ></path>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
      <!-- MODAL PERINGATAN LOGIN WISHLIST -->
      <div
        v-if="showAuthModal"
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/60 backdrop-blur-sm"
      >
        <div
          class="w-full max-w-sm p-6 bg-white shadow-2xl rounded-2xl text-center"
        >
          <div
            class="flex items-center justify-center w-16 h-16 mx-auto mb-4 bg-blue-100 rounded-full"
          >
            <svg
              class="w-8 h-8 text-blue-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
              ></path>
            </svg>
          </div>
          <h3 class="mb-2 text-xl font-bold text-gray-900">Login Diperlukan</h3>
          <p class="mb-6 text-sm text-gray-500">
            Anda harus masuk atau mendaftar terlebih dahulu untuk menyimpan
            kendaraan ini ke Wishlist Anda.
          </p>
          <div class="flex gap-3">
            <button
              @click="showAuthModal = false"
              class="flex-1 px-4 py-2 text-sm font-semibold text-gray-700 transition-colors bg-gray-100 rounded-xl hover:bg-gray-200"
            >
              Batal
            </button>
            <router-link
              to="/login"
              class="flex-1 px-4 py-2 text-sm font-semibold text-white transition-colors bg-blue-600 rounded-xl hover:bg-blue-700"
            >
              Pergi ke Login
            </router-link>
          </div>
        </div>
      </div>
    </main>

    <div
      v-else
      class="flex-1 flex flex-col justify-center items-center py-20 text-center px-4"
    >
      <svg
        class="w-16 h-16 text-red-400 mb-4"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
        ></path>
      </svg>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">
        Motor Tidak Ditemukan
      </h2>
      <p class="text-gray-500 mb-6">
        Maaf, data motor yang Anda cari tidak ada atau telah dihapus.
      </p>
      <router-link
        to="/katalog"
        class="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition"
        >Kembali ke Katalog</router-link
      >
    </div>

    <PublicFooter />
  </div>
</template>

<script setup>
import api, { BASE_URL } from "../../services/api";
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import PublicNavbar from "../../components/PublicNavbar.vue";
import PublicFooter from "../../components/PublicFooter.vue";

const route = useRoute();
const motor = ref(null);
// State untuk Galeri Foto
const activeImage = ref(null);

// Menggabungkan foto utama dan foto galeri menjadi satu array
const allPhotos = computed(() => {
  if (!motor.value) return [];
  const photos = [];

  if (motor.value.image_url) {
    photos.push(motor.value.image_url);
  }
  if (motor.value.gallery && motor.value.gallery.length > 0) {
    photos.push(...motor.value.gallery);
  }

  return photos;
});

const isLoading = ref(true);
const DEALER_WA_NUMBER = "6281222444951"; // Ganti dengan nomor WhatsApp aslimu

// --- State Kalkulator Simulasi ---
const dpPercentage = ref(20); // Default DP 20%
const selectedTenor = ref(35); // Default Tenor 35 Bulan
const flatInterestRatePerMonth = 1.5; // Bunga flat 1.5% per bulan

// --- Fungsi Format ---
const formatCurrency = (value) => {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    minimumFractionDigits: 0,
  }).format(value || 0);
};

const getImageUrl = (url) => {
  if (!url) return null;
  return `${BASE_URL}${url}?t=${new Date().getTime()}`;
};

const getBasicColor = (colorName) => {
  if (!colorName) return "transparent";
  const name = colorName.toLowerCase();
  if (name.includes("hitam") || name.includes("black")) return "#1a1a1a";
  if (name.includes("putih") || name.includes("white")) return "#f9fafb";
  if (name.includes("merah") || name.includes("red")) return "#dc2626";
  if (name.includes("biru") || name.includes("blue")) return "#2563eb";
  if (name.includes("abu") || name.includes("silver")) return "#9ca3af";
  if (name.includes("kuning") || name.includes("yellow")) return "#facc15";
  return "#e5e7eb";
};

// --- Logika Kalkulator ---
const dpAmount = computed(() => {
  if (!motor.value) return 0;
  return (motor.value.price * dpPercentage.value) / 100;
});

const monthlyInstallment = computed(() => {
  if (!motor.value) return 0;
  const principal = motor.value.price - dpAmount.value; // Pokok hutang
  const totalInterestPercent = flatInterestRatePerMonth * selectedTenor.value; // Total bunga (%)
  const totalInterestAmount = principal * (totalInterestPercent / 100); // Total nominal bunga
  const totalDebt = principal + totalInterestAmount; // Total hutang
  return totalDebt / selectedTenor.value; // Cicilan per bulan
});

// --- WhatsApp Links ---
// Link biasa untuk tombol hijau di atas
const waLink = computed(() => {
  if (!motor.value) return "#";
  const text = encodeURIComponent(
    `Halo Abu Motor! Saya tertarik dengan motor *${motor.value.brand} ${motor.value.model_name}* warna ${motor.value.color} seharga ${formatCurrency(motor.value.price)}. Apakah stoknya masih tersedia?`,
  );
  return `https://wa.me/${DEALER_WA_NUMBER}?text=${text}`;
});

// Link khusus dengan data simulasi kredit
const waLinkWithSimulation = computed(() => {
  if (!motor.value) return "#";
  const text = `Halo Abu Motor! Saya berminat membeli kendaraan berikut secara kredit:

*${motor.value.brand} ${motor.value.model_name}*
Warna: ${motor.value.color}
Harga OTR: ${formatCurrency(motor.value.price)}

*Rincian Simulasi Saya:*
- Uang Muka (DP): ${formatCurrency(dpAmount.value)} (${dpPercentage.value}%)
- Tenor: ${selectedTenor.value} Bulan
- Estimasi Cicilan: *${formatCurrency(monthlyInstallment.value)} / bulan*

Tolong pandu saya untuk proses pengajuannya. Terima kasih!`;
  return `https://wa.me/${DEALER_WA_NUMBER}?text=${encodeURIComponent(text)}`;
});

// --- State & Fungsi Wishlist ---
const isWishlisted = ref(false);
const showAuthModal = ref(false);

/// Fungsi untuk mengecek apakah user sudah menyimpan motor ini
const checkWishlistStatus = async (motorId) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    try {
      const res = await api.get(`/wishlist/check/${motorId}`);
      isWishlisted.value = res.data.is_wishlisted;
    } catch (error) {
      // Jika token kedaluwarsa atau tidak valid (401 / 422)
      if (
        error.response &&
        (error.response.status === 401 || error.response.status === 422)
      ) {
        console.warn("Sesi login berakhir. Mengembalikan status ke Guest.");
        // Hapus token yang sudah basi agar tidak nyangkut
        localStorage.removeItem("access_token");
        localStorage.removeItem("user_data");
      } else {
        console.error(
          "Gagal mengecek status wishlist:",
          error.response?.data || error.message,
        );
      }
    }
  }
};

const toggleWishlist = async () => {
  const token = localStorage.getItem("access_token");

  if (!token) {
    showAuthModal.value = true;
    return;
  }

  try {
    const res = await api.post("/wishlist/toggle", {
      motorcycle_id: motor.value.id,
    });

    isWishlisted.value = res.data.is_wishlisted;

    // Alert sederhana (bisa kamu ganti pakai Toast/Snackbar nanti biar lebih estetik)
    if (isWishlisted.value) {
      alert("❤️ Kendaraan berhasil disimpan ke Wishlist Anda!");
    } else {
      alert("💔 Kendaraan dihapus dari Wishlist.");
    }
  } catch (error) {
    alert("Terjadi kesalahan saat mengupdate Wishlist.");
  }
};

// --- Fungsi Share (Native Browser) ---
const shareVehicle = async () => {
  const url = window.location.href;
  const title = `Cek ${motor.value.brand} ${motor.value.model_name} di Abu Motor!`;
  const text = `Harganya cuma ${formatCurrency(motor.value.price)}. Kondisi ${motor.value.condition}, lihat detail lengkapnya di sini.`;

  if (navigator.share) {
    try {
      await navigator.share({
        title: title,
        text: text,
        url: url,
      });
    } catch (err) {
      console.log("Share dibatalkan oleh pengguna", err);
    }
  } else {
    // Fallback jika browser tidak support Web Share API (seperti Chrome PC lama)
    navigator.clipboard.writeText(url);
    alert("Link berhasil disalin ke clipboard!");
  }
};

// --- Fetch Data ---
const fetchMotorDetail = async () => {
  isLoading.value = true;
  try {
    const id = route.params.id;
    const response = await axios.get(`${BASE_URL}/api/inventory/${id}`);
    motor.value = response.data.data;

    // Set gambar aktif pertama kali
    activeImage.value = motor.value.image_url;

    checkWishlistStatus(motor.value.id);
  } catch (error) {
    console.error("Gagal mengambil data detail:", error);
    motor.value = null;
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchMotorDetail();
  window.scrollTo(0, 0);
});
</script>
