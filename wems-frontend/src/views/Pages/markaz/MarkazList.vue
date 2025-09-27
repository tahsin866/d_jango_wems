<template>
  <div class="font-[SolaimanLipi] min-h-screen bg-gray-100 transition-colors duration-300">
    <!-- AdminLTE Classic Header -->
    <div class="bg-gray-800 border-b border-gray-900 shadow-lg py-6 px-8 flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-extrabold text-white tracking-tight flex items-center">
          <i class="fas fa-university mr-3 text-indigo-300"></i>
          {{ examName }}
        </h1>
        <p class="text-gray-200 mt-2 font-medium text-base">Markaz Management Dashboard</p>
      </div>
      <div class="flex items-center gap-2">
        <input
          v-model="searchQuery"
          class="px-4 py-2 rounded border border-gray-600 bg-gray-900 text-white text-base focus:border-indigo-400 focus:ring focus:ring-indigo-500 focus:ring-opacity-50"
          :placeholder="`${examName} - খুঁজুন`"
        />
        <button
          @click="handleRefresh"
          class="inline-flex items-center px-4 py-2 bg-indigo-600 border border-indigo-700 rounded font-bold text-white shadow hover:bg-indigo-700 transition"
        >
          <i class="fas fa-sync mr-2"></i>
          রিফ্রেশ
        </button>
        <button
          @click="onCreate"
          class="inline-flex items-center px-4 py-2 bg-green-600 border border-green-700 rounded font-bold text-white shadow hover:bg-green-700 transition"
        >
          <i class="fas fa-plus mr-2"></i>
          আবেদন করুন
        </button>
      </div>
    </div>

    <div class="mx-auto px-8 py-10 space-y-10 ">
      <!-- Stats Cards - Classic Info Box -->
  <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-7">
    <div
      v-for="(stat, idx) in stats"
      :key="idx"
      class="bg-white border border-gray-300 rounded-lg shadow-sm p-0 transition hover:shadow-md"
      style="min-width:220px;"
    >
      <!-- Card Header -->
      <div class="flex items-center justify-between px-5 py-3 bg-gray-50 border-b border-gray-200 rounded-t">
        <div class="flex items-center">
          <i :class="`fas fa-${stat.icon} mr-2 text-gray-500`"></i>
          <span class="font-semibold text-base text-gray-800">{{ stat.title }}</span>
        </div>
      </div>
      <!-- Card Body -->
      <div class="px-5 py-7 text-center">
        <span class="text-2xl font-bold text-gray-900">{{ stat.value }}</span>
        <span
          class="ml-2 px-2 py-1 text-xs rounded font-bold inline-flex items-center border"
          :class="stat.trendUp ? 'bg-gray-100 text-gray-700 border-gray-200' : 'bg-gray-100 text-gray-700 border-gray-200'"
        >
          <i
            :class="stat.trendUp ? 'fas fa-arrow-up mr-1 text-gray-500' : 'fas fa-arrow-down mr-1 text-gray-500'"
          ></i>
          {{ stat.change }}
        </span>
        <div class="mt-4">
          <div class="h-5 rounded bg-gray-100 border border-gray-300 shadow-inner flex items-center w-full">
            <div
              class="h-5 rounded-l transition-all duration-500 flex items-center bg-gray-300"
              :style="{ width: Math.round((stat.trend[stat.trend.length - 1] / Math.max(...stat.trend)) * 100) + '%' }"
            >
              <span
                class="pr-2 text-gray-900 font-bold text-xs"
                v-if="((stat.trend[stat.trend.length - 1] / Math.max(...stat.trend)) * 100) > 15"
              >
                {{ Math.round((stat.trend[stat.trend.length - 1] / Math.max(...stat.trend)) * 100) }}%
              </span>
            </div>
          </div>
          <div class="flex justify-between mt-1 text-xs text-gray-500">
            <span>Min: {{ Math.min(...stat.trend) }}</span>
            <span>Max: {{ Math.max(...stat.trend) }}</span>
          </div>
        </div>
      </div>
      <!-- Card Footer -->
      <div class="bg-gray-50 border-t border-gray-200 rounded-b px-5 py-2 flex items-center justify-between">
        <span class="text-xs text-gray-600 flex items-center">
          <i :class="`fas fa-${stat.icon} mr-1 text-gray-400`"></i>
          {{ stat.title }}
        </span>
        <span class="text-xs text-gray-500">Info</span>
      </div>
    </div>
  </div>

      <!-- Table Box -->
      <div class="bg-white rounded shadow-lg border border-gray-300 overflow-hidden">
        <AgreementTable
          :loading="loading"
          :agreements="agreements"
          :filtered="filteredAgreements"
          @view="onView"
          @edit="onEdit"
          @delete="onRequestDelete"
          @submit="onRequestSubmit"
        />
      </div>

      <!-- Details panel below the table (inline, not modal) -->
      <div v-if="selectedAgreement" class="bg-white border border-gray-300 rounded shadow-lg p-6">
        <AgreementDetailsPanel
          :agreement="selectedAgreement"
          @close="selectedAgreement = null"
        />
      </div>

      <!-- Confirm dialogs -->
      <ConfirmDialog
        v-model:visible="showDeleteModal"
        title="আবেদন মুছে ফেলুন"
        description="আপনি কি নিশ্চিত যে এই আবেদনটি স্থায়ীভাবে মুছে ফেলতে চান? এই কাজটি অপরিবর্তনীয়!"
        confirmLabel="মুছে ফেলুন"
        cancelLabel="বাতিল করুন"
        @confirm="confirmDelete"
      />

      <ConfirmDialog
        v-model:visible="showSubmitModal"
        title="বোর্ডে দাখিল করুন"
        description="আপনি কি নিশ্চিত যে এই আবেদনটি চূড়ান্তভাবে বোর্ডে দাখিল করতে চান? দাখিলের পর পরিবর্তন করা যাবে না।"
        confirmLabel="দাখিল করুন"
        cancelLabel="বাতিল করুন"
        @confirm="confirmSubmit"
      />

      <Toast position="top-right" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';

// Components
import AgreementTable from '@/views/Pages/markaz/components/AgreementTable.vue';
import AgreementDetailsPanel from '@/views/Pages/markaz/components/AgreementDetailsPanel.vue';
import ConfirmDialog from '@/views/Pages/markaz/components/ConfirmDialog.vue';
import Toast from 'primevue/toast';

// Composable
import { useAgreements, type Agreement } from '@/views/Pages/markaz/composable/useAgreements';

// Stats dummy for classic cards (replace with actual if needed)
const stats = ref([
  {
    title: 'মোট আবেদন',
    value: '১৫৯',
    change: '+৫%',
    icon: 'file-alt',
    color: 'indigo',
    trend: [120, 122, 130, 140, 145, 150, 159],
    trendUp: true
  },
  {
    title: 'পেন্ডিং',
    value: '৫২',
    change: '-৩%',
    icon: 'hourglass-half',
    color: 'blue',
    trend: [60, 58, 55, 54, 53, 52, 52],
    trendUp: false
  },
  {
    title: 'দাখিল',
    value: '১০৭',
    change: '+৮%',
    icon: 'check-circle',
    color: 'green',
    trend: [80, 88, 90, 95, 100, 105, 107],
    trendUp: true
  },
  {
    title: 'বাতিল',
    value: '০',
    change: '০%',
    icon: 'times-circle',
    color: 'red',
    trend: [0,0,0,0,0,0,0],
    trendUp: false
  }
]);

// Initialize composable
const {
  agreements,
  loading,
  fetchAgreements,
  deleteAgreementById,
  submitAgreementById,
  examName
} = useAgreements();

// ID source (change as needed)
// import { useRoute } from 'vue-router';
// const route = useRoute();
// const userId = Number(route.params.id) || 22; // Default/fallback

// Router and toast
const router = useRouter();
const toast = useToast();

// Local reactive state
const searchQuery = ref('');
const selectedAgreement = ref<Agreement | null>(null);
const showDeleteModal = ref(false);
const showSubmitModal = ref(false);
const pendingDeleteId = ref<number | null>(null);
const pendingSubmitId = ref<number | null>(null);

// Computed properties
const filteredAgreements = computed(() => {
  if (!searchQuery.value.trim()) return agreements.value;

  const query = searchQuery.value.toLowerCase().trim();
  return agreements.value.filter(agreement =>
    agreement.main_madrasa.toLowerCase().includes(query) ||
    agreement.exam_name.toLowerCase().includes(query) ||
    agreement.markaz_type.toLowerCase().includes(query) ||
    agreement.status.toLowerCase().includes(query)
  );
});

// Event handlers
async function handleRefresh() {
  try {
  await fetchAgreements();
    toast.add({
      severity: 'success',
      summary: 'রিফ্রেশ সম্পন্ন',
      detail: 'ডেটা সফলভাবে আপডেট হয়েছে',
      life: 3000
    });
  } catch {
    toast.add({
      severity: 'error',
      summary: 'ত্রুটি',
      detail: 'ডেটা লোড করতে সমস্যা হয়েছে',
      life: 3000
    });
  }
}

function onView(agreement: Agreement) {
  selectedAgreement.value = agreement;
}

function onEdit(agreement: Agreement) {
  router.push({
    name: 'MarkazEdit',
    params: { id: agreement.id.toString() }
  });
}

function onRequestDelete(agreement: Agreement) {
  pendingDeleteId.value = agreement.id;
  showDeleteModal.value = true;
}

function confirmDelete() {
  if (!pendingDeleteId.value) return;

  const success = deleteAgreementById(pendingDeleteId.value);

  if (success) {
    toast.add({
      severity: 'success',
      summary: 'মুছে ফেলা হয়েছে',
      detail: 'আবেদন সফলভাবে মুছে ফেলা হয়েছে',
      life: 3000
    });

    if (selectedAgreement.value?.id === pendingDeleteId.value) {
      selectedAgreement.value = null;
    }
  } else {
    toast.add({
      severity: 'error',
      summary: 'ত্রুটি',
      detail: 'আবেদন মুছতে সমস্যা হয়েছে',
      life: 3000
    });
  }

  showDeleteModal.value = false;
  pendingDeleteId.value = null;
}

function onRequestSubmit(agreement: Agreement) {
  pendingSubmitId.value = agreement.id;
  showSubmitModal.value = true;
}

function confirmSubmit() {
  if (!pendingSubmitId.value) return;

  const success = submitAgreementById(pendingSubmitId.value);

  if (success) {
    toast.add({
      severity: 'info',
      summary: 'দাখিল সম্পন্ন',
      detail: 'আবেদন বোর্ডে সফলভাবে দাখিল হয়েছে!',
      life: 3000
    });

    if (selectedAgreement.value?.id === pendingSubmitId.value) {
      selectedAgreement.value.status = 'submitted';
    }
  } else {
    toast.add({
      severity: 'error',
      summary: 'ত্রুটি',
      detail: 'আবেদন দাখিল করতে সমস্যা হয়েছে',
      life: 3000
    });
  }

  showSubmitModal.value = false;
  pendingSubmitId.value = null;
}

function onCreate() {
  router.push({ name: 'MarkazApply' });
}

onMounted(async () => {
  await fetchAgreements();
});
</script>

<style scoped>
/* AdminLTE flavor, minimal parent styles */
</style>
