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
      bgLight: 'bg-indigo-50',
      text: 'text-indigo-700',
      textLight: 'text-indigo-500',
      stroke: 'stroke-indigo-500',
      fill: 'fill-indigo-500'
    },
    blue: {
      bg: 'bg-blue-500',
      bgLight: 'bg-blue-50',
      text: 'text-blue-700',
      textLight: 'text-blue-500',
      stroke: 'stroke-blue-500',
      fill: 'fill-blue-500'
    },
    slate: {
      bg: 'bg-slate-600',
      bgLight: 'bg-slate-50',
      text: 'text-slate-700',
      textLight: 'text-slate-500',
      stroke: 'stroke-slate-500',
      fill: 'fill-slate-500'
    },
    gray: {
      bg: 'bg-gray-600',
      bgLight: 'bg-gray-50',
      text: 'text-gray-700',
      textLight: 'text-gray-500',
      stroke: 'stroke-gray-500',
      fill: 'fill-gray-500'
    }
  }
  return colorMap[color] || colorMap.indigo
}
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5">
    <div
      v-for="(stat, index) in stats"
      :key="index"
      class="bg-white border border-gray-200 rounded-lg shadow-sm p-5 hover:shadow-md transition-shadow duration-200"
    >
      <!-- Header with title and info -->
      <div class="flex justify-between items-center mb-3">
        <h3 class="text-xl font-medium text-gray-500">{{ stat.title }}</h3>
        <div class="relative">
          <button
            @mouseenter="showTooltip(index)"
            @mouseleave="hideTooltip"
            @focus="showTooltip(index)"
            @blur="hideTooltip"
            class="text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-400 rounded-full p-1"
            aria-label="Help"
            type="button"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
            </svg>
          </button>
          <div
            v-if="tooltipIndex === index"
            class="absolute z-10 right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 p-2 text-xs text-gray-600"
          >
            {{ stat.tooltip }}
          </div>
        </div>
      </div>

      <!-- Main metric -->
      <div class="flex flex-col mb-3">
        <div class="flex items-baseline">
          <span class="text-2xl font-semibold text-gray-900">{{ stat.value }}</span>
          <span
            class="ml-2 px-2 py-0.5 text-xs rounded-full flex items-center"
            :class="stat.trendUp ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'"
          >
            <svg
              v-if="stat.trendUp"
              class="h-3 w-3 mr-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
            <svg
              v-else
              class="h-3 w-3 mr-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0v-8m0 8l-8-8-4 4-6-6" />
            </svg>
            {{ stat.change }}
          </span>
        </div>
        <span class="text-xs text-gray-500 mt-1">গত মাসের তুলনায়</span>
      </div>

      <!-- Chart and icon area -->
      <div class="flex items-center gap-3">
        <!-- Sparkline chart -->
        <div class="flex-1 h-12">
          <svg
            viewBox="0 0 100 30"
            class="w-full h-full overflow-visible"
            preserveAspectRatio="none"
          >
            <defs>
              <linearGradient :id="`gradient-${index}`" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" :stop-color="getColorClasses(stat.color).textLight" stop-opacity="0.2" />
                <stop offset="100%" :stop-color="getColorClasses(stat.color).textLight" stop-opacity="0" />
              </linearGradient>
            </defs>
            <!-- Area fill -->
            <path
              :d="
                `M0,30 ${
                  stat.trend
                    .map(
                      (v, i) =>
                        `L${i * (100 / (stat.trend.length - 1))},${30 -
                          ((v - Math.min(...stat.trend)) /
                            ((Math.max(...stat.trend) - Math.min(...stat.trend)) || 1)) *
                            20}`
                    )
                    .join(' ')
                } L100,30 Z`
              "
              :fill="`url(#gradient-${index})`"
            />
            <!-- Line -->
            <polyline
              :points="
                stat.trend
                  .map(
                    (v, i) =>
                      `${i * (100 / (stat.trend.length - 1))},${30 -
                        ((v - Math.min(...stat.trend)) /
                          ((Math.max(...stat.trend) - Math.min(...stat.trend)) || 1)) *
                          20}`
                  )
                  .join(' ')
              "
              fill="none"
              :stroke="getColorClasses(stat.color).stroke.replace('stroke-', '')"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <!-- Last point -->
            <circle
              :cx="100"
              :cy="
                30 -
                ((stat.trend[stat.trend.length - 1] - Math.min(...stat.trend)) /
                  ((Math.max(...stat.trend) - Math.min(...stat.trend)) || 1)) *
                  20
              "
              r="2"
              :fill="getColorClasses(stat.color).fill.replace('fill-', '')"
              stroke-width="1"
              stroke="#fff"
            />
          </svg>
        </div>
        <!-- Icon -->
        <div :class="`rounded-md p-3 ${getColorClasses(stat.color).bgLight}`">
          <i :class="`fas fa-${stat.icon} ${getColorClasses(stat.color).text}`"></i>
        </div>
      </div>
    </div>
  </div>
</template>
