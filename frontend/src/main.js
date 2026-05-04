import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router'; // Import router yang baru dibuat
import './style.css'; // Import Tailwind CSS
import { OhVueIcon, addIcons } from "oh-vue-icons";
import { FaFlag, RiZhihuFill } from "oh-vue-icons/icons";

addIcons(FaFlag, RiZhihuFill);

const app = createApp(App);

app.use(createPinia());
app.use(router); // Gunakan router
app.component("v-icon", OhVueIcon);
app.mount('#app');