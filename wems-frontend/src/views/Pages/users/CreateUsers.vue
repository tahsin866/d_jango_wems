<template>
  <div style="font-family: 'SolaimanLipi', sans-serif;" class="py-12 bg-gray-100">
    <div class="sm:px-6 lg:px-8">
      <div class="border border-gray-200 bg-white shadow-sm rounded-sm">
        <div class="p-6 bg-white border-b border-gray-200">
          <!-- Header -->
          <div class="mb-6 flex items-center gap-3">
            <div class="p-2 rounded-sm bg-gray-100">
              <i class="fas fa-users-cog text-gray-700 text-xl"></i>
            </div>
            <h2 class="text-xl font-bold text-gray-800 leading-tight tracking-tight">
              ইউজার ম্যানেজমেন্ট সিস্টেম
            </h2>
          </div>
          <!-- Tab System -->
          <div class="mb-6">
            <div class="flex items-center border-b border-gray-200 bg-gray-50 rounded-t-sm px-2 py-1">
              <button
                v-for="tab in tabs"
                :key="tab.value"
                class="px-5 py-2 rounded-t-sm font-semibold text-sm transition-all duration-150 focus:outline-none"
                :class="[
                  currentTab === tab.value
                    ? 'bg-white border-l border-r border-t border-gray-300 border-b-0 text-gray-800 shadow-sm'
                    : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
                ]"
                @click="currentTab = tab.value"
              >
                {{ tab.label }}
              </button>
            </div>
          </div>
          <!-- Tab Content -->
          <div class="bg-white border rounded-b-sm px-3 py-6 mt-0">
            <UserTable
              v-if="currentTab === 'madrasa'"
              :admins="madrasaAdmins"
              :designation-options="designationOptionsMadrasa"
              table-title="মাদরাসা এডমিন তালিকা"
              create-user-route="/admin/create-madrasa-admin"
            />
            <UserTable
              v-else-if="currentTab === 'board'"
              :admins="boardAdmins"
              :designation-options="designationOptionsBoard"
              table-title="বোর্ড এডমিন তালিকা"
              create-user-route="/admin/create-board-admin"
            />
            <UserTable
              v-else-if="currentTab === 'others'"
              :admins="otherAdmins"
              :designation-options="designationOptionsOthers"
              table-title="নেগরান, মুমতাহিন, যোন তালিকা"
              create-user-route="/admin/create-other-admin"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import UserTable from './UserTable.vue';

const tabs = [
  { label: 'মাদরাসা এডমিন', value: 'madrasa' },
  { label: 'বোর্ড এডমিন', value: 'board' },
  { label: 'নেগরান/মুমতাহিন/যোন', value: 'others' }
];
const currentTab = ref('madrasa');

// Dummy Data
const madrasaAdmins = ref([
  {
    id: 1,
    name: 'মুহাম্মাদ আজিজ',
    phone: '01710001111',
    email: 'aziz@madrasa.com',
    profile_image: '',
    designation: 1
  },
  {
    id: 2,
    name: 'শফিকুল ইসলাম',
    phone: '01710001112',
    email: 'shafik@madrasa.com',
    profile_image: '',
    designation: 2
  }
]);

const boardAdmins = ref([
  {
    id: 11,
    name: 'আবদুল করিম',
    phone: '01820002221',
    email: 'karim@board.com',
    profile_image: '',
    designation: 3
  },
  {
    id: 12,
    name: 'মোঃ হাবিব',
    phone: '01820002222',
    email: 'habib@board.com',
    profile_image: '',
    designation: 3
  }
]);

const otherAdmins = ref([
  {
    id: 21,
    name: 'মাওলানা রশিদ',
    phone: '01930003331',
    email: 'rashid@negoran.com',
    profile_image: '',
    designation: 4 // নেগরান
  },
  {
    id: 22,
    name: 'ইকবাল হোসেন',
    phone: '01930003332',
    email: 'iqbal@mumtahin.com',
    profile_image: '',
    designation: 5 // মুমতাহিন
  },
  {
    id: 23,
    name: 'রিয়াদ খান',
    phone: '01930003333',
    email: 'riyad@jon.com',
    profile_image: '',
    designation: 6 // যোন
  }
]);

// Designation dropdown options for each tab
const designationOptionsMadrasa = [
  { name: 'সুপার এডমিন', value: 1 },
  { name: 'সহ সুপার এডমিন', value: 2 }
];
const designationOptionsBoard = [
  { name: 'বোর্ড এডমিন', value: 3 }
];
const designationOptionsOthers = [
  { name: 'নেগরান', value: 4 },
  { name: 'মুমতাহিন', value: 5 },
  { name: 'যোন', value: 6 }
];
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

/* Tab hover effects */
button:hover {
  transition: background-color 0.2s ease, color 0.2s ease;
}

/* Custom focus styles for accessibility */
button:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(107, 114, 128, 0.3);
}
</style>
