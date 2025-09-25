<template>
  <div>
    <!-- AdminLTE Box Header -->
    <div class="flex flex-col md:flex-row justify-between gap-4 mb-4 items-center border-b border-gray-300 bg-gray-50 rounded-t px-4 py-3">
      <!-- Search -->
      <div class="flex-1">
        <div class="relative">
          <span class="p-input-icon-left w-full">
            <InputText
              v-model="filters['global'].value"
              :placeholder="`${tableTitle} থেকে ফোন নম্বর দিয়ে সার্চ করুন`"
              class="w-full border border-gray-300 rounded px-3 py-2 focus:border-indigo-500 focus:ring-indigo-300 focus:ring-1 shadow-sm"
            />
            <i class="fas fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
          </span>
        </div>
      </div>
      <!-- Create User Button -->
      <div>
        <RouterLink
          :to="createUserRoute"
          class="inline-flex items-center px-4 py-2 bg-indigo-700 border border-indigo-800 rounded font-bold text-xs text-white uppercase tracking-wider hover:bg-indigo-800 shadow transition"
        >
          <i class="fas fa-user-plus mr-2"></i>
          নতুন ইউজার
        </RouterLink>
      </div>
    </div>
    <!-- AdminLTE Table -->
    <div class="bg-white border border-gray-300 shadow-sm rounded-b px-2 pb-4">
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
            <div class="h-10 w-10 rounded-full overflow-hidden border border-gray-200 bg-gray-100">
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
            <span class="px-2 py-1 inline-flex text-xs leading-5 font-bold rounded-full border border-gray-300"
                  :class="getDesignationClass(slotProps.data.designation)">
              <i class="fas fa-user-tag mr-1"></i>
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
                  <i class="fas fa-exclamation-triangle mr-3 text-red-500" style="font-size: 2rem"></i>
                  <div>
                    <p class="text-sm text-gray-500">
                      আপনি কি নিশ্চিত যে আপনি এই এডমিন ডিলিট করতে চান? এই কাজটি অপরিবর্তনীয়।
                    </p>
                  </div>
                </div>
                <template #footer>
                  <Button label="বাতিল করুন" icon="pi pi-times" class="p-button-text" @click="showModal = false" />
                  <Button label="ডিলিট করুন" icon="pi pi-check" class="p-button-danger" @click="deleteAdmin" />
                </template>
              </Dialog>
              <SplitButton
                label="সংশোধন"
                @click="editUser(slotProps.data.id)"
                :model="getActionItems(slotProps.data.id)"
                class="p-button-sm  text-gray-700 font-semibold "
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
  switch (designation) {
    case 1: return 'bg-purple-100 text-purple-800';
    case 2: return 'bg-gray-100 text-gray-800';
    case 3: return 'bg-blue-100 text-blue-800';
    case 4: return 'bg-green-100 text-green-800';
    case 5: return 'bg-pink-100 text-pink-800';
    case 6: return 'bg-yellow-100 text-yellow-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};
</script>
