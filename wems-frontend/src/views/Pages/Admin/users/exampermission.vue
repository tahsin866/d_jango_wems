<template>
  <div
  style="                                                                    font-family: 'SolaimanLipi', sans-serif;
                                                "


  class="h-full bg-white border-l border-gray-200 flex flex-col mt-10">
    <!-- Header -->
    <div class="border-b border-gray-200 px-6 py-4 flex justify-between items-center flex-shrink-0">
      <div>
        <h2 class="text-xl font-bold text-gray-800">পারমিশন সেট করুন</h2>
        <p class="text-sm text-gray-600 mt-1" v-if="user">ব্যবহারকারী: {{ user.name || user.email || 'Unknown' }}</p>
      </div>
      <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
    </div>

    <!-- Content with proper scrolling -->
    <div class="flex-1 overflow-y-auto p-6 scrollable-content" style="height: calc(100vh - 200px);">
      <!-- Module List Wrapper -->
      <div class="content-wrapper">
        <div class="space-y-6">
        <div
          v-for="module in modules"
          :key="module.id"
          class="bg-gray-50 rounded-lg p-4"
        >
          <div class="flex items-center gap-3 mb-4">
            <!-- Module Checkbox -->
            <label class="flex items-center">
              <input
                type="checkbox"
                class="mr-2 w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
                :checked="hasModulePermission(module.id)"
                @change="toggleModulePermission(module.id, $event)"
              />
            </label>

            <span v-if="module.icon" class="text-xl">
              <i :class="module.icon"></i>
            </span>
            <div>
              <h3 class="text-lg font-semibold text-gray-800">{{ module.name }}</h3>
              <p class="text-gray-500 text-sm" v-if="module.description">{{ module.description }}</p>
            </div>
          </div>

          <!-- Menu List for this module -->
          <div class="space-y-2">
            <div
              v-for="menu in getMenus(module.id)"
              :key="menu.id"
              class="flex items-center justify-between bg-white rounded px-3 py-2 border"
            >
              <div class="flex items-center">
                <span v-if="menu.icon" class="mr-2 text-sm">
                  <i :class="menu.icon"></i>
                </span>
                <div>
                  <span class="font-medium text-gray-700">{{ menu.name }}</span>
                  <span class="text-xs text-gray-400 ml-2" v-if="menu.description">{{ menu.description }}</span>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <label class="flex items-center">
                  <input
                    type="checkbox"
                    class="mr-1"
                    :checked="hasPermission(menu.id, 'READ')"
                    @change="togglePermission(menu.id, 'READ', $event)"
                  />
                  View
                </label>
                <label class="flex items-center">
                  <input
                    type="checkbox"
                    class="mr-1"
                    :checked="hasPermission(menu.id, 'CREATE')"
                    @change="togglePermission(menu.id, 'CREATE', $event)"
                  />
                  Create
                </label>
                <label class="flex items-center">
                  <input
                    type="checkbox"
                    class="mr-1"
                    :checked="hasPermission(menu.id, 'UPDATE')"
                    @change="togglePermission(menu.id, 'UPDATE', $event)"
                  />
                  Edit
                </label>
                <label class="flex items-center">
                  <input
                    type="checkbox"
                    class="mr-1"
                    :checked="hasPermission(menu.id, 'DELETE')"
                    @change="togglePermission(menu.id, 'DELETE', $event)"
                  />
                  Delete
                </label>
              </div>
            </div>
          </div>
        </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Fixed Footer Buttons -->
    <div class="fixed-bottom-bar">
      <button @click="$emit('close')" class="btn-cancel">Cancel</button>
      <button @click="savePermissions" class="btn-save">Save</button>
    </div>

</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const props = defineProps(['modules', 'menus', 'user', 'userPermissions'])
const emit = defineEmits(['save', 'close'])

// Local state for permissions
const localPermissions = ref([])

// Initialize permissions from props or empty
onMounted(() => {
  console.log('exampermission mounted with props:', {
    modules: props.modules,
    menus: props.menus,
    user: props.user,
    userPermissions: props.userPermissions
  })

  if (props.userPermissions && props.userPermissions.length > 0) {
    localPermissions.value = [...props.userPermissions]
  }
})

// Use props.modules and props.menus or fallback data
const modules = computed(() => props.modules || [
  { id: 1, name: 'পরীক্ষা ব্যবস্থাপনা', description: 'পরীক্ষা পরিচালনা ব্যবস্থা', icon: 'fas fa-clipboard-list' },
  { id: 2, name: 'ফলাফল প্রকাশ', description: 'পরীক্ষার ফলাফল প্রকাশ', icon: 'fas fa-chart-bar' },
  { id: 3, name: 'সার্টিফিকেট', description: 'সার্টিফিকেট প্রদান ব্যবস্থা', icon: 'fas fa-certificate' },
  { id: 4, name: 'কেন্দ্র ব্যবস্থাপনা', description: 'পরীক্ষা কেন্দ্র ব্যবস্থাপনা', icon: 'fas fa-map-marker-alt' }
])

const menus = computed(() => props.menus || [
  { id: 1, module_id: 1, name: 'পরীক্ষা ড্যাশবোর্ড', description: 'পরীক্ষার সারসংক্ষেপ', href: '/exam/dashboard', icon: 'fas fa-tachometer-alt' },
  { id: 2, module_id: 1, name: 'পরীক্ষা তালিকা', description: 'সকল পরীক্ষার তালিকা', href: '/exam/list', icon: 'fas fa-list' },
  { id: 3, module_id: 1, name: 'নতুন পরীক্ষা', description: 'নতুন পরীক্ষা তৈরি করুন', href: '/exam/create', icon: 'fas fa-plus-circle' },
  { id: 4, module_id: 2, name: 'ফলাফল দেখুন', description: 'ফলাফল দেখুন', href: '/results/view', icon: 'fas fa-eye' },
  { id: 5, module_id: 2, name: 'ফলাফল প্রকাশ', description: 'ফলাফল প্রকাশ করুন', href: '/results/publish', icon: 'fas fa-bullhorn' },
  { id: 6, module_id: 3, name: 'সার্টিফিকেট তৈরি', description: 'সার্টিফিকেট তৈরি করুন', href: '/certificate/create', icon: 'fas fa-file-certificate' },
  { id: 7, module_id: 3, name: 'সার্টিফিকেট ডাউনলোড', description: 'সার্টিফিকেট ডাউনলোড করুন', href: '/certificate/download', icon: 'fas fa-download' },
  { id: 8, module_id: 4, name: 'কেন্দ্র তালিকা', description: 'পরীক্ষা কেন্দ্রের তালিকা', href: '/centers/list', icon: 'fas fa-map' },
  { id: 9, module_id: 4, name: 'কেন্দ্র বরাদ্দ', description: 'কেন্দ্র বরাদ্দ করুন', href: '/centers/assign', icon: 'fas fa-check-circle' }
])

// Filter menus for each module
function getMenus(moduleId: number) {
  return menus.value.filter(menu => menu.module_id === moduleId)
}

// Check if user has specific permission for menu
function hasPermission(menuId: number, permissionType: string) {
  return localPermissions.value.some(perm =>
    perm.menu_id === menuId && perm.permission_type === permissionType
  )
}

// Toggle permission for a menu
function togglePermission(menuId: number, permissionType: string, event: Event) {
  const isChecked = (event.target as HTMLInputElement).checked

  if (isChecked) {
    // Add permission if not exists
    if (!hasPermission(menuId, permissionType)) {
      localPermissions.value.push({
        user_id: props.user?.id,
        menu_id: menuId,
        permission_type: permissionType
      })
    }
  } else {
    // Remove permission
    localPermissions.value = localPermissions.value.filter(perm =>
      !(perm.menu_id === menuId && perm.permission_type === permissionType)
    )
  }
}

// Check if user has permission for module (check all menu permissions for the module)
function hasModulePermission(moduleId: number) {
  const moduleMenus = getMenus(moduleId)
  return moduleMenus.every(menu =>
    hasPermission(menu.id, 'READ')
  )
}

// Toggle module permission (toggles all menu permissions for the module)
function toggleModulePermission(moduleId: number, event: Event) {
  const isChecked = (event.target as HTMLInputElement).checked
  const moduleMenus = getMenus(moduleId)

  moduleMenus.forEach(menu => {
    if (isChecked) {
      // Add READ permission for all menus in this module
      if (!hasPermission(menu.id, 'READ')) {
        localPermissions.value.push({
          user_id: props.user?.id,
          menu_id: menu.id,
          permission_type: 'READ'
        })
      }
    } else {
      // Remove all permissions for all menus in this module
      ['READ', 'CREATE', 'UPDATE', 'DELETE'].forEach(permissionType => {
        localPermissions.value = localPermissions.value.filter(perm =>
          !(perm.menu_id === menu.id && perm.permission_type === permissionType)
        )
      })
    }
  })
}

// Save permissions
function savePermissions() {
  emit('save', localPermissions.value)
}
</script>

<style scoped>
/* Main container styling */
.permission-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Fixed footer styling */
.fixed-bottom-bar {
  position: fixed;
  bottom: 0;
  right: 0;
  width: 50%;
  background: white;
  border-top: 1px solid #e5e7eb;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  z-index: 50;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

.btn-cancel {
  background-color: #d1d5db;
  color: #374151;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-cancel:hover {
  background-color: #9ca3af;
}

.btn-save {
  background-color: #3b82f6;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-save:hover {
  background-color: #2563eb;
}

/* Ensure content area has proper scrolling */
.scrollable-content {
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 #f1f5f9;
}

.scrollable-content::-webkit-scrollbar {
  width: 8px;
}

.scrollable-content::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.scrollable-content::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 4px;
}

.scrollable-content::-webkit-scrollbar-thumb:hover {
  background-color: #94a3b8;
}

/* Ensure content doesn't overlap with fixed footer */
.content-wrapper {
  padding-bottom: 80px;
}
</style>
