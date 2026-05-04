import { createRouter, createWebHistory } from "vue-router";

// Halaman Publik
import Home from "../views/public/Home.vue";
import Katalog from "../views/public/Katalog.vue";
import Kontak from "../views/public/Kontak.vue";
import Blog from "../views/public/Blog.vue";
import ArticleDetail from "../views/public/ArticleDetail.vue";

// Auth & Admin
import Login from "../views/admin/Login.vue";
import DashboardLayout from "../components/AdminLayout.vue";
import Dashboard from "../views/admin/Dashboard.vue";
import Inventory from "../views/admin/Inventory.vue";
import Sales from "../views/admin/Sales.vue";
import Finance from "../views/admin/Finance.vue";
import Customers from "../views/admin/Customers.vue";
import Affiliates from "../views/admin/Affiliates.vue";
import Users from "../views/admin/Users.vue";
import MotorcycleDetail from "../views/public/MotorcycleDetail.vue";
import ExternalValidations from "../views/admin/ExternalValidations.vue";
import SellerDashboard from "../views/admin/SellerDashboard.vue";
import SellersView from "../views/admin/Sellers.vue";
import ArticlesView from "../views/admin/Articles.vue";
import Banners from "../views/admin/Banners.vue";
import Register from "../views/admin/Register.vue";
import Wishlist from "../views/admin/Wishlist.vue";
import SellerProfile from "../views/admin/SellerProfile.vue";

const routes = [
  // --- ROUTES PUBLIK ---
  { path: "/", name: "Home", component: Home },
  { path: "/katalog", name: "Katalog", component: Katalog },
  { path: "/kontak", name: "Kontak", component: Kontak },
  { path: "/login", name: "Login", component: Login },
  { path: "/register", name: "Register", component: Register },
  { path: "/motor/:id", name: "MotorDetail", component: MotorcycleDetail },
  { path: "/blog", name: "Blog", component: Blog },
  { path: "/blog/:slug", name: "ArticleDetail", component: ArticleDetail },

  // (Catatan: Rute publik untuk dashboard seller/validasi dihapus
  // karena sudah ada di dalam children /admin yang dilindungi)

  // --- ROUTES ADMIN (DILINDUNGI) ---
  {
    path: "/admin",
    component: DashboardLayout,
    meta: { requiresAuth: true }, // Semua yang di dalam /admin butuh login
    children: [
      {
        path: "dashboard",
        name: "Dashboard",
        component: Dashboard,
        meta: { roles: ["super_admin", "admin_cabang"] },
      },
      {
        path: "inventory",
        name: "Inventory",
        component: Inventory,
        meta: { roles: ["super_admin", "finance", "cs", "admin_cabang"] },
      },
      {
        path: "finance",
        name: "Finance",
        component: Finance,
        meta: { roles: ["super_admin", "finance", "admin_cabang"] },
      },
      {
        path: "sales",
        name: "Sales",
        component: Sales,
        meta: { roles: ["super_admin", "finance", "cs", "admin_cabang"] },
      },
      {
        path: "customers",
        name: "Pelanggan",
        component: Customers,
        meta: { roles: ["super_admin", "finance", "cs", "admin_cabang"] },
      },
      {
        path: "affiliates",
        name: "Mitra / Affiliates",
        component: Affiliates,
        meta: { roles: ["super_admin", "finance"] },
      },
      {
        path: "users",
        name: "Pengguna",
        component: Users,
        meta: { roles: ["super_admin"] },
      },
      {
        path: "validasi-eksternal",
        name: "Validasi Pengajuan",
        component: ExternalValidations,
        meta: { roles: ["super_admin", "admin_cabang"] },
      },
      {
        path: "seller-dashboard",
        name: "Seller Dashboard",
        component: SellerDashboard,
        meta: { roles: ["seller"] },
      },
      {
        path: "wishlist",
        name: "Wishlist",
        component: Wishlist,
        meta: { roles: ["seller"] },
      },
      {
        path: "sellers",
        name: "Sellers",
        component: SellersView,
        // PERBAIKAN TYPO: "role" diubah menjadi "roles" agar terbaca oleh Guard
        meta: { roles: ["super_admin", "cs", "finance", "admin_cabang"] },
      },
      {
        path: "articles",
        name: "Articles dan Blog",
        component: ArticlesView,
        meta: { roles: ["super_admin", "cs"] },
      },
      {
        path: "banners",
        name: "Manajemen Banner",
        component: Banners,
        meta: { roles: ["super_admin", "cs"] },
      },
      {
        path: "brands-categories",
        name: "BrandsCategories",
        component: () => import("../views/admin/BrandsCategories.vue"),
        meta: { roles: ["super_admin", "cs"] },
      },
      {
        path: "branches",
        name: "Manajemen Cabang",
        component: () => import("../views/admin/Branches.vue"),
        meta: { requiresAuth: true, role: "super_admin" }, // Pastikan hanya super_admin yang bisa akses
      },
      {
        path: "profile",
        name: "SellerProfile",
        component: SellerProfile,
        meta: { requiresAuth: true },
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ==========================================
// NAVIGATION GUARD (Satpam Pintu Masuk)
// ==========================================

// Fungsi bantuan untuk mengarahkan user ke halaman utamanya sesuai role
const redirectByRole = (role) => {
  if (role === "super_admin" || role === "cs") {
    return { name: "Inventory" };
  } else if (role === "finance") {
    return { name: "Finance" };
  } else if (role === "seller") {
    return { name: "Seller Dashboard" };
  } else {
    return { name: "Home" }; // Fallback jika role tidak dikenali
  }
};

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token");
  let userData = null;

  try {
    userData = JSON.parse(localStorage.getItem("user_data"));
  } catch (e) {}

  // 1. Cek apakah halaman butuh login?
  if (
    to.meta.requiresAuth ||
    to.matched.some((record) => record.meta.requiresAuth)
  ) {
    if (!token || !userData) {
      // Jika belum login, tendang ke halaman login
      return next({ name: "Login" });
    }

    // 2. Jika sudah login, cek apakah dia punya Role yang diizinkan untuk rute ini?
    const routeRoles =
      to.meta.roles ||
      to.matched.find((record) => record.meta.roles)?.meta.roles;

    if (routeRoles && !routeRoles.includes(userData.role)) {
      // Jika rolenya tidak ada di daftar yang diizinkan, kembalikan ke basecamp masing-masing
      alert(
        "Akses Ditolak! Anda tidak memiliki izin untuk membuka halaman ini.",
      );
      return next(redirectByRole(userData.role));
    }
  }

  // 3. Jika mencoba ke halaman Login tapi sudah login, arahkan sesuai role
  if (to.name === "Login" && token && userData) {
    return next(redirectByRole(userData.role));
  }

  // Izinkan masuk
  next();
});

export default router;
