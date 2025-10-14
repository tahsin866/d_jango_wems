
import './assets/main.css'
// Import Swiper styles
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'
import 'jsvectormap/dist/jsvectormap.css'
import 'flatpickr/dist/flatpickr.css'

import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import ToastService from 'primevue/toastservice';
import Button from 'primevue/button';
import SplitButton from 'primevue/splitbutton';
import Dialog from 'primevue/dialog';
import Toast from 'primevue/toast';

import Badge from 'primevue/badge';
import Card from 'primevue/card';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import InputText from 'primevue/inputtext';
import Tooltip from 'primevue/tooltip';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import VueApexCharts from 'vue3-apexcharts';
import { useSidebarPreloader } from '@/composables/useSidebarPreloader';




// Set correct session_token for authentication (for debugging)
localStorage.setItem('token', '66de19b4b676e1b3cb1786c2fbe40399d9ba60d2fb727711c60af1035265f9b1')

const app = createApp(App);

// Preload sidebar data immediately
const { preloadSidebarData } = useSidebarPreloader();
preloadSidebarData();

app.use(router);
app.use(VueApexCharts);
app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});
app.use(ToastService);

// Register PrimeVue components globally
app.component('PrimeButton', Button);
app.component('SplitButton', SplitButton);
app.component('PrimeDialog', Dialog);
app.component('PrimeToast', Toast);
app.directive('tooltip', Tooltip);
app.component('PrimeBadge', Badge);
app.component('PrimeCard', Card);
app.component('PrimeColumn', Column);
app.component('DataTable', DataTable);
app.component('InputText', InputText);

app.mount('#app');
