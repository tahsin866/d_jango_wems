<script setup>
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'

// Data structure, no TypeScript
const examAnalytics = ref({
  passRate: '৮৫.৭%',
  averageGrade: '৩.৮৫',
  topSubject: 'হাদীস শরীফ',
  lowestSubject: 'আরবি ভাষা'
})

// Date and user information
const dateTime = '2025-08-07 06:47:54'
const userName = 'tahsin866'

onMounted(() => {
  // Pass Rate Chart
  const passRateCtx = document.getElementById('passRateChart')
  if (passRateCtx) {
    new Chart(passRateCtx, {
      type: 'doughnut',
      data: {
        labels: ['পাস', 'ফেল'],
        datasets: [{
          data: [85.7, 14.3],
          backgroundColor: ['#4f46e5', '#e2e8f0'],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '75%',
        plugins: {
          legend: { display: false }
        }
      }
    })
  }

  // Subject Performance Chart
  const subjectCtx = document.getElementById('subjectPerformanceChart')
  if (subjectCtx) {
    new Chart(subjectCtx, {
      type: 'bar',
      data: {
        labels: ['হাদীস', 'ফিকাহ', 'তাফসীর', 'আরবি', 'ইসলামি ইতিহাস'],
        datasets: [{
          label: 'গড় নম্বর',
          data: [85, 78, 72, 65, 80],
          backgroundColor: [
            '#4f46e5', '#3b82f6', '#6366f1', '#8b5cf6', '#2563eb'
          ],
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            grid: {
              color: '#f1f5f9'
            }
          },
          x: {
            grid: {
              display: false
            }
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    })
  }

  // Yearly Trend Chart
  const trendCtx = document.getElementById('yearlyTrendChart')
  if (trendCtx) {
    new Chart(trendCtx, {
      type: 'line',
      data: {
        labels: ['১৪৪২', '১৪৪৩', '১৪৪৪', '১৪৪৫', '১৪৪৬'],
        datasets: [{
          label: 'পাস রেট',
          data: [78, 80, 82, 84, 85.7],
          borderColor: '#4f46e5',
          backgroundColor: 'rgba(79, 70, 229, 0.1)',
          tension: 0.3,
          fill: true,
          pointRadius: 4,
          pointBackgroundColor: '#4f46e5'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: false,
            min: 70,
            max: 100,
            grid: {
              color: '#f1f5f9'
            }
          },
          x: {
            grid: {
              display: false
            }
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    })
  }
})
</script>

<template>
  <div class="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden mb-8">
    <!-- Header with metadata -->
    <div class="border-b border-gray-200 bg-gray-50 px-6 py-4">
      <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3">
        <div>
          <h3 class="text-lg font-medium text-gray-900 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
            </svg>
            পরীক্ষার বিশ্লেষণ (Analytics)
          </h3>
          <p class="text-sm text-gray-500 mt-1">সমস্ত পরীক্ষার ডেটা ও ট্রেন্ড</p>
        </div>
        <div class="flex items-center text-sm text-gray-500 gap-4">
          <div class="flex items-center gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            {{ dateTime }}
          </div>
          <div class="flex items-center gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            {{ userName }}
          </div>
        </div>
      </div>
    </div>

    <div class="p-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Key Metrics -->
        <div class="bg-white rounded-lg border border-gray-200 shadow-sm p-5">
          <h4 class="text-sm font-medium text-gray-900 mb-4 pb-2 border-b border-gray-200">মূল পরিসংখ্যান</h4>
          <div class="space-y-3 w-full">
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">পাস রেট</span>
              <span class="text-sm font-semibold text-gray-900 bg-indigo-50 px-2 py-0.5 rounded">{{ examAnalytics.passRate }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">গড় গ্রেড</span>
              <span class="text-sm font-semibold text-gray-900 bg-blue-50 px-2 py-0.5 rounded">{{ examAnalytics.averageGrade }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">সর্বোচ্চ বিষয়</span>
              <span class="text-sm font-semibold text-gray-900 bg-green-50 px-2 py-0.5 rounded">{{ examAnalytics.topSubject }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">সর্বনিম্ন বিষয়</span>
              <span class="text-sm font-semibold text-gray-900 bg-red-50 px-2 py-0.5 rounded">{{ examAnalytics.lowestSubject }}</span>
            </div>
          </div>
          <div class="mt-6 h-40 w-full relative">
            <canvas id="passRateChart"></canvas>
            <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <span class="text-2xl font-bold text-indigo-600">{{ examAnalytics.passRate }}</span>
              <span class="text-xs text-gray-600">পাস রেট</span>
            </div>
          </div>
        </div>

        <!-- Subject Performance -->
        <div class="bg-white rounded-lg border border-gray-200 shadow-sm p-5">
          <h4 class="text-sm font-medium text-gray-900 mb-4 pb-2 border-b border-gray-200">বিষয়ভিত্তিক পারফরম্যান্স</h4>
          <div class="h-56">
            <canvas id="subjectPerformanceChart"></canvas>
          </div>
        </div>

        <!-- Yearly Trend -->
        <div class="bg-white rounded-lg border border-gray-200 shadow-sm p-5">
          <h4 class="text-sm font-medium text-gray-900 mb-4 pb-2 border-b border-gray-200">বার্ষিক ট্রেন্ড</h4>
          <div class="h-56">
            <canvas id="yearlyTrendChart"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer with metadata -->
    <div class="border-t border-gray-200 bg-gray-50 px-6 py-3">
      <div class="flex justify-between items-center text-sm text-gray-500">
        <span>সর্বশেষ আপডেট: ২৬ জুন, ২০২৫</span>
        <div class="flex items-center gap-2">
          <button class="inline-flex items-center text-indigo-600 hover:text-indigo-800 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            ডাউনলোড
          </button>
          <button class="inline-flex items-center text-indigo-600 hover:text-indigo-800 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" />
            </svg>
            প্রিন্ট করুন
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
