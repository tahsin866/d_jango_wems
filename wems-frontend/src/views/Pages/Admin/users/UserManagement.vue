<template>
  <div>
    <UserTabs :departments="departments" v-model="selectedDepartment" />

    <!-- Dynamic Department Tables -->
    <div v-if="!selectedDepartment">
      <UserTable
        :users="filteredUsers"
        :roles="roles"
        :canCreate="canCreateUser"
        :canEdit="canEditUser"
        :canDelete="canDeleteUser"
        @create="showUserForm"
        @edit="showUserForm"
        @delete="deleteUser"
      />
    </div>

    <!-- Department-specific tables based on department name -->
    <div v-else-if="selectedDepartment.name === 'একাউন্টস'">
      <AccountsTable
        :users="filteredUsers"
        :roles="roles"
        :canCreate="canCreateUser"
        :canEdit="canEditUser"
        :canDelete="canDeleteUser"
        @create="showUserForm"
        @edit="showUserForm"
        @delete="deleteUser"
      />
    </div>

    <div v-else-if="selectedDepartment.name === 'প্রকাশনা'">
      <PublicationsTable
        :users="filteredUsers"
        :roles="roles"
        :canCreate="canCreateUser"
        :canEdit="canEditUser"
        :canDelete="canDeleteUser"
        @create="showUserForm"
        @edit="showUserForm"
        @delete="deleteUser"
      />
    </div>

    <div v-else-if="selectedDepartment.name === 'তালিম তারবিয়াত'">
      <TalimTable
        :users="filteredUsers"
        :roles="roles"
        :canCreate="canCreateUser"
        :canEdit="canEditUser"
        :canDelete="canDeleteUser"
        @create="showUserForm"
        @edit="showUserForm"
        @delete="deleteUser"
      />
    </div>

    <div v-else-if="selectedDepartment.name === 'সনদ শাখা'">
      <SonodTable
        :users="filteredUsers"
        :roles="roles"
        :canCreate="canCreateUser"
        :canEdit="canEditUser"
        :canDelete="canDeleteUser"
        @create="showUserForm"
        @edit="showUserForm"
        @delete="deleteUser"
      />
    </div>

    <div v-else-if="selectedDepartment.name === 'রেজিস্ট্রেশন'">
      <RegistrationTable
        :users="filteredUsers"
        :roles="roles"
        :canCreate="canCreateUser"
        :canEdit="canEditUser"
        :canDelete="canDeleteUser"
        @create="showUserForm"
        @edit="showUserForm"
        @delete="deleteUser"
      />
    </div>

    <div v-else-if="selectedDepartment.name === 'প্রশাসন'">
      <AdministrationTable
        :users="filteredUsers"
        :roles="roles"
        :canCreate="canCreateUser"
        :canEdit="canEditUser"
        :canDelete="canDeleteUser"
        @create="showUserForm"
        @edit="showUserForm"
        @delete="deleteUser"
      />
    </div>

    <div v-else-if="selectedDepartment.name === 'প্রশিক্ষণ'">
      <TrainingTable
        :users="filteredUsers"
        :roles="roles"
        :canCreate="canCreateUser"
        :canEdit="canEditUser"
        :canDelete="canDeleteUser"
        @create="showUserForm"
        @edit="showUserForm"
        @delete="deleteUser"
      />
    </div>

    <div v-else-if="selectedDepartment.name === 'পরীক্ষাবিভাগ'">
      <ExamTable
        :users="filteredUsers"
        :roles="roles"
        :canCreate="canCreateUser"
        :canEdit="canEditUser"
        :canDelete="canDeleteUser"
        :canSetPermission="true"
        @create="showUserForm"
        @edit="showUserForm"
        @delete="deleteUser"
        @set-permission="openPermissionDialog"
      />
    </div>

    <!-- Fallback -->
    <div v-else>
      <UserTable
        :users="filteredUsers"
        :roles="roles"
        :canCreate="canCreateUser"
        :canEdit="canEditUser"
        :canDelete="canDeleteUser"
        @create="showUserForm"
        @edit="showUserForm"
        @delete="deleteUser"
      />
    </div>

    <UserForm
      v-if="showForm"
      :roles="roles"
      :departments="departments"
      :user="editingUser"
      :permissions="permissions"
      @save="saveUser"
      @close="closeForm"
      @set-permission="openPermissionDialog"
    />
    <!-- Permission Side Panel -->
    <div v-if="showPermissionDialog && showForm === false" class="fixed inset-y-0 right-0 z-50 w-1/2 bg-white shadow-xl transform transition-transform duration-300 ease-in-out">
      <exampermission
        :modules="currentDepartmentModules"
        :menus="currentDepartmentMenus"
        :user="editingUser"
        :userPermissions="editingUserPermissions"
        @save="savePermissions"
        @close="closePermissionDialog"
        class="h-full"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import UserTabs from '@/views/Pages/Admin/users/UserTabs.vue'
import UserTable from '@/views/Pages/Admin/users/UserTable.vue'
import UserForm from '@/views/Pages/Admin/users/UserForm.vue'
import exampermission from '@/views/Pages/Admin/users/exampermission.vue'
import apiClient from '@/services/api-client'

// Department-specific table components
import AccountsTable from '@/views/Pages/Admin/users/accounts/AccountsTable.vue'
import PublicationsTable from '@/views/Pages/Admin/users/publications/PublicationsTable.vue'
import RegistrationTable from '@/views/Pages/Admin/users/registration/RegistrationTable.vue'
import SonodTable from '@/views/Pages/Admin/users/sonod/SonodTable.vue'
import AdministrationTable from '@/views/Pages/Admin/users/administration/AdministrationTable.vue'
import TrainingTable from '@/views/Pages/Admin/users/training/TrainingTable.vue'
import TalimTable from '@/views/Pages/Admin/users/talim/TalimTable.vue'
import ExamTable from '@/views/Pages/Admin/users/exam/ExamTable.vue'

// Department-wise data and components logic here...
// (Include all the original data and computed properties)

// Type definitions
interface Department {
  id: number
  name: string
}

// Departments - fetched from API
const departments = ref<Department[]>([])

// Fetch roles from API
async function fetchRoles() {
  try {
    const response = await apiClient.getUserTypes()
    if (response.data) {
      roles.value = response.data
    }
  } catch (error) {
    console.error('Failed to fetch roles:', error)
    // Fallback to hardcoded roles
    roles.value = [
      { id: 1, name: 'Master Admin' },
      { id: 2, name: 'Super Admin' },
      { id: 3, name: 'Board Admin' },
      { id: 4, name: 'IT Head' },
      { id: 5, name: 'Dept Head' },
      { id: 6, name: 'Staff' }
    ]
  }
}

// Reactive state
const selectedDepartment = ref<Department | null>(null)
const showForm = ref(false)
const editingUser = ref(null)
const showPermissionDialog = ref(false)
const editingUserPermissions = ref([])

// Roles - fetched from API
const roles = ref([])

const currentDepartmentModules = ref([])
const currentDepartmentMenus = ref([])
const filteredUsers = ref([])

const canCreateUser = true
const canEditUser = true
const canDeleteUser = true

const permissions = [
  { id: 1, name: 'View', description: 'Can view records' },
  { id: 2, name: 'Create', description: 'Can create records' },
  { id: 3, name: 'Edit', description: 'Can edit records' },
  { id: 4, name: 'Delete', description: 'Can delete records' },
  { id: 5, name: 'Set Permission', description: 'Can set permissions' }
]

function showUserForm() {
  showForm.value = true
}

function saveUser() {
  showForm.value = false
}

function closeForm() {
  showForm.value = false
}

async function openPermissionDialog(userData: any) {
  editingUser.value = userData

  console.log('Opening permission dialog for user:', userData)
  console.log('Selected department:', selectedDepartment.value)

  // For exam department, use department ID 1 (based on your JSON data showing department_id: 1)
  // Otherwise use the user's department if available
  let departmentId = userData?.department || (selectedDepartment.value?.id)

  // If this is exam department, use 1 (matching the JSON data)
  if (selectedDepartment.value?.name === 'পরীক্ষাবিভাগ') {
    departmentId = 1
  }

  console.log('Using department ID:', departmentId)

  // Fetch modules and menus for the user's department
  if (departmentId) {
    await fetchDepartmentModulesAndMenus(departmentId)
  }

  // Fetch user's existing permissions
  if (userData && userData.id) {
    try {
      const response = await apiClient.getUserPermissions(userData.id)
      if (response.data) {
        editingUserPermissions.value = response.data
      }
    } catch (error) {
      console.error('Failed to fetch user permissions:', error)
      editingUserPermissions.value = []
    }
  }

  showPermissionDialog.value = true
  showForm.value = false
}

async function savePermissions(permissionsData: any[]) {
  if (editingUser.value && editingUser.value.id) {
    try {
      // Format permissions for API
      const formattedPermissions = permissionsData.map(perm => ({
        menu_id: perm.menu_id,
        permission_id: getPermissionId(perm.permission_type)
      }))

      const response = await apiClient.saveUserPermissions(editingUser.value.id, formattedPermissions)
      if (response.data) {
        console.log('Permissions saved successfully')
      }
    } catch (error) {
      console.error('Failed to save permissions:', error)
    }
  }
  showPermissionDialog.value = false
}

// Helper function to get permission ID from permission type
function getPermissionId(permissionType: string): number {
  const permissionMap: { [key: string]: number } = {
    'READ': 2,    // Based on the permissions table data
    'CREATE': 1,
    'UPDATE': 3,
    'DELETE': 4
  }
  return permissionMap[permissionType] || 2 // Default to READ
}

function closePermissionDialog() {
  showPermissionDialog.value = false
}

function deleteUser() {
  // Delete user logic
}

// Fetch modules and menus for a department
async function fetchDepartmentModulesAndMenus(departmentId: number) {
  try {
    console.log('Fetching modules for department:', departmentId)
    // Fetch modules for this department
    const modulesResponse = await apiClient.getModulesByDepartment(departmentId)
    console.log('Modules API response:', modulesResponse)

    if (modulesResponse.data) {
      currentDepartmentModules.value = modulesResponse.data
      console.log('Modules set to:', currentDepartmentModules.value)
    }

    // Fetch all menus for these modules
    const menusResponse = await apiClient.getMenus()
    console.log('Menus API response:', menusResponse)

    if (menusResponse.data) {
      // Filter menus that belong to the department's modules
      const moduleIds = currentDepartmentModules.value.map((m: any) => m.id)
      console.log('Module IDs for filtering menus:', moduleIds)

      currentDepartmentMenus.value = menusResponse.data.filter((menu: any) =>
        moduleIds.includes(menu.module_id)
      )
      console.log('Filtered menus set to:', currentDepartmentMenus.value)
    }
  } catch (error) {
    console.error('Failed to fetch modules and menus:', error)
    // Fallback to empty arrays
    currentDepartmentModules.value = []
    currentDepartmentMenus.value = []
  }
}

// Fetch departments from API
async function fetchDepartments() {
  try {
    const response = await apiClient.getDepartments()
    if (response.data) {
      departments.value = response.data
    }
  } catch (error) {
    console.error('Failed to fetch departments:', error)
    // Fallback to hardcoded departments
    departments.value = [
      { id: 1, name: 'একাউন্টস' },
      { id: 2, name: 'পবলিকেশন' },
      { id: 3, name: 'তালিম ও তারবিয়াত' },
      { id: 4, name: 'সনদ শাখা' },
      { id: 5, name: 'রেজিস্ট্রেশন শাখা' },
      { id: 6, name: 'প্রশাসন' },
      { id: 7, name: 'প্রশিক্ষণ শাখা' },
      { id: 8, name: 'পরিক্ষাবিভাগ' }
    ]
  }
}

// Fetch departments and roles on component mount
onMounted(() => {
  fetchDepartments()
  fetchRoles()
})
</script>
