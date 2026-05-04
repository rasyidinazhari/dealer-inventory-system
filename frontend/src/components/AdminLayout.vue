<template>
  <div class="flex h-screen overflow-hidden font-sans bg-gray-50">
    <!-- Overlay untuk Mobile -->
    <div
      v-if="isSidebarOpen"
      @click="isSidebarOpen = false"
      class="fixed inset-0 z-20 transition-opacity bg-gray-800 bg-opacity-50 lg:hidden"
    ></div>

    <!-- SIDEBAR -->
    <aside
      class="fixed inset-y-0 left-0 z-30 flex flex-col transition-all duration-300 ease-in-out transform bg-white border-r border-gray-200 shadow-lg lg:shadow-sm lg:static"
      :class="[
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',
        isSidebarCollapsed ? 'lg:w-20' : 'w-64',
      ]"
    >
      <!-- HEADER SIDEBAR (Logo & Tombol Collapse) -->
      <div
        class="flex items-center h-16 border-b border-gray-100 shrink-0 transition-all overflow-hidden"
        :class="
          isSidebarCollapsed
            ? 'justify-center gap-1.5 px-2'
            : 'justify-between px-6'
        "
      >
        <!-- Logo Layar Lebar -->
        <a href="/">
          <img
            v-if="!isSidebarCollapsed"
            src="/abumotor-logo.png"
            alt="abu motor logo"
            class="w-20 shrink-0"
          />

          <!-- Logo Layar Minimize (Ubah jadi object-contain agar tidak terpotong) -->
          <img
            v-else
            src="/abumotor-logo.png"
            alt="logo"
            class="object-contain w-9 shrink-0"
          />
        </a>

        <!-- Tombol Close Mobile -->
        <button
          @click="isSidebarOpen = false"
          class="text-gray-500 lg:hidden hover:text-gray-700 shrink-0"
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
              d="M6 18L18 6M6 6l12 12"
            ></path>
          </svg>
        </button>

        <!-- Tombol Collapse Desktop (Margin dan Padding disesuaikan) -->
        <button
          @click="isSidebarCollapsed = !isSidebarCollapsed"
          class="hidden lg:flex p-1 rounded-lg text-gray-500 hover:text-gray-800 hover:bg-gray-100 transition-colors shrink-0"
        >
          <svg
            v-if="!isSidebarCollapsed"
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M11 19l-7-7 7-7m8 14l-7-7 7-7"
            ></path>
          </svg>
          <svg
            v-else
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M13 5l7 7-7 7M5 5l7 7-7 7"
            ></path>
          </svg>
        </button>
      </div>

      <!-- MENU NAVIGASI UTAMA -->
      <nav class="flex-1 px-3 py-4 space-y-1 overflow-x-hidden overflow-y-auto">
        <!-- Manajemen Group -->
        <div
          class="pt-4 pb-2"
          v-if="
            ['super_admin', 'cs', 'admin_cabang', 'finance'].includes(userRole)
          "
        >
          <p
            v-if="!isSidebarCollapsed"
            class="px-3 text-xs font-semibold tracking-wider text-gray-400 uppercase truncate"
          >
            Manajemen
          </p>
          <p v-else class="font-bold text-center text-gray-300">•••</p>
        </div>

        <router-link
          v-if="['super_admin', 'cs', 'admin_cabang'].includes(userRole)"
          to="/admin/inventory"
          @click="isSidebarOpen = false"
          class="flex items-center group nav-link"
          :class="isSidebarCollapsed ? 'justify-center px-0' : 'gap-3 px-3'"
          active-class="active-link"
          title="Stok Kendaraan"
        >
          <svg
            class="w-5 h-5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
            />
          </svg>
          <span v-if="!isSidebarCollapsed" class="truncate"
            >Stok Kendaraan</span
          >
        </router-link>

        <router-link
          v-if="['super_admin', 'admin_cabang'].includes(userRole)"
          to="/admin/validasi-eksternal"
          @click="isSidebarOpen = false"
          class="flex items-center group nav-link"
          :class="isSidebarCollapsed ? 'justify-center px-0' : 'gap-3 px-3'"
          active-class="active-link"
          title="Validasi Seller"
        >
          <svg
            class="w-5 h-5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
            />
          </svg>
          <span v-if="!isSidebarCollapsed" class="truncate"
            >Validasi Seller</span
          >
        </router-link>

        <router-link
          v-if="
            ['super_admin', 'finance', 'cs', 'admin_cabang'].includes(userRole)
          "
          to="/admin/sales"
          @click="isSidebarOpen = false"
          class="flex items-center group nav-link"
          :class="isSidebarCollapsed ? 'justify-center px-0' : 'gap-3 px-3'"
          active-class="active-link"
          title="Penjualan & Kredit"
        >
          <svg
            class="w-5 h-5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
            />
          </svg>
          <span v-if="!isSidebarCollapsed" class="truncate"
            >Penjualan & Kredit</span
          >
        </router-link>

        <router-link
          v-if="['super_admin', 'finance', 'admin_cabang'].includes(userRole)"
          to="/admin/finance"
          @click="isSidebarOpen = false"
          class="flex items-center group nav-link"
          :class="isSidebarCollapsed ? 'justify-center px-0' : 'gap-3 px-3'"
          active-class="active-link"
          title="Laporan Keuangan"
        >
          <svg
            class="w-5 h-5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
          </svg>
          <span v-if="!isSidebarCollapsed" class="truncate"
            >Laporan Keuangan</span
          >
        </router-link>

        <!-- Master Data Group -->
        <div
          class="pt-4 pb-2"
          v-if="
            ['super_admin', 'cs', 'admin_cabang', 'finance'].includes(userRole)
          "
        >
          <p
            v-if="!isSidebarCollapsed"
            class="px-3 text-xs font-semibold tracking-wider text-gray-400 uppercase truncate"
          >
            Master Data
          </p>
          <p v-else class="font-bold text-center text-gray-300">•••</p>
        </div>

        <router-link
          v-if="['super_admin', 'cs', 'admin_cabang'].includes(userRole)"
          to="/admin/customers"
          @click="isSidebarOpen = false"
          class="flex items-center group nav-link"
          :class="isSidebarCollapsed ? 'justify-center px-0' : 'gap-3 px-3'"
          active-class="active-link"
          title="Pelanggan"
        >
          <svg
            class="w-5 h-5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
            />
          </svg>
          <span v-if="!isSidebarCollapsed" class="truncate">Pelanggan</span>
        </router-link>

        <router-link
          v-if="['super_admin', 'cs', 'admin_cabang'].includes(userRole)"
          to="/admin/sellers"
          @click="isSidebarOpen = false"
          class="flex items-center group nav-link"
          :class="isSidebarCollapsed ? 'justify-center px-0' : 'gap-3 px-3'"
          active-class="active-link"
          title="Sellers"
        >
          <svg
            class="w-5 h-5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
            />
          </svg>
          <span v-if="!isSidebarCollapsed" class="truncate">Sellers</span>
        </router-link>

        <router-link
          v-if="['super_admin'].includes(userRole)"
          to="/admin/brands-categories"
          @click="isSidebarOpen = false"
          class="flex items-center group nav-link"
          :class="isSidebarCollapsed ? 'justify-center px-0' : 'gap-3 px-3'"
          active-class="active-link"
          title="Merek & Kategori"
        >
          <svg
            class="w-5 h-5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
            />
          </svg>
          <span v-if="!isSidebarCollapsed" class="truncate"
            >Merek & Kategori</span
          >
        </router-link>

        <!-- SELLER KHUSUS -->
        <router-link
          v-if="userRole === 'seller'"
          to="/admin/seller-dashboard"
          @click="isSidebarOpen = false"
          class="flex items-center group nav-link"
          :class="isSidebarCollapsed ? 'justify-center px-0' : 'gap-3 px-3'"
          active-class="active-link"
          title="Pengajuan Penjualan"
        >
          <svg
            class="w-5 h-5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <span v-if="!isSidebarCollapsed" class="truncate"
            >Pengajuan Penjualan</span
          >
        </router-link>

        <router-link
          v-if="userRole === 'seller'"
          to="/admin/wishlist"
          @click="isSidebarOpen = false"
          class="flex items-center group nav-link"
          :class="isSidebarCollapsed ? 'justify-center px-0' : 'gap-3 px-3'"
          active-class="active-link"
          title="Wishlist"
        >
          <svg
            class="w-5 h-5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
            />
          </svg>
          <span v-if="!isSidebarCollapsed" class="truncate">Wishlist</span>
        </router-link>

        <!-- KONTEN & SISTEM -->
        <router-link
          v-if="['super_admin', 'cs'].includes(userRole)"
          to="/admin/articles"
          @click="isSidebarOpen = false"
          class="flex items-center group nav-link"
          :class="isSidebarCollapsed ? 'justify-center px-0' : 'gap-3 px-3'"
          active-class="active-link"
          title="Artikel & Blog"
        >
          <svg
            class="w-5 h-5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"
            />
          </svg>
          <span v-if="!isSidebarCollapsed" class="truncate"
            >Artikel & Blog</span
          >
        </router-link>

        <router-link
          v-if="['super_admin', 'cs'].includes(userRole)"
          to="/admin/banners"
          @click="isSidebarOpen = false"
          class="flex items-center group nav-link"
          :class="isSidebarCollapsed ? 'justify-center px-0' : 'gap-3 px-3'"
          active-class="active-link"
          title="Manajemen Banner"
        >
          <svg
            class="w-5 h-5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
          <span v-if="!isSidebarCollapsed" class="truncate"
            >Manajemen Banner</span
          >
        </router-link>

        <router-link
          v-if="userRole === 'super_admin'"
          to="/admin/branches"
          @click="isSidebarOpen = false"
          class="flex items-center group nav-link"
          :class="isSidebarCollapsed ? 'justify-center px-0' : 'gap-3 px-3'"
          active-class="active-link"
          title="Cabang / Lokasi"
        >
          <svg
            class="w-5 h-5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1v1H9V7zm5 0h1v1h-1V7zm-5 4h1v1H9v-1zm5 0h1v1h-1v-1zm-3 4H2v-2h9v2z"
            ></path>
          </svg>
          <span v-if="!isSidebarCollapsed" class="truncate"
            >Cabang / Lokasi</span
          >
        </router-link>

        <router-link
          v-if="userRole === 'super_admin'"
          to="/admin/users"
          @click="isSidebarOpen = false"
          class="flex items-center group nav-link"
          :class="isSidebarCollapsed ? 'justify-center px-0' : 'gap-3 px-3'"
          active-class="active-link"
          title="Manajemen Akun"
        >
          <svg
            class="w-5 h-5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
            />
          </svg>
          <span v-if="!isSidebarCollapsed" class="truncate"
            >Manajemen Akun</span
          >
        </router-link>
        <router-link
          v-if="userRole === 'seller'"
          to="/admin/profile"
          @click="isSidebarOpen = false"
          class="flex items-center nav-link group"
          :class="isSidebarCollapsed ? 'justify-center px-0' : 'gap-3 px-3'"
          active-class="active-link"
          title="Profil Saya"
        >
          <svg
            class="w-5 h-5 shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
            ></path>
          </svg>
          <span v-if="!isSidebarCollapsed" class="truncate">Profil Saya</span>
        </router-link>
      </nav>

      <!-- BAGIAN BAWAH SIDEBAR (User Profile, Filter Mobile & Logout) -->
      <div
        class="flex flex-col gap-3 p-4 border-t border-gray-100 bg-gray-50/50 shrink-0"
      >
        <!-- Filter Cabang KHUSUS MOBILE (Hanya muncul di HP) -->
        <div v-if="userRole === 'super_admin'" class="relative lg:hidden">
          <label
            class="block mb-1 text-[10px] font-bold tracking-wider text-gray-500 uppercase"
            >Filter Cabang</label
          >
          <select
            v-model="selectedBranch"
            @change="updateGlobalBranch"
            class="block w-full py-2 pl-3 pr-10 text-sm bg-white border-gray-300 rounded-md shadow-sm cursor-pointer focus:border-blue-500 focus:outline-none focus:ring-blue-500"
          >
            <option value="">Semua Cabang</option>
            <option
              v-for="branch in branches"
              :key="branch.id"
              :value="branch.id"
            >
              {{ branch.name }}
            </option>
          </select>
        </div>

        <!-- Profil & Tombol Logout -->
        <div
          class="flex items-center"
          :class="
            isSidebarCollapsed
              ? 'justify-center flex-col gap-4'
              : 'justify-between'
          "
        >
          <!-- Avatar & Info -->
          <div
            class="flex items-center gap-3"
            :class="{ 'justify-center': isSidebarCollapsed }"
          >
            <div
              class="flex items-center justify-center font-bold text-blue-700 bg-blue-100 rounded-full w-9 h-9 shrink-0"
            >
              {{ user.username ? user.username.charAt(0).toUpperCase() : "U" }}
            </div>
            <div
              v-if="!isSidebarCollapsed"
              class="flex flex-col overflow-hidden"
            >
              <span
                class="text-sm font-bold leading-tight text-gray-900 truncate"
                >{{ user.username }}</span
              >
              <span
                class="mt-0.5 text-xs font-medium text-gray-500 capitalize truncate"
                >{{ user.role.replace("_", " ") }}</span
              >
            </div>
          </div>

          <!-- Tombol Logout (Icon only) -->
          <button
            @click="handleLogout"
            class="p-2 text-red-500 transition-colors rounded-lg hover:bg-red-100 hover:text-red-700"
            :class="{ 'shrink-0': !isSidebarCollapsed }"
            title="Keluar / Logout"
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
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
              ></path>
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- MAIN CONTENT -->
    <div class="flex flex-col flex-1 min-w-0 overflow-hidden">
      <!-- NAVBAR -->
      <header
        class="z-10 flex items-center justify-between h-16 px-4 bg-white border-b border-gray-200 shadow-sm lg:px-8 shrink-0"
      >
        <div class="flex items-center gap-3">
          <button
            @click="isSidebarOpen = true"
            class="p-1 text-gray-600 rounded-md lg:hidden hover:text-gray-900 hover:bg-gray-100"
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
                d="M4 6h16M4 12h16M4 18h16"
              ></path>
            </svg>
          </button>
          <h2
            class="text-lg font-semibold text-gray-800 truncate max-w-[200px] sm:max-w-none"
          >
            {{ currentRouteName }}
          </h2>
        </div>

        <!-- Bagian Kanan Navbar (HANYA Filter Cabang Desktop) -->
        <div class="flex items-center gap-3 lg:gap-4">
          <div
            v-if="userRole === 'super_admin'"
            class="relative hidden lg:block"
          >
            <select
              v-model="selectedBranch"
              @change="updateGlobalBranch"
              class="block w-full py-2 pl-3 pr-10 text-sm bg-white border-gray-300 rounded-md shadow-sm cursor-pointer focus:border-blue-500 focus:outline-none focus:ring-blue-500"
            >
              <option value="">Semua Cabang</option>
              <option
                v-for="branch in branches"
                :key="branch.id"
                :value="branch.id"
              >
                {{ branch.name }}
              </option>
            </select>
          </div>
        </div>
      </header>

      <!-- PAGE CONTENT -->
      <main class="flex-1 p-4 overflow-y-auto sm:p-6 bg-gray-50">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component
              :is="Component"
              :key="route.fullPath + globalBranchTrigger"
            />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import api from "../services/api";

const router = useRouter();
const route = useRoute();
const isSidebarOpen = ref(false);
const isSidebarCollapsed = ref(false);

const user = ref({ username: "", role: "" });
const userRole = computed(() => user.value.role);
const currentRouteName = computed(() => route.name || "Dashboard");

// STATE FILTER CABANG
const branches = ref([]);
const selectedBranch = ref("");
const globalBranchTrigger = ref(0); // Digunakan untuk me-refresh komponen saat cabang berubah

onMounted(async () => {
  const userData = JSON.parse(localStorage.getItem("user_data") || "{}");
  if (userData.username) {
    user.value = userData;
    // Jika super admin, ambil daftar cabang untuk dropdown
    if (userData.role === "super_admin") {
      await fetchBranches();
      // Cek jika sebelumnya ada cabang yang dipilih di localStorage
      const savedBranch = localStorage.getItem("selected_branch_id");
      if (savedBranch) selectedBranch.value = savedBranch;
    }
  } else {
    router.push({ name: "Login" });
  }
});

const fetchBranches = async () => {
  try {
    const response = await api.get("/master/branches");
    branches.value = response.data.data;
  } catch (error) {
    console.error("Gagal mengambil daftar cabang", error);
  }
};

const updateGlobalBranch = () => {
  // Simpan pilihan cabang ke local storage agar halaman lain bisa membaca
  localStorage.setItem("selected_branch_id", selectedBranch.value);

  // Picu event kustom agar komponen halaman (seperti Inventory.vue) tahu ada perubahan cabang
  window.dispatchEvent(
    new CustomEvent("branchChanged", { detail: selectedBranch.value }),
  );

  // Ubah trigger agar router-view merender ulang komponen
  globalBranchTrigger.value += 1;
};

const handleLogout = () => {
  if (confirm("Apakah Anda yakin ingin keluar?")) {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_data");
    localStorage.removeItem("selected_branch_id"); // Bersihkan filter cabang
    router.push({ name: "Login" });
  }
};
</script>

<style scoped>
.nav-link {
  @apply flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-colors text-gray-700 hover:bg-gray-100;
}
.active-link {
  @apply bg-blue-50 text-blue-700 hover:bg-blue-50;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
