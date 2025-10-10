<template>
  <div style="font-family: 'SolaimanLipi', sans-serif;">
    <!-- Debug Info for SonodTable -->
    <div class="mb-2 p-2 bg-yellow-50 rounded text-xs text-yellow-600">
      <strong>সনদ শাখা টেবিল লোড হয়েছে</strong> - Total Users: {{ users.length }}
    </div>

    <div class="overflow-x-auto mt-4">
      <table class="min-w-full border border-gray-200 rounded-lg shadow-sm bg-white">
        <thead>
          <tr class="bg-gray-100">
            <th class="px-4 py-2 text-left font-semibold text-gray-700">নাম</th>
            <th class="px-4 py-2 text-left font-semibold text-gray-700">ইমেইল</th>
            <th class="px-4 py-2 text-left font-semibold text-gray-700">রোল</th>
            <th class="px-4 py-2 text-left font-semibold text-gray-700">সনদ পজিশন</th>
            <th class="px-4 py-2 text-left font-semibold text-gray-700">স্ট্যাটাস</th>
            <th class="px-4 py-2 text-left font-semibold text-gray-700">একশন</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50 border-b last:border-b-0">
            <td class="px-4 py-2 whitespace-nowrap">{{ user.name }}</td>
            <td class="px-4 py-2 whitespace-nowrap">{{ user.email }}</td>
            <td class="px-4 py-2 whitespace-nowrap">{{ getRole(user.role) }}</td>
            <td class="px-4 py-2 whitespace-nowrap">{{ user.position || 'N/A' }}</td>
            <td class="px-4 py-2 whitespace-nowrap">
              <span :class="user.status === 'active' ? 'bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-medium' : 'bg-red-100 text-red-700 px-2 py-1 rounded text-xs font-medium'">
                {{ user.status === 'active' ? 'সক্রিয়' : 'নিষ্ক্রিয়' }}
              </span>
            </td>
            <td class="px-4 py-2 whitespace-nowrap">
              <button v-if="canEdit" @click="$emit('edit', user)" class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded mr-2 text-xs">Edit</button>
              <button v-if="canDelete" @click="$emit('delete', user)" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-xs">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="mt-4">
      <button v-if="canCreate" @click="$emit('create')" class="bg-green-500 hover:bg-green-600 text-white px-4 py-3 rounded-sm shadow text-sm font-semibold">নতুন সনদ ইউজার</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// Type definitions
interface Role {
  id: number
  name: string
}

interface User {
  id: number
  name: string
  email: string
  role: number
  position: string
  status: string
}

const props = defineProps<{
  users?: User[]
  roles?: Role[]
  canCreate?: boolean
  canEdit?: boolean
  canDelete?: boolean
}>()

// Dummy data fallback for roles and users
const dummyRoles: Role[] = [
  { id: 1, name: 'Master Admin' },
  { id: 2, name: 'Super Admin' },
  { id: 3, name: 'Board Admin' },
  { id: 4, name: 'IT Head' },
  { id: 5, name: 'Dept Head' },
  { id: 6, name: 'Staff' }
]

const dummyUsers: User[] = [
  { id: 16, name: 'Certificate Head', email: 'certhead@erp.com', role: 5, position: 'Head of Certificates', status: 'active' },
  { id: 17, name: 'Certificate Officer', email: 'certofficer@erp.com', role: 6, position: 'Certificate Officer', status: 'active' },
  { id: 18, name: 'Data Entry Operator', email: 'dataentry@erp.com', role: 6, position: 'Data Entry Operator', status: 'active' },
  { id: 19, name: 'Document Verifier', email: 'docverifier@erp.com', role: 6, position: 'Document Verifier', status: 'active' }
]

// Use props or fallback to dummy data
const roles = computed(() => props.roles && props.roles.length > 0 ? props.roles : dummyRoles)
const users = computed(() => props.users && props.users.length > 0 ? props.users : dummyUsers)
const canCreate = computed(() => props.canCreate ?? true)
const canEdit = computed(() => props.canEdit ?? true)
const canDelete = computed(() => props.canDelete ?? true)

function getRole(roleId: number): string {
  const role = roles.value.find((r: Role) => r.id === roleId)
  return role ? role.name : 'Unknown'
}
</script>
