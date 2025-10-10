<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="max-w-4xl mx-auto mt-8"
  >
    <!-- AdminLTE Box -->
    <div class="rounded border border-gray-300 bg-white shadow-lg">
      <!-- Box Header -->
      <div class="flex items-center justify-between px-5 py-3 box-header border-b border-gray-200 bg-gray-100 rounded-t">
        <div>
          <h3 class="font-bold text-lg text-gray-800 flex items-center">
            <i class="fas fa-bullseye mr-2 text-indigo-500"></i>
            Monthly Target
          </h3>
          <p class="mt-1 text-gray-600 text-sm">
            Target you’ve set for each month
          </p>
        </div>
        <div>
          <DropdownMenu :menu-items="menuItems">
            <template #icon>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none"
                xmlns="http://www.w3.org/2000/svg"
                class="text-gray-400 hover:text-gray-700"
              >
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M10.2441 6C10.2441 5.0335 11.0276 4.25 11.9941 4.25H12.0041C12.9706 4.25 13.7541 5.0335 13.7541 6C13.7541 6.9665 12.9706 7.75 12.0041 7.75H11.9941C11.0276 7.75 10.2441 6.9665 10.2441 6ZM10.2441 18C10.2441 17.0335 11.0276 16.25 11.9941 16.25H12.0041C12.9706 16.25 13.7541 17.0335 13.7541 18C13.7541 18.9665 12.9706 19.75 12.0041 19.75H11.9941C11.0276 19.75 10.2441 18.9665 10.2441 18ZM11.9941 10.25C11.0276 10.25 10.2441 11.0335 10.2441 12C10.2441 12.9665 11.0276 13.75 11.9941 13.75H12.0041C12.9706 13.75 13.7541 12.9665 13.7541 12C13.7541 11.0335 12.9706 10.25 12.0041 10.25H11.9941Z"
                  fill="currentColor"
                />
              </svg>
            </template>
          </DropdownMenu>
        </div>
      </div>

      <!-- Box Body: Classic Progress Bar (AdminLTE style) -->
      <div class="px-8 py-7 bg-white flex flex-col items-center justify-center">
        <div class="w-full max-w-xs my-6">
          <div class="mb-3 flex justify-between items-center">
            <span class="font-bold text-gray-600 text-sm">Progress</span>
            <span class="font-bold text-indigo-700 text-lg">{{ series[0] }}%</span>
          </div>
          <div class="h-8 rounded bg-gray-100 border border-gray-300 shadow-inner flex items-center">
            <div
              class="h-8 rounded-l bg-indigo-500 transition-all duration-500 flex items-center justify-end"
              :style="{ width: series[0] + '%' }"
            >
              <span
                class="pr-2 text-white font-bold text-base"
                v-if="series[0] > 15"
              >
                {{ series[0] }}%
              </span>
            </div>
          </div>
          <div class="flex justify-between mt-2 text-xs text-gray-500">
            <span>0%</span>
            <span>100%</span>
          </div>
        </div>
        <span
          class="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700 shadow"
        >+10%</span>
        <p class="mx-auto mt-6 w-full max-w-md text-center text-sm text-gray-700">
          You earn $3287 today, it's higher than last month. Keep up your good work!
        </p>
      </div>

      <!-- Box Footer (Stats) -->
      <div class="flex items-center justify-center gap-7 px-8 py-5 bg-gray-50 border-t border-gray-200 rounded-b">
        <!-- Target -->
        <div class="flex flex-col items-center">
          <p class="mb-1 text-gray-500 text-xs">Target</p>
          <p class="flex items-center gap-1 text-lg font-bold text-gray-800">
            $20K
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M7.26816 13.6632C7.4056 13.8192 7.60686 13.9176 7.8311 13.9176C7.83148 13.9176 7.83187 13.9176 7.83226 13.9176C8.02445 13.9178 8.21671 13.8447 8.36339 13.6981L12.3635 9.70076C12.6565 9.40797 12.6567 8.9331 12.3639 8.6401C12.0711 8.34711 11.5962 8.34694 11.3032 8.63973L8.5811 11.36L8.5811 2.5C8.5811 2.08579 8.24531 1.75 7.8311 1.75C7.41688 1.75 7.0811 2.08579 7.0811 2.5L7.0811 11.3556L4.36354 8.63975C4.07055 8.34695 3.59568 8.3471 3.30288 8.64009C3.01008 8.93307 3.01023 9.40794 3.30321 9.70075L7.26816 13.6632Z"
                fill="#D92D20"
              />
            </svg>
          </p>
        </div>
        <div class="h-8 w-px bg-gray-300"></div>
        <!-- Revenue -->
        <div class="flex flex-col items-center">
          <p class="mb-1 text-gray-500 text-xs">Revenue</p>
          <p class="flex items-center gap-1 text-lg font-bold text-gray-800">
            $20K
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M7.60141 2.33683C7.73885 2.18084 7.9401 2.08243 8.16435 2.08243C8.16475 2.08243 8.16516 2.08243 8.16556 2.08243C8.35773 2.08219 8.54998 2.15535 8.69664 2.30191L12.6968 6.29924C12.9898 6.59203 12.9899 7.0669 12.6971 7.3599C12.4044 7.6529 11.9295 7.65306 11.6365 7.36027L8.91435 4.64004L8.91435 13.5C8.91435 13.9142 8.57856 14.25 8.16435 14.25C7.75013 14.25 7.41435 13.9142 7.41435 13.5L7.41435 4.64442L4.69679 7.36025C4.4038 7.65305 3.92893 7.6529 3.63613 7.35992C3.34333 7.06693 3.34348 6.59206 3.63646 6.29926L7.60141 2.33683Z"
                fill="#039855"
              />
            </svg>
          </p>
        </div>
        <div class="h-8 w-px bg-gray-300"></div>
        <!-- Today -->
        <div class="flex flex-col items-center">
          <p class="mb-1 text-gray-500 text-xs">Today</p>
          <p class="flex items-center gap-1 text-lg font-bold text-gray-800">
            $20K
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M7.60141 2.33683C7.73885 2.18084 7.9401 2.08243 8.16435 2.08243C8.16475 2.08243 8.16516 2.08243 8.16556 2.08243C8.35773 2.08219 8.54998 2.15535 8.69664 2.30191L12.6968 6.29924C12.9898 6.59203 12.9899 7.0669 12.6971 7.3599C12.4044 7.6529 11.9295 7.65306 11.6365 7.36027L8.91435 4.64004L8.91435 13.5C8.91435 13.9142 8.57856 14.25 8.16435 14.25C7.75013 14.25 7.41435 13.9142 7.41435 13.5L7.41435 4.64442L4.69679 7.36025C4.4038 7.65305 3.92893 7.6529 3.63613 7.35992C3.34333 7.06693 3.34348 6.59206 3.63646 6.29926L7.60141 2.33683Z"
                fill="#039855"
              />
            </svg>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import DropdownMenu from '../common/DropdownMenu.vue'
const menuItems = [
  { label: 'View More', onClick: () => console.log('View More clicked') },
  { label: 'Delete', onClick: () => console.log('Delete clicked') },
]
const props = defineProps({
  value: {
    type: Number,
    default: 75.55,
  },
})
const series = computed(() => [props.value])
// VueApexCharts import/remove: Not needed for classic progress bar!
</script>
