<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <!-- Module List -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="module in modules"
        :key="module.id"
        class="bg-white shadow rounded-lg p-5 flex flex-col gap-4"
      >
        <div class="flex items-center gap-3">
          <span v-if="module.icon" class="text-2xl">
            <!-- Use icon class name or image -->
            <i :class="module.icon"></i>
            <!-- If you want to use image, replace above line with:
                 <img :src="module.icon" alt="icon" class="w-8 h-8" />
            -->
          </span>
          <div>
            <h2 class="text-xl font-bold text-gray-800">{{ module.name }}</h2>
            <p class="text-gray-500 text-sm" v-if="module.description">{{ module.description }}</p>
          </div>
        </div>

        <!-- Menu List for this module -->
        <div class="mt-2">
          <ul class="space-y-2">
            <li
              v-for="menu in getMenus(module.id)"
              :key="menu.id"
              class="flex items-center bg-gray-100 hover:bg-gray-200 rounded px-3 py-2 transition cursor-pointer"
              @click="goTo(menu.href)"
            >
              <span v-if="menu.icon" class="mr-2 text-lg">
                <!-- Use icon class name or image -->
                <i :class="menu.icon"></i>
                <!-- Or <img :src="menu.icon" alt="icon" class="w-6 h-6" /> -->
              </span>
              <span class="font-semibold text-gray-700">{{ menu.name }}</span>
              <span class="text-xs text-gray-400 ml-2" v-if="menu.description">{{ menu.description }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Dummy data for modules
const modules = [
  { id: 1, name: 'Accounts', description: 'Manage financial operations', icon: 'fas fa-money-check-alt' },
  { id: 2, name: 'Publication', description: 'Publishing management', icon: 'fas fa-book-open' },
  { id: 3, name: 'Training', description: 'Staff training department', icon: 'fas fa-chalkboard-teacher' }
]

// Dummy data for menus
const menus = [
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

// Navigation function (replace with vue-router if needed)
function goTo(href: string) {
  window.location.href = href
}
</script>

<style scoped>
/* Tailwind CSS is used for all styling. You can add custom styles if needed. */
</style>
