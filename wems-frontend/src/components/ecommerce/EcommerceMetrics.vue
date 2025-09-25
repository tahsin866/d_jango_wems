<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-7 mt-8"
  >
    <div
      v-for="(stat, index) in stats"
      :key="index"
      class="border border-gray-300 rounded shadow-lg bg-white p-0"
    >
      <!-- Classic AdminLTE Box Header -->
      <div class="flex items-center justify-between px-5 py-3 bg-gray-100 border-b border-gray-200 rounded-t">
        <h3 class="font-bold text-base text-gray-800 flex items-center tracking-tight">
          <i :class="`fas fa-${stat.icon} mr-2 text-${stat.color}-500`"></i>
          {{ stat.title }}
        </h3>
        <div class="relative">
          <button
            @mouseenter="showTooltip(index)"
            @mouseleave="hideTooltip"
            @focus="showTooltip(index)"
            @blur="hideTooltip"
            class="text-gray-400 hover:text-gray-600 focus:outline-none rounded-full p-1"
            aria-label="Help"
            type="button"
          >
            <i class="fas fa-question-circle"></i>
          </button>
          <div
            v-if="tooltipIndex === index"
            class="absolute z-10 right-0 mt-2 w-48 rounded bg-gray-900 text-gray-50 shadow-lg p-2 text-xs"
          >
            {{ stat.tooltip }}
          </div>
        </div>
      </div>

      <!-- Box Body: Main metric and change -->
      <div class="px-5 pt-5 pb-2 flex flex-col items-center">
        <span class="text-2xl font-extrabold text-gray-900">{{ stat.value }}</span>
        <span
          class="mt-2 px-2 py-0.5 text-xs rounded font-bold inline-flex items-center"
          :class="stat.trendUp ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
        >
          <i
            :class="stat.trendUp ? 'fas fa-arrow-up mr-1 text-green-600' : 'fas fa-arrow-down mr-1 text-red-600'"
          ></i>
          {{ stat.change }}
        </span>
        <span class="text-xs text-gray-500 mt-1">গত মাসের তুলনায়</span>
      </div>

      <!-- Classic AdminLTE Chart: Vertical Bar Chart (instead of sparkline/progress bar) -->
      <div class="px-5 pb-4">
        <div class="mb-1 flex justify-between items-center">
          <span class="font-bold text-xs text-gray-600">Trend</span>
          <span class="font-bold text-xs text-gray-800">
            {{ Math.round((stat.trend[stat.trend.length - 1] / Math.max(...stat.trend)) * 100) }}%
          </span>
        </div>
        <!-- Classic vertical bar chart -->
        <div class="flex items-end gap-1 h-20 w-full py-2">
          <div
            v-for="(v, i) in stat.trend"
            :key="i"
            class="flex-1 flex justify-center"
          >
            <div
              class="w-2 rounded-t"
              :style="{
                height: Math.max((v / Math.max(...stat.trend)) * 70, 4) + 'px',
                background: i === stat.trend.length - 1
                  ? 'linear-gradient(180deg,' + getColorClasses(stat.color).bgLight.replace('bg-', '') + ',#6366f1)'
                  : getColorClasses(stat.color).bgLight.replace('bg-', ''),
              }"
            ></div>
          </div>
        </div>
        <div class="flex justify-between mt-1 text-xs text-gray-500">
          <span>Min: {{ Math.min(...stat.trend) }}</span>
          <span>Max: {{ Math.max(...stat.trend) }}</span>
        </div>
      </div>

      <!-- Classic AdminLTE Box Footer -->
      <div class="bg-gray-50 border-t border-gray-200 rounded-b px-5 py-2 flex items-center justify-between">
        <span class="text-xs text-gray-600">
          <i :class="`fas fa-${stat.icon} mr-1 text-${stat.color}-400`"></i>
          {{ stat.title }}
        </span>
        <span class="text-xs text-gray-600">Info</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// Fake analytics chart data (sparkline)
function getRandomData(len = 20, base = 1000, variation = 80): number[] {
  let val = base
  return Array.from({ length: len }, () => {
    val += Math.floor(Math.random() * variation - variation / 2)
    return Math.max(val, 0)
  })
}

type Stat = {
  title: string
  value: string
  change: string
  icon: string
  color: 'indigo' | 'blue' | 'slate' | 'gray'
  trend: number[]
  trendUp: boolean
  tooltip: string
}

const stats = ref<Stat[]>([
  {
    title: 'মোট মাদরাসা',
    value: '১৫,৪৮৯',
    change: '+৩.৫%',
    icon: 'building',
    color: 'indigo',
    trend: getRandomData(20, 15000, 200),
    trendUp: true,
    tooltip: 'দেশব্যাপী অনুমোদিত কওমী মাদরাসা'
  },
  {
    title: 'মোট ছাত্র',
    value: '৮৭,৩৪৫',
    change: '+৫.২%',
    icon: 'users',
    color: 'blue',
    trend: getRandomData(20, 80000, 800),
    trendUp: true,
    tooltip: 'সর্বমোট ছাত্র সংখ্যা'
  },
  {
    title: 'পরীক্ষার্থী',
    value: '৭৫,৬৭৮',
    change: '+৪.৮%',
    icon: 'user-graduate',
    color: 'slate',
    trend: getRandomData(20, 70000, 600),
    trendUp: true,
    tooltip: 'চলতি বছর পরীক্ষার্থী সংখ্যা'
  },
  {
    title: 'মোট মারকায',
    value: '৩৪৫',
    change: '+২.১%',
    icon: 'landmark',
    color: 'gray',
    trend: getRandomData(20, 320, 8),
    trendUp: true,
    tooltip: 'বিভিন্ন বিভাগীয় মারকাযের সংখ্যা'
  }
])

// Tooltip visibility
const tooltipIndex = ref<number | null>(null)
const showTooltip = (idx: number) => (tooltipIndex.value = idx)
const hideTooltip = () => (tooltipIndex.value = null)

const getColorClasses = (color: Stat['color']) => {
  const colorMap = {
    indigo: {
      bg: 'bg-indigo-500',
      bgLight: 'bg-indigo-300',
      text: 'text-indigo-700',
      textLight: 'text-indigo-500',
      stroke: 'stroke-indigo-500',
      fill: 'fill-indigo-500'
    },
    blue: {
      bg: 'bg-blue-500',
      bgLight: 'bg-blue-300',
      text: 'text-blue-700',
      textLight: 'text-blue-500',
      stroke: 'stroke-blue-500',
      fill: 'fill-blue-500'
    },
    slate: {
      bg: 'bg-slate-600',
      bgLight: 'bg-slate-300',
      text: 'text-slate-700',
      textLight: 'text-slate-500',
      stroke: 'stroke-slate-500',
      fill: 'fill-slate-500'
    },
    gray: {
      bg: 'bg-gray-600',
      bgLight: 'bg-gray-300',
      text: 'text-gray-700',
      textLight: 'text-gray-500',
      stroke: 'stroke-gray-500',
      fill: 'fill-gray-500'
    }
  }
  return colorMap[color] || colorMap.indigo
}
</script>
