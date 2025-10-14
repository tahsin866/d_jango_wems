<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="max-w-3xl mx-auto mt-8"
  >
    <div class="border border-gray-300 bg-white rounded shadow-lg">
      <!-- Box Header -->
      <div class="flex items-center justify-between px-5 py-3 border-b border-gray-200 bg-gray-100 rounded-t">
        <h3 class="font-bold text-lg text-gray-800 flex items-center">
          <i class="fas fa-chart-bar mr-2 text-indigo-500"></i>
          Monthly Sales
        </h3>
        <div class="relative">
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

      <!-- Box Body: Classic AdminLTE Bar Chart -->
      <div class="px-8 py-7 bg-white flex flex-col items-center">
        <div class="w-full max-w-xl mx-auto">
          <div class="pb-2 flex items-center justify-between">
            <span class="font-bold text-gray-600 text-sm">Sales Trend</span>
            <span class="text-xs text-gray-500">2025</span>
          </div>
          <!-- Classic Bar Chart (SVG) -->
          <div class="bg-gray-100 border border-gray-300 rounded p-4 flex items-end h-44">
            <svg viewBox="0 0 360 140" class="w-full h-full">
              <!-- Grid lines -->
              <g>
                <line v-for="i in 5" :key="i"
                  :x1="0" :x2="360"
                  :y1="i*28" :y2="i*28"
                  stroke="#e5e7eb" stroke-width="1"/>
              </g>
              <!-- Bars -->
              <g>
                <rect
                  v-for="(val, i) in series[0].data"
                  :key="i"
                  :x="i*28+14"
                  :y="140 - (val / Math.max(...series[0].data)) * 120"
                  width="18"
                  :height="(val / Math.max(...series[0].data)) * 120"
                  rx="4"
                  :fill="i === series[0].data.length-1 ? '#6366f1' : '#a5b4fc'"
                />
              </g>
              <!-- X labels -->
              <g>
                <text
                  v-for="(cat, i) in chartOptions.xaxis.categories"
                  :key="cat"
                  :x="i*28+23"
                  y="135"
                  font-size="11"
                  text-anchor="middle"
                  fill="#64748b"
                >{{ cat }}</text>
              </g>
            </svg>
          </div>
          <div class="flex justify-between pt-2 text-xs text-gray-500">
            <span>Min: {{ Math.min(...series[0].data) }}</span>
            <span>Max: {{ Math.max(...series[0].data) }}</span>
          </div>
        </div>
        <span
          class="mt-4 rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700 shadow"
        >+10%</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DropdownMenu from '../common/DropdownMenu.vue'
const menuItems = [
  { label: 'View More', onClick: () => console.log('View More clicked') },
  { label: 'Delete', onClick: () => console.log('Delete clicked') },
]

const series = ref([
  {
    name: 'Sales',
    data: [168, 385, 201, 298, 187, 195, 291, 110, 215, 390, 280, 112],
  },
])

const chartOptions = {
  xaxis: {
    categories: [
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec',
    ],
  },
}
</script>
