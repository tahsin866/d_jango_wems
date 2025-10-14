<template>
  <div class="overflow-x-auto mt-4">
    <table class="min-w-full border border-gray-200 rounded-lg shadow-sm bg-white">
      <thead>
        <tr class="bg-gray-100">
          <th class="px-4 py-2 text-left font-semibold text-gray-700">নাম</th>
          <th class="px-4 py-2 text-left font-semibold text-gray-700">ইমেইল</th>
          <th class="px-4 py-2 text-left font-semibold text-gray-700">রোল</th>
          <th class="px-4 py-2 text-left font-semibold text-gray-700">ডিপার্টমেন্ট</th>
          <th class="px-4 py-2 text-left font-semibold text-gray-700">স্ট্যাটাস</th>
          <th class="px-4 py-2 text-left font-semibold text-gray-700">একশন</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50 border-b last:border-b-0">
          <td class="px-4 py-2 whitespace-nowrap">{{ user.name }}</td>
          <td class="px-4 py-2 whitespace-nowrap">{{ user.email }}</td>
          <td class="px-4 py-2 whitespace-nowrap">{{ getRole(user.role) }}</td>
          <td class="px-4 py-2 whitespace-nowrap">{{ getDepartment(user.department) }}</td>
          <td class="px-4 py-2 whitespace-nowrap">
            <span :class="user.status === 'Active' ? 'bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-medium' : 'bg-red-100 text-red-700 px-2 py-1 rounded text-xs font-medium'">
              {{ user.status }}
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
    <button v-if="canCreate" @click="$emit('create')" class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded shadow text-sm font-semibold">নতুন ইউজার</button>
  </div>
</template>
<script setup>
const props = defineProps(['users', 'roles', 'canCreate', 'canEdit', 'canDelete'])

// Dummy data fallback for roles and users
const dummyRoles = [
  { id: 1, name: 'Admin' },
  { id: 2, name: 'Editor' },
  { id: 3, name: 'Viewer' }
]
const dummyUsers = [
  { id: 1, name: 'John Doe', email: 'john@example.com', role: 1, department: 1, status: 'Active' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 2, department: 2, status: 'Inactive' }
]

const roles = props.roles || dummyRoles
const users = props.users || dummyUsers
const canCreate = props.canCreate ?? true
const canEdit = props.canEdit ?? true
const canDelete = props.canDelete ?? true

function getRole(roleId) {
  const role = roles.find(r => r.id === roleId)
  return role ? role.name : ''
}
function getDepartment(deptId) {
  if (!deptId) return ''
  const departments = [
    { id: 1, name: 'Accounts' }, { id: 2, name: 'Publication' }, { id: 3, name: 'Talim & Tarbiat' }, { id: 4, name: 'Sanad' }, { id: 5, name: 'Registration' }, { id: 6, name: 'Administration' }, { id: 7, name: 'Training' }
  ]
  const dept = departments.find(d => d.id === deptId)
  return dept ? dept.name : ''
}
</script>
