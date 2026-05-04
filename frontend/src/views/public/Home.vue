<template>
  <div class="min-h-screen bg-gray-50 font-sans flex flex-col">
    
    <PublicNavbar />
    
    <!-- BANNER SECTION (Modern Centered Carousel) -->
    <header class="pt-8 pb-4 bg-white overflow-hidden relative">
      <!-- Carousel Track -->
      <div 
        ref="bannerScroll"
        class="flex gap-4 md:gap-6 overflow-x-auto snap-x snap-mandatory hide-scrollbar px-[7.5vw] md:px-[15vw] items-center"
        @scroll="handleScroll"
      >
        <template v-if="banners.length > 0">
          <div 
            v-for="(banner, index) in banners" 
            :key="banner.id"
            class="w-[85vw] md:w-[70vw] h-[200px] sm:h-[300px] md:h-[400px] shrink-0 snap-center rounded-3xl overflow-hidden relative transition-all duration-500 cursor-pointer"
            :class="currentSlide === index ? 'scale-100 opacity-100 shadow-xl' : 'scale-95 opacity-50 shadow-md'"
            @click="scrollToSlide(index)"
          >
            <component 
              :is="banner.link_url ? (banner.link_url.startsWith('http') ? 'a' : 'router-link') : 'div'"
              :[banner.link_url?.startsWith('http')?'href':'to']="banner.link_url"
              :target="banner.link_url?.startsWith('http') ? '_blank' : null"
              class="block w-full h-full"
            >
              <img :src="getImageUrl(banner.image_url)" class="w-full h-full object-cover" :alt="banner.title || 'Promo Banner'">
              
              <div v-if="banner.title" class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-black/80 via-black/40 to-transparent p-6 sm:p-10 pt-24 text-left">
                <div class="max-w-7xl mx-auto">
                  <h2 class="text-xl md:text-4xl font-extrabold text-white tracking-tight drop-shadow-md">{{ banner.title }}</h2>
                </div>
              </div>
            </component>
          </div>
        </template>

        <!-- FALLBACK BANNERS (Jika API Kosong) -->
        <template v-else>
          <div 
            class="w-[85vw] md:w-[70vw] h-[200px] sm:h-[300px] md:h-[400px] shrink-0 snap-center rounded-3xl overflow-hidden relative bg-gradient-to-r from-blue-900 to-blue-600 flex items-center justify-center transition-all duration-500 cursor-pointer"
            :class="currentSlide === 0 ? 'scale-100 opacity-100 shadow-xl' : 'scale-95 opacity-50 shadow-md'"
            @click="scrollToSlide(0)"
          >
            <div class="absolute inset-0 opacity-20 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')]"></div>
            <div class="text-center px-4 relative z-10">
              <span class="inline-block py-1 px-3 rounded-full bg-blue-500/30 text-blue-100 text-[10px] md:text-sm font-semibold mb-2 md:mb-4 backdrop-blur-sm border border-blue-400/50">Promo Spesial Awal Tahun</span>
              <h2 class="text-2xl md:text-5xl font-extrabold text-white mb-2 md:mb-4 tracking-tight">Kredit DP 0 Rupiah!</h2>
              <p class="text-blue-100 text-xs md:text-xl max-w-2xl mx-auto mb-4 md:mb-8">Bawa pulang kendaraan impianmu hari ini juga. Proses cepat dan cicilan ringan.</p>
              <router-link to="/katalog" class="bg-white text-blue-600 px-6 py-2 md:px-8 md:py-3 rounded-full text-sm md:text-base font-bold hover:bg-gray-100 transition shadow-lg">Cari Sekarang</router-link>
            </div>
          </div>

          <div 
            class="w-[85vw] md:w-[70vw] h-[200px] sm:h-[300px] md:h-[400px] shrink-0 snap-center rounded-3xl overflow-hidden relative bg-gradient-to-r from-emerald-800 to-teal-600 flex items-center justify-center transition-all duration-500 cursor-pointer"
            :class="currentSlide === 1 ? 'scale-100 opacity-100 shadow-xl' : 'scale-95 opacity-50 shadow-md'"
            @click="scrollToSlide(1)"
          >
            <div class="absolute inset-0 opacity-20 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')]"></div>
            <div class="text-center px-4 relative z-10">
              <span class="inline-block py-1 px-3 rounded-full bg-emerald-500/30 text-emerald-100 text-[10px] md:text-sm font-semibold mb-2 md:mb-4 backdrop-blur-sm border border-emerald-400/50">Cashback Hingga 2 Juta</span>
              <h2 class="text-2xl md:text-5xl font-extrabold text-white mb-2 md:mb-4 tracking-tight">Potongan Maksimal</h2>
              <p class="text-emerald-100 text-xs md:text-xl max-w-2xl mx-auto mb-4 md:mb-8">Dapatkan diskon besar-besaran untuk pembelian unit secara tunai bulan ini.</p>
              <a :href="waLinkGeneral" target="_blank" class="bg-emerald-500 text-white border border-emerald-400 px-6 py-2 md:px-8 md:py-3 rounded-full text-sm md:text-base font-bold hover:bg-emerald-400 transition shadow-lg">Klaim Promo via WA</a>
            </div>
          </div>
        </template>
      </div>

      <!-- Navigation Arrows -->
      <button v-if="totalSlides > 1" @click="prevSlide" class="hidden md:flex absolute left-[5vw] top-1/2 -translate-y-1/2 bg-white/90 hover:bg-white text-gray-800 p-3 rounded-full shadow-lg backdrop-blur-sm transition z-10 focus:outline-none">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
      </button>
      <button v-if="totalSlides > 1" @click="nextSlide" class="hidden md:flex absolute right-[5vw] top-1/2 -translate-y-1/2 bg-white/90 hover:bg-white text-gray-800 p-3 rounded-full shadow-lg backdrop-blur-sm transition z-10 focus:outline-none">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
      </button>

      <!-- Dots Indicators -->
      <div v-if="totalSlides > 1" class="flex justify-center gap-2 mt-6">
        <button 
          v-for="n in totalSlides" :key="n" 
          @click="scrollToSlide(n-1)" 
          :class="currentSlide === n-1 ? 'bg-blue-600 w-8 shadow-sm' : 'bg-gray-300 w-2 hover:bg-gray-400'" 
          class="h-2 rounded-full transition-all duration-300 focus:outline-none"
        ></button>
      </div>
    </header>

    <!-- KATEGORI KENDARAAN (Dipindah ke Bawah Banner & Diberi Ruang Bebas) -->
    <!-- KATEGORI KENDARAAN (Desain Ikon E-Commerce) -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full mt-8 mb-10 relative z-20">
      <div class="flex overflow-x-auto gap-3 sm:gap-6 pb-4 hide-scrollbar snap-x justify-center">
        
        <!-- 1. Lihat Semua -->
        <router-link to="/katalog" class="flex flex-col items-center group cursor-pointer w-[75px] sm:w-[90px] shrink-0 snap-start">
          <div class="w-14 h-14 sm:w-[60px] sm:h-[60px] bg-[#F0F5FF] rounded-2xl flex items-center justify-center text-blue-600 transition-transform duration-300 group-hover:scale-105">
            <svg class="w-6 h-6 sm:w-7 sm:h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
          </div>
          <span class="mt-2 text-[11px] sm:text-xs font-medium text-gray-700 text-center leading-tight group-hover:text-blue-600">Lihat Semua</span>
        </router-link>

        <!-- 2. Mobil Baru -->
        <router-link to="/katalog?type=Mobil&condition=Baru" class="flex flex-col items-center group cursor-pointer w-[75px] sm:w-[90px] shrink-0 snap-start">
          <div class="w-14 h-14 sm:w-[60px] sm:h-[60px] bg-[#F0F5FF] rounded-2xl flex items-center justify-center text-blue-600 transition-transform duration-300 group-hover:scale-105">
            <svg class="w-6 h-6 sm:w-7 sm:h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 13h2l2-6h10l2 6h2v5a2 2 0 01-2 2h-1v-2a2 2 0 00-2-2H8a2 2 0 00-2 2v2H5a2 2 0 01-2-2v-5z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13L7 7h10l2 6M7 17a2 2 0 11-4 0 2 2 0 014 0zM21 17a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
          </div>
          <span class="mt-2 text-[11px] sm:text-xs font-medium text-gray-700 text-center leading-tight group-hover:text-blue-600">Mobil Baru</span>
        </router-link>

        <!-- 3. Mobil Bekas -->
        <router-link to="/katalog?type=Mobil&condition=Bekas" class="flex flex-col items-center group cursor-pointer w-[75px] sm:w-[90px] shrink-0 snap-start">
          <div class="w-14 h-14 sm:w-[60px] sm:h-[60px] bg-[#F0F5FF] rounded-2xl flex items-center justify-center text-blue-600 transition-transform duration-300 group-hover:scale-105">
            <svg class="w-6 h-6 sm:w-7 sm:h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 13h2l2-6h10l2 6h2v5a2 2 0 01-2 2h-1v-2a2 2 0 00-2-2H8a2 2 0 00-2 2v2H5a2 2 0 01-2-2v-5z"></path></svg>
          </div>
          <span class="mt-2 text-[11px] sm:text-xs font-medium text-gray-700 text-center leading-tight group-hover:text-blue-600">Mobil Bekas</span>
        </router-link>

        <!-- 4. Motor Baru -->
        <router-link to="/katalog?type=Motor&condition=Baru" class="flex flex-col items-center group cursor-pointer w-[75px] sm:w-[90px] shrink-0 snap-start">
          <div class="w-14 h-14 sm:w-[60px] sm:h-[60px] bg-[#F0F5FF] rounded-2xl flex items-center justify-center text-blue-600 transition-transform duration-300 group-hover:scale-105">
            <Motorbike class="w-6 h-6 sm:w-7 sm:h-7" />
          </div>
          <span class="mt-2 text-[11px] sm:text-xs font-medium text-gray-700 text-center leading-tight group-hover:text-blue-600">Motor Baru</span>
        </router-link>

        <!-- 5. Motor Bekas -->
        <router-link to="/katalog?type=Motor&condition=Bekas" class="flex flex-col items-center group cursor-pointer w-[75px] sm:w-[90px] shrink-0 snap-start">
          <div class="w-14 h-14 sm:w-[60px] sm:h-[60px] bg-[#F0F5FF] rounded-2xl flex items-center justify-center text-blue-600 transition-transform duration-300 group-hover:scale-105">
            <Motorbike class="w-6 h-6 sm:w-7 sm:h-7" />
          </div>
          <span class="mt-2 text-[11px] sm:text-xs font-medium text-gray-700 text-center leading-tight group-hover:text-blue-600">Motor Bekas</span>
        </router-link>
        
        <!-- 6. Menu Tambahan (Bisa digeser) -->
        <!-- <a :href="waLinkGeneral" target="_blank" class="flex flex-col items-center group cursor-pointer w-[75px] sm:w-[90px] shrink-0 snap-start">
          <div class="w-14 h-14 sm:w-[60px] sm:h-[60px] bg-[#F0F5FF] rounded-2xl flex items-center justify-center text-blue-600 transition-transform duration-300 group-hover:scale-105">
            <svg class="w-6 h-6 sm:w-7 sm:h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          </div>
          <span class="mt-2 text-[11px] sm:text-xs font-medium text-gray-700 text-center leading-tight group-hover:text-blue-600">Promo</span>
        </a> -->
        
        <!-- 7. Menu Tambahan (Bisa digeser) -->
        <router-link to="/blog" class="flex flex-col items-center group cursor-pointer w-[75px] sm:w-[90px] shrink-0 snap-start">
          <div class="w-14 h-14 sm:w-[60px] sm:h-[60px] bg-[#F0F5FF] rounded-2xl flex items-center justify-center text-blue-600 transition-transform duration-300 group-hover:scale-105">
            <svg class="w-6 h-6 sm:w-7 sm:h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path></svg>
          </div>
          <span class="mt-2 text-[11px] sm:text-xs font-medium text-gray-700 text-center leading-tight group-hover:text-blue-600">Berita</span>
        </router-link>

      </div>
    </section>

    <!-- MAIN KATALOG CONTENT -->
    <main class="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16 w-full">
      
      <div v-if="isLoading" class="flex justify-center py-12">
        <div class="animate-pulse flex flex-col items-center">
          <div class="h-10 w-10 bg-blue-200 rounded-full mb-4"></div>
          <p class="text-gray-500">Memuat data kendaraan...</p>
        </div>
      </div>

      <div v-else class="space-y-12 sm:space-y-16 mt-6 sm:mt-0">
        
        <!-- SECTION MOTOR BEKAS -->
        <section v-if="motorSecond.length > 0">
          <div class="flex items-center justify-between mb-4 sm:mb-6 border-b-2 border-blue-500 pb-2">
            <h2 class="text-xl sm:text-2xl font-bold text-gray-900 truncate pr-2">Motor Second Pilihan</h2>
            <router-link to="/katalog?type=Motor&condition=Bekas" class="text-xs sm:text-sm font-bold text-blue-600 hover:text-blue-800 shrink-0">Lihat Semua &rarr;</router-link>
          </div>
          <div class="flex overflow-x-auto gap-4 sm:gap-6 pb-6 snap-x snap-mandatory hide-scrollbar -mx-4 px-4 sm:mx-0 sm:px-0">
            <!-- Ubah lebar w-[280px] menjadi w-[220px] di mobile, sm:w-[280px] di desktop -->
            <router-link v-for="motor in motorSecond" :key="motor.id" :to="'/motor/' + motor.id" class="w-[220px] sm:w-[280px] shrink-0 snap-start bg-white rounded-xl sm:rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg transition-shadow duration-300 flex flex-col group block">
              <div class="h-36 sm:h-48 bg-gray-50 relative flex items-center justify-center overflow-hidden">
                <img v-if="motor.image_url" :src="getImageUrl(motor.image_url)" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                <span class="absolute top-2 right-2 sm:top-3 sm:right-3 bg-white/90 px-1.5 sm:px-2 py-0.5 sm:py-1 rounded text-[10px] sm:text-xs font-bold text-gray-700">{{ motor.brand }}</span>
                <span v-if="motor.branch_name" class="absolute bottom-2 left-2 sm:bottom-3 sm:left-3 bg-blue-600/90 text-white px-1.5 sm:px-2 py-0.5 sm:py-1 rounded text-[9px] sm:text-[10px] font-bold">{{ motor.branch_name }}</span>
              </div>
              <div class="p-3 sm:p-5 flex-1 flex flex-col">
                <h3 class="text-base sm:text-lg font-bold text-gray-900 mb-1 line-clamp-1">{{ motor.model_name }}</h3>
                <p class="text-xs sm:text-sm text-gray-500 mb-3 sm:mb-4">{{ motor.year }} | {{ motor.mileage }}</p>
                <div class="mt-auto">
                  <p class="text-lg sm:text-xl font-black text-blue-600 truncate" :title="formatCurrency(motor.price)">{{ formatCurrency(motor.price) }}</p>
                </div>
              </div>
            </router-link>
          </div>
        </section>

        <!-- SECTION MOTOR BARU -->
        <section v-if="motorBaru.length > 0">
          <div class="flex items-center justify-between mb-4 sm:mb-6 border-b-2 border-blue-500 pb-2">
            <h2 class="text-xl sm:text-2xl font-bold text-gray-900 truncate pr-2">Motor Baru Terpopuler</h2>
            <router-link to="/katalog?type=Motor&condition=Baru" class="text-xs sm:text-sm font-bold text-blue-600 hover:text-blue-800 shrink-0">Lihat Semua &rarr;</router-link>
          </div>
          <div class="flex overflow-x-auto gap-4 sm:gap-6 pb-6 snap-x snap-mandatory hide-scrollbar -mx-4 px-4 sm:mx-0 sm:px-0">
            <router-link v-for="motor in motorBaru" :key="motor.id" :to="'/motor/' + motor.id" class="w-[220px] sm:w-[280px] shrink-0 snap-start bg-white rounded-xl sm:rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg transition-shadow duration-300 flex flex-col group block">
              <div class="h-36 sm:h-48 bg-gray-50 relative flex items-center justify-center overflow-hidden">
                <img v-if="motor.image_url" :src="getImageUrl(motor.image_url)" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                <span class="absolute top-2 left-2 sm:top-3 sm:left-3 bg-indigo-500 text-white px-1.5 sm:px-2 py-0.5 sm:py-1 rounded text-[10px] sm:text-xs font-bold">NEW</span>
                <span v-if="motor.branch_name" class="absolute bottom-2 left-2 sm:bottom-3 sm:left-3 bg-blue-600/90 text-white px-1.5 sm:px-2 py-0.5 sm:py-1 rounded text-[9px] sm:text-[10px] font-bold">{{ motor.branch_name }}</span>
              </div>
              <div class="p-3 sm:p-5 flex-1 flex flex-col">
                <h3 class="text-base sm:text-lg font-bold text-gray-900 mb-1 line-clamp-1">{{ motor.model_name }}</h3>
                <p class="text-xs sm:text-sm text-gray-500 mb-3 sm:mb-4">Stock: {{ motor.stock }} unit</p>
                <div class="mt-auto">
                  <p class="text-lg sm:text-xl font-black text-blue-600 truncate" :title="formatCurrency(motor.price)">{{ formatCurrency(motor.price) }}</p>
                </div>
              </div>
            </router-link>
          </div>
        </section>

        <!-- SECTION MOBIL BEKAS -->
        <section v-if="mobilSecond.length > 0">
          <div class="flex items-center justify-between mb-4 sm:mb-6 border-b-2 border-indigo-500 pb-2">
            <h2 class="text-xl sm:text-2xl font-bold text-gray-900 truncate pr-2">Mobil Second Berkualitas</h2>
            <router-link to="/katalog?type=Mobil&condition=Bekas" class="text-xs sm:text-sm font-bold text-indigo-600 hover:text-indigo-800 shrink-0">Lihat Semua &rarr;</router-link>
          </div>
          <div class="flex overflow-x-auto gap-4 sm:gap-6 pb-6 snap-x snap-mandatory hide-scrollbar -mx-4 px-4 sm:mx-0 sm:px-0">
            <router-link v-for="motor in mobilSecond" :key="motor.id" :to="'/motor/' + motor.id" class="w-[220px] sm:w-[280px] shrink-0 snap-start bg-white rounded-xl sm:rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg transition-shadow duration-300 flex flex-col group block">
              <div class="h-36 sm:h-48 bg-gray-50 relative flex items-center justify-center overflow-hidden">
                <img v-if="motor.image_url" :src="getImageUrl(motor.image_url)" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                <span class="absolute top-2 right-2 sm:top-3 sm:right-3 bg-white/90 px-1.5 sm:px-2 py-0.5 sm:py-1 rounded text-[10px] sm:text-xs font-bold text-gray-700">{{ motor.brand }}</span>
                <span v-if="motor.branch_name" class="absolute bottom-2 left-2 sm:bottom-3 sm:left-3 bg-indigo-600/90 text-white px-1.5 sm:px-2 py-0.5 sm:py-1 rounded text-[9px] sm:text-[10px] font-bold">{{ motor.branch_name }}</span>
              </div>
              <div class="p-3 sm:p-5 flex-1 flex flex-col">
                <h3 class="text-base sm:text-lg font-bold text-gray-900 mb-1 line-clamp-1">{{ motor.model_name }}</h3>
                <p class="text-xs sm:text-sm text-gray-500 mb-3 sm:mb-4">{{ motor.year }} | {{ motor.transmission }}</p>
                <div class="mt-auto">
                  <p class="text-lg sm:text-xl font-black text-indigo-600 truncate" :title="formatCurrency(motor.price)">{{ formatCurrency(motor.price) }}</p>
                </div>
              </div>
            </router-link>
          </div>
        </section>

        <!-- SECTION MOBIL BARU -->
        <section v-if="mobilBaru.length > 0">
          <div class="flex items-center justify-between mb-4 sm:mb-6 border-b-2 border-indigo-500 pb-2">
            <h2 class="text-xl sm:text-2xl font-bold text-gray-900 truncate pr-2">Mobil Baru Istimewa</h2>
            <router-link to="/katalog?type=Mobil&condition=Baru" class="text-xs sm:text-sm font-bold text-indigo-600 hover:text-indigo-800 shrink-0">Lihat Semua &rarr;</router-link>
          </div>
          <div class="flex overflow-x-auto gap-4 sm:gap-6 pb-6 snap-x snap-mandatory hide-scrollbar -mx-4 px-4 sm:mx-0 sm:px-0">
            <router-link v-for="motor in mobilBaru" :key="motor.id" :to="'/motor/' + motor.id" class="w-[220px] sm:w-[280px] shrink-0 snap-start bg-white rounded-xl sm:rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg transition-shadow duration-300 flex flex-col group block">
              <div class="h-36 sm:h-48 bg-gray-50 relative flex items-center justify-center overflow-hidden">
                <img v-if="motor.image_url" :src="getImageUrl(motor.image_url)" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                <span class="absolute top-2 left-2 sm:top-3 sm:left-3 bg-indigo-500 text-white px-1.5 sm:px-2 py-0.5 sm:py-1 rounded text-[10px] sm:text-xs font-bold">NEW</span>
                <span v-if="motor.branch_name" class="absolute bottom-2 left-2 sm:bottom-3 sm:left-3 bg-indigo-600/90 text-white px-1.5 sm:px-2 py-0.5 sm:py-1 rounded text-[9px] sm:text-[10px] font-bold">{{ motor.branch_name }}</span>
              </div>
              <div class="p-3 sm:p-5 flex-1 flex flex-col">
                <h3 class="text-base sm:text-lg font-bold text-gray-900 mb-1 line-clamp-1">{{ motor.model_name }}</h3>
                <p class="text-xs sm:text-sm text-gray-500 mb-3 sm:mb-4">{{ motor.brand }} | {{ motor.transmission }}</p>
                <div class="mt-auto">
                  <p class="text-lg sm:text-xl font-black text-indigo-600 truncate" :title="formatCurrency(motor.price)">{{ formatCurrency(motor.price) }}</p>
                </div>
              </div>
            </router-link>
          </div>
        </section>

      </div>
    </main>
    
    <section class="py-16 bg-white border-t border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-4">
          <div>
            <h2 class="text-3xl font-extrabold text-gray-900 sm:text-4xl">Kabar & Tips Otomotif</h2>
            <p class="mt-3 text-lg text-gray-500">Informasi terbaru seputar perawatan kendaraan dan promo dealer kami.</p>
          </div>
          <router-link to="/blog" class="hidden md:inline-flex items-center text-blue-600 font-bold hover:text-blue-800 transition-colors">
            Lihat Semua Artikel 
            <svg class="w-5 h-5 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
          </router-link>
        </div>

        <div v-if="isLoadingArticles" class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="i in 3" :key="i" class="animate-pulse flex flex-col bg-gray-50 rounded-2xl h-[400px] border border-gray-100">
             <div class="h-48 bg-gray-200 rounded-t-2xl"></div>
             <div class="p-6 space-y-4">
               <div class="h-4 bg-gray-200 rounded w-1/3"></div>
               <div class="h-6 bg-gray-200 rounded w-3/4"></div>
               <div class="h-4 bg-gray-200 rounded w-full"></div>
               <div class="h-4 bg-gray-200 rounded w-5/6"></div>
             </div>
          </div>
        </div>
        
        <div v-else-if="latestArticles.length === 0" class="text-center py-12 bg-gray-50 rounded-2xl border border-dashed border-gray-300">
          <p class="text-gray-500 font-medium">Belum ada artikel yang diterbitkan.</p>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <article v-for="article in latestArticles" :key="article.id" class="flex flex-col bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 group">
            <router-link :to="`/blog/${article.slug}`" class="block overflow-hidden h-52 shrink-0 relative">
              <img v-if="article.image_url" :src="getImageUrl(article.image_url)" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" :alt="article.title">
            </router-link>
            
            <div class="p-6 flex flex-col flex-1">
              <div class="flex items-center text-xs text-gray-500 mb-3 gap-2">
                <span class="font-bold text-blue-600 uppercase tracking-wider">{{ article.author_name || 'Admin' }}</span>
                <span>•</span>
                <span>{{ article.created_at }}</span>
              </div>
              <router-link :to="`/blog/${article.slug}`" class="flex-1 block">
                <h3 class="text-xl font-bold text-gray-900 mb-3 group-hover:text-blue-600 transition-colors line-clamp-2">{{ article.title }}</h3>
                <p class="text-gray-600 text-sm line-clamp-3 mb-4 leading-relaxed">{{ article.content }}</p>
              </router-link>
            </div>
          </article>
        </div>
      </div>
    </section>
    
    <PublicFooter />

  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue';
import api from '../../services/api';
import axios from 'axios';
import PublicNavbar from '../../components/PublicNavbar.vue';
import PublicFooter from '../../components/PublicFooter.vue';
import { Motorbike } from 'lucide-vue-next';

const latestArticles = ref([]); 
const isLoadingArticles = ref(true); 
const DEALER_WA_NUMBER = '6281222444951'; 
const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5001';

const isLoading = ref(true);
const motors = ref([]);

// --- LOGIKA BANNER (NATIVE SCROLL-SNAP CAROUSEL) ---
const banners = ref([]);
const currentSlide = ref(0);
const bannerScroll = ref(null);
let slideInterval;

const totalSlides = computed(() => banners.value.length > 0 ? banners.value.length : 2);

// Sinkronisasi posisi scroll dengan dot active indicator
const handleScroll = () => {
  if (!bannerScroll.value || bannerScroll.value.children.length === 0) return;
  const scrollLeft = bannerScroll.value.scrollLeft;
  const slideWidth = bannerScroll.value.children[0].offsetWidth;
  currentSlide.value = Math.round(scrollLeft / slideWidth);
};

// Auto scroll element ke tengah layar berkat snap-center padding
// Auto scroll elemen secara horizontal TANPA memicu lompatan vertikal
const scrollToSlide = (index) => {
  if (!bannerScroll.value) return;
  
  const container = bannerScroll.value;
  const slide = container.children[index];
  
  if (slide) {
    // Hitung posisi persis di tengah
    const scrollPosition = slide.offsetLeft - (container.offsetWidth - slide.offsetWidth) / 2;
    
    // Gunakan scrollTo pada container, bukan scrollIntoView pada elemen
    container.scrollTo({
      left: scrollPosition,
      behavior: 'smooth'
    });
    
    resetSlideShow(); // Reset timer saat ditekan manual atau otomatis
  }
};

const nextSlide = () => { 
  const next = (currentSlide.value + 1) % totalSlides.value;
  scrollToSlide(next);
};

const prevSlide = () => { 
  const prev = (currentSlide.value - 1 + totalSlides.value) % totalSlides.value;
  scrollToSlide(prev);
};

const startSlideShow = () => { 
  slideInterval = setInterval(nextSlide, 5000); 
};

const resetSlideShow = () => {
  clearInterval(slideInterval);
  startSlideShow();
};

const fetchBanners = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/api/banners/public`);
    banners.value = response.data.data;
  } catch (error) {
    console.error('Gagal mengambil banner:', error);
  }
};
// -----------------------------

const motorSecond = computed(() => motors.value.filter(m => m.vehicle_type === 'Motor' && m.condition === 'Bekas' && m.is_active && m.stock > 0).slice(0, 4));
const motorBaru = computed(() => motors.value.filter(m => m.vehicle_type === 'Motor' && m.condition === 'Baru' && m.is_active && m.stock > 0).slice(0, 4));
const mobilSecond = computed(() => motors.value.filter(m => m.vehicle_type === 'Mobil' && m.condition === 'Bekas' && m.is_active && m.stock > 0).slice(0, 4));
const mobilBaru = computed(() => motors.value.filter(m => m.vehicle_type === 'Mobil' && m.condition === 'Baru' && m.is_active && m.stock > 0).slice(0, 4));

const formatCurrency = (value) => {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(value || 0);
};

const getImageUrl = (url) => {
  if (!url) return null;
  return `${BASE_URL}${url}?t=${new Date().getTime()}`;
};

const waLinkGeneral = computed(() => {
  const text = encodeURIComponent('Halo Abu Motor, saya ingin konsultasi mengenai promo dan pembelian kendaraan.');
  return `https://wa.me/${DEALER_WA_NUMBER}?text=${text}`;
});

const fetchKatalog = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get(`${BASE_URL}/api/inventory/`);
    motors.value = response.data.data.reverse(); 
  } catch (error) {
    console.error('Gagal mengambil data katalog:', error);
  } finally {
    isLoading.value = false;
  }
};

const fetchLatestArticles = async () => {
  try {
    const res = await api.get('/articles/public?limit=3');
    latestArticles.value = res.data.data || [];
  } catch (error) {
    console.error("Gagal memuat artikel", error);
    latestArticles.value = []; 
  } finally {
    isLoadingArticles.value = false;
  }
};

onMounted(async () => {
  await Promise.all([
    fetchBanners(),
    fetchKatalog(),
    fetchLatestArticles()
  ]);
  startSlideShow();
});

onUnmounted(() => {
  clearInterval(slideInterval);
});
</script>

<style scoped>
/* Sembunyikan scrollbar native agar terlihat premium seperti aplikasi mobile */
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>