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
            <div class="flex items-center border-b border-gray-200 bg-gray-50 rounded-t-sm px-2 py-1 overflow-x-auto">
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
              :admins="tabData[currentTab].admins"
              :designation-options="tabData[currentTab].designationOptions"
              :table-title="tabData[currentTab].tableTitle"
              :create-user-route="tabData[currentTab].createUserRoute"
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
  { label: 'নেগরান/মুমতাহিন/যোন', value: 'others' },
  { label: 'সনদ শাখা', value: 'sanad' },
  { label: 'একাউন্স', value: 'accounts' },
  { label: 'তালিম তারবিয়াত', value: 'talim_tarbiat' },
  { label: 'রেজিষ্ট্রেশন শাখা', value: 'registration' },
  { label: 'প্রকাশনা', value: 'publication' },
  { label: 'প্রশাসন', value: 'administration' },
  { label: 'প্রশিক্ষণ শাখা', value: 'training' }
];
const currentTab = ref('madrasa');

// Dummy Data & Designation
const tabData = {
  madrasa: {
    admins: [
      { id: 1, name: 'মুহাম্মাদ আজিজ', phone: '01710001111', email: 'aziz@madrasa.com', profile_image: '', designation: 1 },
      { id: 2, name: 'শফিকুল ইসলাম', phone: '01710001112', email: 'shafik@madrasa.com', profile_image: '', designation: 2 }
    ],
    designationOptions: [
      { name: 'সুপার এডমিন', value: 1 },
      { name: 'সহ সুপার এডমিন', value: 2 }
    ],
    tableTitle: 'মাদরাসা এডমিন তালিকা',
    createUserRoute: '/admin/create-madrasa-admin'
  },
  board: {
    admins: [
      { id: 11, name: 'আবদুল করিম', phone: '01820002221', email: 'karim@board.com', profile_image: '', designation: 3 },
      { id: 12, name: 'মোঃ হাবিব', phone: '01820002222', email: 'habib@board.com', profile_image: '', designation: 3 }
    ],
    designationOptions: [{ name: 'বোর্ড এডমিন', value: 3 }],
    tableTitle: 'বোর্ড এডমিন তালিকা',
    createUserRoute: '/admin/create-board-admin'
  },
  others: {
    admins: [
      { id: 21, name: 'মাওলানা রশিদ', phone: '01930003331', email: 'rashid@negoran.com', profile_image: '', designation: 4 },
      { id: 22, name: 'ইকবাল হোসেন', phone: '01930003332', email: 'iqbal@mumtahin.com', profile_image: '', designation: 5 },
      { id: 23, name: 'রিয়াদ খান', phone: '01930003333', email: 'riyad@jon.com', profile_image: '', designation: 6 }
    ],
    designationOptions: [
      { name: 'নেগরান', value: 4 },
      { name: 'মুমতাহিন', value: 5 },
      { name: 'যোন', value: 6 }
    ],
    tableTitle: 'নেগরান, মুমতাহিন, যোন তালিকা',
    createUserRoute: '/admin/create-other-admin'
  },
  sanad: {
    admins: [
      { id: 31, name: 'মাহমুদুল হাসান', phone: '01640004444', email: 'mahmud@sanad.com', profile_image: '', designation: 7 },
      { id: 32, name: 'আসাদুজ্জামান', phone: '01640004445', email: 'asad@sanad.com', profile_image: '', designation: 8 }
    ],
    designationOptions: [
      { name: 'সনদ শাখা প্রধান', value: 7 },
      { name: 'সনদ শাখা সহকারী', value: 8 }
    ],
    tableTitle: 'সনদ শাখা ইউজার তালিকা',
    createUserRoute: '/admin/create-sanad-admin'
  },
  accounts: {
    admins: [
      { id: 41, name: 'রাকিবুল ইসলাম', phone: '01550005555', email: 'rakib@accounts.com', profile_image: '', designation: 9 },
      { id: 42, name: 'সাইফুল ইসলাম', phone: '01550005556', email: 'saiful@accounts.com', profile_image: '', designation: 9 }
    ],
    designationOptions: [{ name: 'একাউন্স অফিসার', value: 9 }],
    tableTitle: 'একাউন্স ইউজার তালিকা',
    createUserRoute: '/admin/create-accounts-admin'
  },
  talim_tarbiat: {
    admins: [
      { id: 51, name: 'শামসুল হুদা', phone: '01360006666', email: 'shamsul@talim.com', profile_image: '', designation: 10 }
    ],
    designationOptions: [{ name: 'তালিম তারবিয়াত অফিসার', value: 10 }],
    tableTitle: 'তালিম তারবিয়াত ইউজার তালিকা',
    createUserRoute: '/admin/create-talim-tarbiat-admin'
  },
  registration: {
    admins: [
      { id: 61, name: 'ফারুক আহমেদ', phone: '01470007777', email: 'faruk@registration.com', profile_image: '', designation: 11 }
    ],
    designationOptions: [{ name: 'রেজিষ্ট্রেশন অফিসার', value: 11 }],
    tableTitle: 'রেজিষ্ট্রেশন শাখা ইউজার তালিকা',
    createUserRoute: '/admin/create-registration-admin'
  },
  publication: {
    admins: [
      { id: 71, name: 'হুমায়ুন কবীর', phone: '01780008888', email: 'humayun@publication.com', profile_image: '', designation: 12 }
    ],
    designationOptions: [{ name: 'প্রকাশনা অফিসার', value: 12 }],
    tableTitle: 'প্রকাশনা শাখা ইউজার তালিকা',
    createUserRoute: '/admin/create-publication-admin'
  },
  administration: {
    admins: [
      { id: 81, name: 'মোঃ আনোয়ার', phone: '01890009999', email: 'anwar@administration.com', profile_image: '', designation: 13 }
    ],
    designationOptions: [{ name: 'প্রশাসন অফিসার', value: 13 }],
    tableTitle: 'প্রশাসন ইউজার তালিকা',
    createUserRoute: '/admin/create-administration-admin'
  },
  training: {
    admins: [
      { id: 91, name: 'শহীদুল ইসলাম', phone: '01910001010', email: 'shahidul@training.com', profile_image: '', designation: 14 }
    ],
    designationOptions: [{ name: 'প্রশিক্ষণ অফিসার', value: 14 }],
    tableTitle: 'প্রশিক্ষণ শাখা ইউজার তালিকা',
    createUserRoute: '/admin/create-training-admin'
  }
};
</script>

<style scoped>
.transition-all {
  transition: all 0.2s ease;
}
.shadow-sm {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}
.rounded-sm {
  border-radius: 0.125rem;
}
button:hover {
  transition: background-color 0.2s ease, color 0.2s ease;
}
button:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(107, 114, 128, 0.3);
}
</style>
