<template>
  <div
  style="                                                                    font-family: 'SolaimanLipi', sans-serif;
                                                "


  class="h-full bg-white border-l border-gray-200 flex flex-col mt-10">
    <!-- Header -->
    <div class="border-b border-gray-200 px-6 py-4 flex justify-between items-center">
      <h2 class="text-xl font-bold text-gray-800">পারমিশন সেট করুন</h2>
      <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
    </div>

    <!-- Content -->
    <div class="flex-1 overflow-y-auto p-6">
      <!-- Module List -->
      <div class="space-y-6">
        <div
          v-for="module in modules"
          :key="module.id"
          class="bg-gray-50 rounded-lg p-4"
        >
          <div class="flex items-center gap-3 mb-4">
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
                  <input type="checkbox" class="mr-1" /> View
                </label>
                <label class="flex items-center">
                  <input type="checkbox" class="mr-1" /> Create
                </label>
                <label class="flex items-center">
                  <input type="checkbox" class="mr-1" /> Edit
                </label>
                <label class="flex items-center">
                  <input type="checkbox" class="mr-1" /> Delete
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="border-t border-gray-200 px-6 py-4 flex justify-end space-x-3">
      <button @click="$emit('close')" class="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded font-semibold">Cancel</button>
      <button @click="$emit('save')" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded font-semibold">Save</button>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps(['modules', 'menus', 'user', 'userPermissions'])
const emit = defineEmits(['save', 'close'])

// Use props.modules and props.menus instead of dummy data
const modules = props.modules || [
  { id: 1, name: 'Accounts', description: 'Manage financial operations', icon: 'fas fa-money-check-alt' },
  { id: 2, name: 'Publication', description: 'Publishing management', icon: 'fas fa-book-open' },
  { id: 3, name: 'Training', description: 'Staff training department', icon: 'fas fa-chalkboard-teacher' }
]

const menus = props.menus || [
  { id: 1, module_id: 1, name: 'Dashboard', description: 'Accounts overview', href: '/accounts/dashboard', icon: 'fas fa-tachometer-alt' },
  { id: 2, module_id: 1, name: 'Transactions', description: 'View and manage transactions', href: '/accounts/transactions', icon: 'fas fa-exchange-alt' },
  { id: 3, module_id: 2, name: 'Books', description: 'Published books list', href: '/publication/books', icon: 'fas fa-book' },
  { id: 4, module_id: 2, name: 'Authors', description: 'Manage authors', href: '/publication/authors', icon: 'fas fa-user-edit' },
  { id: 5, module_id: 3, name: 'Sessions', description: 'Training sessions', href: '/training/sessions', icon: 'fas fa-users' },
  { id: 6, module_id: 3, name: 'Materials', description: 'Training materials', href: '/training/materials', icon: 'fas fa-file-alt' }
]

// Filter menus for each module
function getMenus(moduleId: number) {
  return menus.filter(menu => menu.module_id === moduleId)
}
</script>

<style scoped>
/* Tailwind CSS is used for all styling. You can add custom styles if needed. */
</style>
