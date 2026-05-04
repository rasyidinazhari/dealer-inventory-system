<template>
  <footer
    class="bg-gray-900 text-gray-400 py-14 mt-auto border-t border-gray-800"
  >
    <div
      class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-12 gap-10"
    >
      <div class="md:col-span-5">
        <div class="flex items-center gap-2 mb-6">
          <router-link to="/" class="flex items-center gap-2">
            <img src="/abumotor-logo.png" alt="Abu Motor Logo" class="w-20" />
          </router-link>
          <!-- <svg
            class="w-8 h-8 text-blue-500"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M13 10V3L4 14h7v7l9-11h-7z"
            ></path>
          </svg> -->
          <span class="text-2xl font-black text-white tracking-tight"
            >Abu<span class="text-yellow-500">Motor</span></span
          >
        </div>
        <p class="text-sm leading-relaxed mb-6 text-gray-400 pr-4">
          Abu Motor adalah dealer resmi kendaraan roda dua & empat terpercaya.
          Kami menyediakan layanan penjualan Cash dan Kredit untuk berbagai
          merek motor unggulan dengan proses mudah, transparan, dan DP ringan.
          Komitmen kami adalah memberikan pelayanan terbaik bagi pelanggan di
          seluruh wilayah.
        </p>
        <div class="flex items-center gap-4">
          <a
            href="https://www.instagram.com/abu_motor/"
            class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-blue-600 hover:text-white transition-colors"
            target="_blank"
            ><svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path
                d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"
              /></svg
          ></a>
        </div>
      </div>

      <div class="md:col-span-3">
        <h4 class="text-white font-bold mb-6 uppercase tracking-wider text-sm">
          Navigasi Cepat
        </h4>
        <ul class="space-y-3 text-sm">
          <li>
            <router-link
              to="/"
              class="hover:text-blue-400 transition-colors flex items-center gap-2"
              ><span class="w-1.5 h-1.5"></span> Beranda</router-link
            >
          </li>
          <li>
            <router-link
              to="/katalog"
              class="hover:text-blue-400 transition-colors flex items-center gap-2"
              ><span class="w-1.5 h-1.5"></span> Katalog</router-link
            >
          </li>
          <li>
            <router-link
              to="/kontak"
              class="hover:text-blue-400 transition-colors flex items-center gap-2"
              ><span class="w-1.5 h-1.5"></span> Hubungi Kami</router-link
            >
          </li>
          <li>
            <router-link
              to="/blog"
              class="hover:text-blue-400 transition-colors flex items-center gap-2"
              ><span class="w-1.5 h-1.5"></span> Blog</router-link
            >
          </li>
        </ul>
      </div>

      <div class="md:col-span-4">
        <h4 class="text-white font-bold mb-6 uppercase tracking-wider text-sm">
          Hubungi Kami
        </h4>
        <ul class="space-y-4 text-sm">
          <li class="flex items-start gap-3">
            <svg
              class="w-5 h-5 text-gray-500 mt-0.5 shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.243-4.243a8 8 0 1111.314 0z"
              ></path>
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
              ></path>
            </svg>
            <span class="leading-relaxed"
              >Timur Pom Bensin, Jetis, RT.3/RW.1, Sidan, Wonorejo, Kec.
              Polokarto, Kabupaten Sukoharjo, Jawa Tengah 57555</span
            >
          </li>
          <li class="flex items-center gap-3">
            <svg
              class="w-5 h-5 text-gray-500 shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
              ></path>
            </svg>
            <span>0812-2244-4951</span>
          </li>
        </ul>
      </div>
    </div>

    <div
      class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-12 pt-8 border-t border-gray-800 flex justify-center text-xs md:text-sm"
    >
      <p>
        &copy; {{ new Date().getFullYear() }} Abu Motor Dealer. Hak Cipta
        Dilindungi.
      </p>
    </div>
  </footer>
</template>
