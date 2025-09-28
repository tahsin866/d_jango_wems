<template>
  <div>
    <!-- Table Header -->
    <div class="flex flex-col md:flex-row justify-between gap-4 mb-4 items-center border-b border-gray-200 bg-gray-50 rounded-t-sm px-4 py-3">
      <!-- Search -->
      <div class="flex-1">
        <div class="relative">
          <span class="p-input-icon-left w-full">
            <InputText
              v-model="filters['global'].value"
              :placeholder="`${tableTitle} থেকে ফোন নম্বর দিয়ে সার্চ করুন`"
              class="w-full border border-gray-300 rounded-sm px-3 py-2 focus:border-gray-400 focus:ring-gray-300 focus:ring-1 shadow-sm"
            />
            <i class="fas fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
          </span>
        </div>
      </div>
      <!-- Create User Button -->
      <div>
        <RouterLink
          :to="createUserRoute"
          class="inline-flex items-center px-4 py-2 bg-gray-800 border border-gray-700 rounded-sm font-semibold text-xs text-white uppercase tracking-wider hover:bg-gray-700 shadow-sm transition"
        >
          <i class="fas fa-user-plus mr-2"></i>
          নতুন ইউজার
        </RouterLink>
      </div>
    </div>
    <!-- Table -->
    <div class="bg-white border border-gray-200 shadow-sm rounded-b-sm px-2 pb-4">
      <DataTable
        :value="admins"
        :paginator="true"
        :rows="20"
        :rowsPerPageOptions="[5, 10, 20, 50]"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        currentPageReportTemplate="মোট {totalRecords} জন ইউজারের মধ্যে {first}-{last} দেখাচ্ছে"
        responsiveLayout="scroll"
        :globalFilterFields="['name', 'phone', 'email']"
        v-model:filters="filters"
        filterDisplay="menu"
        class="p-datatable-sm"
      >
        <Column field="profile_image" header="ছবি">
          <template #body="slotProps">
            <div class="h-10 w-10 rounded-sm overflow-hidden border border-gray-200 bg-gray-100">
              <img
                :src="slotProps.data.profile_image ? slotProps.data.profile_image : 'https://randomuser.me/api/portraits/men/1.jpg'"
                :alt="slotProps.data.name"
                class="h-full w-full object-cover"
              />
            </div>
          </template>
        </Column>
        <Column field="name" header="নাম" :sortable="true" :filter="true" filterPlaceholder="নাম খুঁজুন"/>
        <Column field="phone" header="ফোন নম্বর" :sortable="true" :filter="true" filterPlaceholder="ফোন নম্বর খুঁজুন"/>
        <Column field="email" header="ইমেইল" :sortable="true" :filter="true" filterPlaceholder="ইমেইল খুঁজুন"/>
        <Column field="designation" header="পদবি" :sortable="true" :filter="true" filterMatchMode="equals">
          <template #body="slotProps">
            <span class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-sm border border-gray-300 bg-gray-100 text-gray-800">
              <i class="fas fa-user-tag mr-1 text-gray-600"></i>
              {{ getDesignationText(slotProps.data.designation) }}
            </span>
          </template>
          <template #filter="{ filterModel }">
            <Dropdown
              v-model="filterModel.value"
              :options="designationOptions"
              optionLabel="name"
              optionValue="value"
              placeholder="পদবি বাছাই করুন"
              class="p-column-filter"
              showClear
            />
          </template>
        </Column>
        <Column header="একশন">
          <template #body="slotProps">
            <div class="flex space-x-2">
              <Toast />
              <Dialog v-model:visible="showModal" :style="{width: '450px'}" header="এডমিন ডিলিট করুন" :modal="true">
                <div class="flex items-start">
                  <i class="fas fa-exclamation-triangle mr-3 text-gray-600" style="font-size: 2rem"></i>
                  <div>
                    <p class="text-sm text-gray-600">
                      আপনি কি নিশ্চিত যে আপনি এই এডমিন ডিলিট করতে চান? এই কাজটি অপরিবর্তনীয়।
                    </p>
                  </div>
                </div>
                <template #footer>
                  <Button label="বাতিল করুন" icon="pi pi-times" class="p-button-text p-button-secondary" @click="showModal = false" />
                  <Button label="ডিলিট করুন" icon="pi pi-check" class="p-button-danger" @click="deleteAdmin" />
                </template>
              </Dialog>
              <SplitButton
                label="সংশোধন"
                @click="editUser(slotProps.data.id)"
                :model="getActionItems(slotProps.data.id)"
                class="p-button-sm p-button-outlined text-gray-700 font-semibold border-gray-300"
              />
            </div>
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import Toast from 'primevue/toast';
import SplitButton from 'primevue/splitbutton';
import { useToast } from "primevue/usetoast";

interface Admin {
  id: number;
  name: string;
  phone: string;
  email: string;
  designation: number;
  profile_image?: string;
}

defineProps<{
  admins: Admin[],
  designationOptions: { name: string, value: number }[],
  tableTitle: string,
  createUserRoute: string
}>();

const FilterMatchMode = {
  STARTS_WITH: 'startswith',
  CONTAINS: 'contains',
  EQUALS: 'equals',
  DATE_IS: 'dateIs'
};

const filters = ref({
  'global': { value: null, matchMode: FilterMatchMode.CONTAINS },
  'name': { value: null, matchMode: FilterMatchMode.STARTS_WITH },
  'phone': { value: null, matchMode: FilterMatchMode.CONTAINS },
  'email': { value: null, matchMode: FilterMatchMode.CONTAINS },
  'designation': { value: null, matchMode: FilterMatchMode.EQUALS }
});

const toast = useToast();
const showModal = ref(false);
const adminIdToDelete = ref<number|null>(null);

const editUser = (userId: number) => {
  toast.add({ severity: 'info', summary: 'Edit', detail: `Editing user ${userId}`, life: 3000 });
};
const viewUser = (userId: number) => {
  toast.add({ severity: 'info', summary: 'View', detail: `Viewing user ${userId}`, life: 3000 });
};
const confirmDelete = (userId: number) => {
  adminIdToDelete.value = userId;
  showModal.value = true;
};
const deleteAdmin = () => {
  toast.add({
    severity: 'success',
    summary: 'সফল',
    detail: 'এডমিন সফলভাবে ডিলিট করা হয়েছে',
    life: 3000
  });
  showModal.value = false;
};
const checkHistory = (userId: number) => {
  toast.add({ severity: 'info', summary: 'History', detail: `Checking history for user ${userId}`, life: 3000 });
};
const getActionItems = (userId: number) => {
  return [
    {
      label: 'ভিউ',
      icon: 'pi pi-eye',
      command: () => viewUser(userId)
    },
    {
      label: 'ডিলিট',
      icon: 'pi pi-trash',
      command: () => confirmDelete(userId)
    },
    {
      label: 'চেক হিস্টরি',
      icon: 'pi pi-history',
      command: () => checkHistory(userId)
    }
  ];
};

const getDesignationText = (designation: number) => {
  switch (designation) {
    case 1: return 'সুপার এডমিন';
    case 2: return 'সহ সুপার এডমিন';
    case 3: return 'বোর্ড এডমিন';
    case 4: return 'নেগরান';
    case 5: return 'মুমতাহিন';
    case 6: return 'যোন';
    default: return 'অন্যান্য';
  }
};

const getDesignationClass = (designation: number) => {
  // All designations now use the same gray styling for a professional look
  return 'bg-gray-100 text-gray-800';
};
</script>

<style scoped>
/* Professional styling enhancements */
.transition-all {
  transition: all 0.2s ease;
}

.shadow-sm {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.rounded-sm {
  border-radius: 0.125rem;
}

/* Custom focus styles for accessibility */
input:focus, select:focus, button:focus {
  outline: none;
}

/* Hover effect for buttons */
button:hover {
  transition: background-color 0.2s ease, border-color 0.2s ease;
}

/* PrimeVue component overrides */
:deep(.p-datatable .p-datatable-header) {
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

:deep(.p-datatable .p-datatable-thead > tr > th) {
  background-color: #f9fafb;
  color: #374151;
  font-weight: 600;
}

:deep(.p-datatable .p-datatable-tbody > tr) {
  transition: background-color 0.2s ease;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
  background-color: #f9fafb;
}

:deep(.p-paginator) {
  background-color: #fff;
  border-top: 1px solid #e5e7eb;
}

:deep(.p-dropdown) {
  border: 1px solid #d1d5db;
  border-radius: 0.125rem;
}

:deep(.p-button) {
  border-radius: 0.125rem;
}

:deep(.p-button-outlined) {
  background-color: #fff;
}

:deep(.p-button-outlined:hover) {
  background-color: #f9fafb;
}

:deep(.p-dialog) {
  border-radius: 0.125rem;
}

:deep(.p-dialog .p-dialog-header) {
  border-bottom: 1px solid #e5e7eb;
  background-color: #f9fafb;
  border-top-left-radius: 0.125rem;
  border-top-right-radius: 0.125rem;
}

:deep(.p-dialog .p-dialog-footer) {
  border-top: 1px solid #e5e7eb;
  background-color: #f9fafb;
  border-bottom-left-radius: 0.125rem;
  border-bottom-right-radius: 0.125rem;
}
</style>
