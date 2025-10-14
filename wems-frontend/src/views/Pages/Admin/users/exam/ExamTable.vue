<template>
  <div style="font-family: 'SolaimanLipi', sans-serif;">
    <!-- Exam Department Tabs -->
    <div class="bg-white rounded-sm text-xl shadow-sm mb-4 mt-10">
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8 px-6 py-3 text-xl">
          <button
            v-for="tab in examTabs"
            :key="tab.id"
            @click="selectedExamTab = tab"
            :class="[
              'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm',
              selectedExamTab.id === tab.id
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            {{ tab.name }}
          </button>
        </nav>
      </div>
    </div>

    <!-- Current Tab Table -->
    <div class="overflow-x-auto mt-4">
      <table class="min-w-full border border-gray-200 rounded-sm shadow-sm bg-white">
        <thead>
          <tr class="bg-gray-100">
            <th class="px-4 py-2 text-left font-semibold text-gray-700">নাম</th>
            <th class="px-4 py-2 text-left font-semibold text-gray-700">ইমেইল</th>
            <th class="px-4 py-2 text-left font-semibold text-gray-700">রোল</th>
            <th class="px-4 py-2 text-left font-semibold text-gray-700">{{ selectedExamTab.positionLabel }}</th>
            <th class="px-4 py-2 text-left font-semibold text-gray-700">স্ট্যাটাস</th>
            <th class="px-4 py-2 text-left font-semibold text-gray-700">একশন</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in currentTabUsers" :key="user.id" class="hover:bg-gray-50 border-b last:border-b-0">
            <td class="px-4 py-2 whitespace-nowrap">{{ user.name }}</td>
            <td class="px-4 py-2 whitespace-nowrap">{{ user.email }}</td>
            <td class="px-4 py-2 whitespace-nowrap">{{ getRole(user.role) }}</td>
            <td class="px-4 py-2 whitespace-nowrap">{{ user.position || 'N/A' }}</td>
            <td class="px-4 py-2 whitespace-nowrap">
              <span :class="user.status === 'active' ? 'bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-medium' : 'bg-red-100 text-red-700 px-2 py-1 rounded text-xs font-medium'">
                {{ user.status }}
              </span>
            </td>
            <td class="px-4 py-2 whitespace-nowrap">
              <button v-if="canEdit" @click="$emit('edit', user)" class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded mr-2 text-xs">Edit</button>
              <button v-if="canSetPermission" @click="$emit('set-permission', user)" class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded mr-2 text-xs">সেট পারমিশন</button>
              <button v-if="canDelete" @click="$emit('delete', user)" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-xs">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="mt-4">
      <button v-if="canCreate" @click="$emit('create')" class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded shadow text-sm font-semibold">
        নতুন {{ selectedExamTab.name }} যোগ করুন
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps(['users', 'roles', 'canCreate', 'canEdit', 'canDelete', 'canSetPermission'])

// Exam Department Tabs
const examTabs = [
  {
    id: 1,
    name: 'এডমিন',
    positionLabel: 'এডমিন পজিশন',
    type: 'admin'
  },
  {
    id: 2,
    name: 'নেগরান',
    positionLabel: 'নেগরান পজিশন',
    type: 'negran'
  },
  {
    id: 3,
    name: 'মুমতাহিন',
    positionLabel: 'মুমতাহিন পজিশন',
    type: 'mumtahin'
  },
  {
    id: 4,
    name: 'জোনাল',
    positionLabel: 'জোনাল পজিশন',
    type: 'zonal'
  },
  {
    id: 5,
    name: 'শিক্ষার্থী',
    positionLabel: 'শিক্ষার্থী পজিশন',
    type: 'student'
  },
  {
    id: 6,
    name: 'মরকায দায়িত্বশীল',
    positionLabel: 'মরকায পজিশন',
    type: 'markaz_responsible'
  }
]

// Selected tab state
const selectedExamTab = ref(examTabs[0])

// Tab-specific user data
const examUsersData = {
  admin: [
    { id: 24, name: 'Exam Head', email: 'examhead@erp.com', role: 5, position: 'Head of Exams', status: 'active', type: 'admin' },
    { id: 25, name: 'Exam Controller', email: 'examcontroller@erp.com', role: 6, position: 'Exam Controller', status: 'active', type: 'admin' },
    { id: 26, name: 'Admin Assistant', email: 'adminassist@erp.com', role: 6, position: 'Admin Assistant', status: 'active', type: 'admin' }
  ],
  negran: [
    { id: 30, name: 'জোনাল নেগরান ১', email: 'negran1@erp.com', role: 6, position: 'জোনাল নেগরান', status: 'active', type: 'negran' },
    { id: 31, name: 'জোনাল নেগরান ২', email: 'negran2@erp.com', role: 6, position: 'জোনাল নেগরান', status: 'active', type: 'negran' },
    { id: 32, name: 'এলাকা নেগরান', email: 'negran3@erp.com', role: 6, position: 'এলাকা নেগরান', status: 'active', type: 'negran' }
  ],
  mumtahin: [
    { id: 35, name: 'মুমতাহিন ১', email: 'mumtahin1@erp.com', role: 6, position: 'সিনিয়র মুমতাহিন', status: 'active', type: 'mumtahin' },
    { id: 36, name: 'মুমতাহিন ২', email: 'mumtahin2@erp.com', role: 6, position: 'জুনিয়র মুমতাহিন', status: 'active', type: 'mumtahin' },
    { id: 37, name: 'মুমতাহিন ৩', email: 'mumtahin3@erp.com', role: 6, position: 'পরীক্ষা গ্রহণকারী', status: 'active', type: 'mumtahin' }
  ],
  zonal: [
    { id: 40, name: 'জোনাল হেড ১', email: 'zonal1@erp.com', role: 5, position: 'জোনাল হেড', status: 'active', type: 'zonal' },
    { id: 41, name: 'জোনাল কর্মকর্তা ১', email: 'zonal2@erp.com', role: 6, position: 'জোনাল কর্মকর্তা', status: 'active', type: 'zonal' },
    { id: 42, name: 'জোনাল সহায়ক', email: 'zonal3@erp.com', role: 6, position: 'জোনাল সহায়ক', status: 'active', type: 'zonal' }
  ],
  student: [
    { id: 45, name: 'আহমদ হাসান', email: 'ahmad@student.com', role: 7, position: 'দাওরায়ে হাদিস', status: 'active', type: 'student' },
    { id: 46, name: 'মুহাম্মদ আলী', email: 'ali@student.com', role: 7, position: 'তাকমিল', status: 'active', type: 'student' },
    { id: 47, name: 'আব্দুল্লাহ করিম', email: 'karim@student.com', role: 7, position: 'মুতাওয়াসসিতা', status: 'active', type: 'student' }
  ],
  markaz_responsible: [
    { id: 50, name: 'মরকায দায়িত্বশীল ১', email: 'markaz1@erp.com', role: 6, position: 'প্রধান দায়িত্বশীল', status: 'active', type: 'markaz_responsible' },
    { id: 51, name: 'মরকায দায়িত্বশীল ২', email: 'markaz2@erp.com', role: 6, position: 'সহকারী দায়িত্বশীল', status: 'active', type: 'markaz_responsible' },
    { id: 52, name: 'মরকায কো-অর্ডিনেটর', email: 'markaz3@erp.com', role: 6, position: 'কো-অর্ডিনেটর', status: 'active', type: 'markaz_responsible' }
  ]
}

// Computed users for current selected tab
const currentTabUsers = computed(() => {
  return examUsersData[selectedExamTab.value.type as keyof typeof examUsersData] || []
})

const canCreate = props.canCreate ?? true
const canEdit = props.canEdit ?? true
const canDelete = props.canDelete ?? true
const canSetPermission = props.canSetPermission ?? true

function getRole(roleId: number) {
  const roles = [
    { id: 5, name: 'Dept Head' },
    { id: 6, name: 'Staff' },
    { id: 7, name: 'Student' }
  ]
  const role = roles.find(r => r.id === roleId)
  return role ? role.name : ''
}
</script>
