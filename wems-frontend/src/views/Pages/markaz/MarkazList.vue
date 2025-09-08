<template>
  <div class="font-[SolaimanLipi] min-h-screen bg-gray-50 dark:bg-slate-950 transition-colors duration-300">
    <!-- Header + Controls -->
    <MarkazHeader
      :examName="examName"
      :searchQuery="searchQuery"
      @update:searchQuery="val => (searchQuery = val)"
      @refresh="handleRefresh"
      @create="onCreate"
    />

    <div class="mx-auto px-6 lg:px-8 py-8 space-y-8">
      <StatsCards :stats="stats" />

      <div class="bg-white rounded-md shadow-md border overflow-hidden dark:bg-slate-900">
        <!-- Loading / Empty / Table states managed inside table component -->
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
      <AgreementDetailsPanel
        v-if="selectedAgreement"
        :agreement="selectedAgreement"
        @close="selectedAgreement = null"
      />

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
import MarkazHeader from '@/views/Pages/markaz/components/MarkazHeader.vue';
import StatsCards from '@/views/Pages/markaz/components/StatsCards.vue';
import AgreementTable from '@/views/Pages/markaz/components/AgreementTable.vue';
import AgreementDetailsPanel from '@/views/Pages/markaz/components/AgreementDetailsPanel.vue';
import ConfirmDialog from '@/views/Pages/markaz/components/ConfirmDialog.vue';
import Toast from 'primevue/toast';

// Composable
import { useAgreements, type Agreement } from '@/views/Pages/markaz/composable/useAgreements';

// Initialize composable
const {
  agreements,
  loading,
  stats,
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
  // Navigate to edit page using router
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

    // Close details panel if the deleted item was selected
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

    // Update selected agreement if it's the one being submitted
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

// Initialize data on mount
onMounted(async () => {
  await fetchAgreements();
});
</script>

<style scoped>
/* Parent level styles kept minimal - children control their own layout */
</style>
