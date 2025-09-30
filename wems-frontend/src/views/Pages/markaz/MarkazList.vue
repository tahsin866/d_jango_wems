<template>
  <div class="font-[SolaimanLipi]  bg-gray-100">
    <!-- Classic AdminLTE Header -->
    <div class="bg-gray-900 border-b border-gray-800 shadow py-5 px-8 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-white flex items-center">
          <i class="fas fa-university mr-3 text-gray-300"></i>
          {{ examName }}
        </h1>
        <p class="text-gray-400 mt-1 text-sm">Markaz Management Dashboard</p>
      </div>
      <div class="flex items-center gap-3">
        <input
          v-model="searchQuery"
          class="px-4 py-2 rounded border border-gray-700 bg-gray-800 text-gray-200 text-sm focus:border-gray-600 focus:ring focus:ring-gray-700 focus:ring-opacity-50"
          :placeholder="`${examName} - খুঁজুন`"
        />
        <button
          @click="handleRefresh"
          class="inline-flex items-center px-4 py-2 bg-gray-700 border border-gray-600 rounded font-medium text-gray-200 hover:bg-gray-600 transition"
        >
          <i class="fas fa-sync mr-2"></i>
          রিফ্রেশ
        </button>
        <button
          @click="onCreate"
          class="inline-flex items-center px-4 py-2 bg-gray-800 border border-gray-700 rounded font-medium text-white hover:bg-gray-700 transition"
        >
          <i class="fas fa-plus mr-2"></i>
          আবেদন করুন
        </button>
      </div>
    </div>

      <!-- Classic Stats Cards -->


      <!-- Table Box -->
      <div class="bg-white rounded shadow border border-gray-300 overflow-hidden">
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
      <div v-if="selectedAgreement" class="bg-white border border-gray-300 rounded shadow p-6">
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
// const stats = ref([
//   {
//     title: 'মোট আবেদন',
//     value: '১৫৯',
//     change: '+৫%',
//     icon: 'file-alt',
//     color: 'gray',
//     trend: [120, 122, 130, 140, 145, 150, 159],
//     trendUp: true
//   },
//   {
//     title: 'পেন্ডিং',
//     value: '৫২',
//     change: '-৩%',
//     icon: 'hourglass-half',
//     color: 'gray',
//     trend: [60, 58, 55, 54, 53, 52, 52],
//     trendUp: false
//   },
//   {
//     title: 'দাখিল',
//     value: '১০৭',
//     change: '+৮%',
//     icon: 'check-circle',
//     color: 'gray',
//     trend: [80, 88, 90, 95, 100, 105, 107],
//     trendUp: true
//   },
//   {
//     title: 'বাতিল',
//     value: '০',
//     change: '০%',
//     icon: 'times-circle',
//     color: 'gray',
//     trend: [0,0,0,0,0,0,0],
//     trendUp: false
//   }
// ]);

// Initialize composable
const {
  agreements,
  loading,
  fetchAgreements,
  deleteAgreementById,
  submitAgreementById,
  examName
} = useAgreements();

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
/* Classic AdminLTE styling */
</style>
