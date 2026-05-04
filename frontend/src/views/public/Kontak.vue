<template>
  <div class="min-h-screen bg-gray-50 font-sans flex flex-col">
    
    <PublicNavbar />

    <header class="bg-blue-600 text-white py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 class="text-3xl md:text-4xl font-extrabold mb-4">Hubungi Kami</h1>
        <p class="text-blue-100 max-w-2xl mx-auto">Punya pertanyaan seputar ketersediaan stok, simulasi kredit, atau layanan purna jual? Jangan ragu untuk menghubungi tim kami.</p>
      </div>
    </header>

    <main class="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 w-full">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        
        <div class="space-y-8">
          <div>
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Informasi Dealer</h2>
            
            <div class="space-y-6">
              <div class="flex items-start gap-4">
                <div class="bg-blue-100 p-3 rounded-xl text-blue-600 shrink-0">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.243-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                </div>
                <div>
                  <h4 class="font-semibold text-gray-900">Alamat Showroom</h4>
                  <p class="text-gray-600 mt-1 leading-relaxed">Timur Pom Bensin, Jetis, RT.3/RW.1, Sidan, Wonorejo, Kec. Polokarto <br> Kabupaten Sukoharjo, Jawa Tengah 57555</p>
                </div>
              </div>

              <div class="flex items-start gap-4">
                <div class="bg-blue-100 p-3 rounded-xl text-blue-600 shrink-0">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>
                </div>
                <div>
                  <h4 class="font-semibold text-gray-900">Telepon & WhatsApp</h4>
                  <p>0812-2244-4951 (Customer Service)</p>
                </div>
              </div>

              <!-- <div class="flex items-start gap-4">
                <div class="bg-blue-100 p-3 rounded-xl text-blue-600 shrink-0">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                </div>
                <div>
                  <h4 class="font-semibold text-gray-900">Email Address</h4>
                  <p class="text-gray-600 mt-1">halo@abumotor.com</p>
                </div>
              </div> -->

              <div class="flex items-start gap-4">
                <div class="bg-blue-100 p-3 rounded-xl text-blue-600 shrink-0">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </div>
                <div>
                  <h4 class="font-semibold text-gray-900">Jam Operasional</h4>
                  <p class="text-gray-600 mt-1">Setiap Hari : 08.00 - 16.00 WIB</p>
                  <p class="text-gray-500 text-sm mt-1">*Hari Libur Nasional Tutup</p>
                </div>
              </div>
            </div>
          </div>

          <div class="flex flex-col sm:flex-row gap-4 pt-6 border-t border-gray-200">
            <a :href="waLinkGeneral" target="_blank" class="flex-1 flex justify-center items-center gap-2 bg-green-500 hover:bg-green-600 text-white px-6 py-3.5 rounded-xl font-bold transition-colors shadow-md shadow-green-200">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 00-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .1 5.392.1 11.947c0 2.096.546 4.142 1.584 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.945-5.393 11.945-11.95a11.813 11.813 0 00-3.53-8.406z"/></svg>
              Chat WhatsApp
            </a>
            <a href="mailto:halo@abumotor.com" class="flex-1 flex justify-center items-center gap-2 bg-gray-900 hover:bg-gray-800 text-white px-6 py-3.5 rounded-xl font-bold transition-colors shadow-md">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
              Kirim Email
            </a>
          </div>
        </div>

        <div class="bg-gray-200 rounded-2xl overflow-hidden shadow-inner min-h-[400px]">
          <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d4804.3015034416!2d110.88343323083485!3d-7.611255076204905!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e7a3d3a52257ecd%3A0x432973e8d75e18de!2sABU%20MOTOR%20SIDAN!5e1!3m2!1sid!2sid!4v1772220400763!5m2!1sid!2sid" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>

      </div>
    </main>

    <PublicFooter />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import PublicNavbar from '../../components/PublicNavbar.vue';
import PublicFooter from '../../components/PublicFooter.vue';

const DEALER_WA_NUMBER = '6281222444951'; // Sesuaikan dengan nomor aslimu

const waLinkGeneral = computed(() => {
  const text = encodeURIComponent('Halo Abu Motor, saya melihat website Anda dan ingin bertanya mengenai produk/layanan.');
  return `https://wa.me/${DEALER_WA_NUMBER}?text=${text}`;
});
</script>