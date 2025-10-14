<template>
  <div style="font-family: 'SolaimanLipi', sans-serif;" class="py-8 px-4 md:px-6 lg:px-8 bg-[#f4f6f9] min-h-screen">
    <!-- Header Dashboard Card -->
    <div class="mb-8 bg-white rounded-lg shadow-lg border border-[#d2d6de]">
      <div class="px-8 py-7 bg-gradient-to-r from-[#3c8dbc] to-[#367fa9] text-white rounded-t-lg">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <div class="bg-[#e9ecef] p-2.5 rounded mr-4">
              <svg class="w-7 h-7 text-[#3c8dbc]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div>
              <h1 class="text-2xl font-bold leading-tight">পরীক্ষা ফি সেটাপ</h1>
              <p class="text-base text-[#f9e79f]">{{ formattedTitle }}</p>
            </div>
          </div>
          <div class="hidden md:flex items-center gap-6">
            <div class="bg-[#e9ecef] px-3 py-1.5 rounded text-base border border-[#d2d6de]">
              <span class="opacity-80">তারিখ:</span> {{ getCurrentDate() }}
            </div>
            <div class="bg-[#e9ecef] px-3 py-1.5 rounded text-base border border-[#d2d6de]">
              <span class="opacity-80">সময়:</span> {{ getCurrentTime() }}
            </div>
          </div>
        </div>
      </div>
      <div class="p-6 bg-[#f4f6f9] border-b border-[#d2d6de]">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center gap-6">
            <div class="px-4 py-2 bg-white rounded shadow border border-[#d2d6de]">
              <div class="text-xs text-[#b5bbc7]">মোট মারহালা</div>
              <div class="text-base font-bold text-[#222d32]">{{ rows.length }}</div>
            </div>
            <div class="px-4 py-2 bg-white rounded shadow border border-[#d2d6de]">
              <div class="text-xs text-[#b5bbc7]">কেন্দ্রীয় পরীক্ষা</div>
              <select v-model="selectedExamSetupId" @change="onExamSetupChange"
                class="text-base font-bold text-[#222d32] bg-white border border-[#d2d6de] rounded px-2 py-1">
                <option v-for="setup in examSetupList" :key="setup.id" :value="setup.id">
                  {{ setup.exam_name }} ({{ setup.english_year }})
                </option>
              </select>
            </div>
            <div class="px-4 py-2 bg-white rounded shadow border border-[#d2d6de]">
              <div class="text-xs text-[#b5bbc7]">শিক্ষাবর্ষ</div>
              <div class="text-base font-bold text-[#222d32]">{{ examSetup?.english_year || 'N/A' }} ইসাব্দ</div>
            </div>
          </div>
          <div class="flex flex-wrap gap-3">
            <button @click="downloadExcel"
              class="flex items-center gap-2 px-4 py-2 bg-[#e9ecef] border border-[#d2d6de] rounded text-[#3c8dbc] hover:bg-[#f4f6f9] transition">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              এক্সেল ডাউনলোড
            </button>
            <button @click="toggleExpand"
              class="flex items-center gap-2 px-4 py-2 bg-[#e9ecef] border border-[#d2d6de] rounded text-[#605ca8] hover:bg-[#f4f6f9] transition">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path v-if="expandAll" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M5 15l7-7 7 7" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
              {{ expandAll ? 'সব সংকুচিত করুন' : 'সব বিস্তৃত করুন' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Fee Setup Cards -->
    <div class="grid grid-cols-1 gap-8">
      <div v-for="(row, index) in rows" :key="index"
        class="bg-white rounded shadow-lg border border-[#d2d6de] transition-all duration-300"
        :class="{ 'ring-2 ring-[#3c8dbc]': expandedCards[index] }">
        <!-- Card Header -->
        <div @click="toggleCard(index)"
          class="flex items-center justify-between px-6 py-5 cursor-pointer bg-gradient-to-r"
          :class="expandedCards[index] ? 'from-[#f4f6f9] to-[#e9ecef] border-b border-[#d2d6de]' : 'from-white to-[#f4f6f9]'">
          <div class="flex items-center gap-4">
            <div
              class="h-10 w-10 flex items-center justify-center rounded-full bg-[#3c8dbc]/10 text-[#3c8dbc] font-bold text-lg">
              {{ index + 1 }}
            </div>
            <div>
              <h3 class="text-lg font-bold text-[#222d32]">{{ row.examName }}</h3>
              <p class="text-base text-[#b5bbc7]">পরীক্ষা ফি সেটআপ</p>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <div v-if="isCardFilled(row)" class="px-3 py-1 rounded-full bg-[#dff0d8] text-[#00a65a] text-xs font-bold">
              <span class="flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                সম্পূর্ণ
              </span>
            </div>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-[#b5bbc7] transition-transform duration-300"
              :class="{ 'rotate-180': expandedCards[index] }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>

        <!-- Card Body (Collapsible) -->
        <div v-show="expandedCards[index]" class="p-7 bg-white">
          <!-- Tabs -->
          <div class="border-b border-[#d2d6de] mb-6">
            <div class="flex -mb-px">
              <button @click="activeTab[index] = 'regular'"
                class="px-4 py-2 font-semibold text-base border-b-2 transition-colors duration-200 mr-4"
                :class="activeTab[index] === 'regular' ? 'border-[#3c8dbc] text-[#3c8dbc]' : 'border-transparent text-[#b5bbc7] hover:text-[#222d32]'">
                নিয়মিত ফি
              </button>
              <button @click="activeTab[index] = 'late'"
                class="px-4 py-2 font-semibold text-base border-b-2 transition-colors duration-200"
                :class="activeTab[index] === 'late' ? 'border-[#605ca8] text-[#605ca8]' : 'border-transparent text-[#b5bbc7] hover:text-[#222d32]'">
                বিলম্ব ফি
              </button>
            </div>
          </div>
          <!-- Regular Fee Section -->
          <div v-if="activeTab[index] === 'regular'">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-7">
              <!-- Date Range -->
              <div class="bg-[#f4f6f9] p-4 rounded-lg">
                <h4 class="text-base font-semibold text-[#222d32] mb-4 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-[#3c8dbc]" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  নিবন্ধন সময়সীমা
                </h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-xs text-[#b5bbc7] mb-1">শুরুর তারিখ</label>
                    <input type="date" v-model="row.dateFrom1"
                      class="block w-full border border-[#d2d6de] rounded-md py-2 px-3 text-[#222d32] focus:outline-none focus:ring-2 focus:ring-[#3c8dbc] focus:border-[#3c8dbc] bg-white" />
                  </div>
                  <div>
                    <label class="block text-xs text-[#b5bbc7] mb-1">শেষের তারিখ</label>
                    <input type="date" v-model="row.dateTo1"
                      class="block w-full border border-[#d2d6de] rounded-md py-2 px-3 text-[#222d32] focus:outline-none focus:ring-2 focus:ring-[#3c8dbc] focus:border-[#3c8dbc] bg-white" />
                  </div>
                </div>
                <div class="text-xs text-[#b5bbc7] mt-3 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1 text-[#f39c12]" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  নিবন্ধন কাল:
                  <span class="ml-1 font-bold text-[#3c8dbc]">
                    {{ calculateDateDifference(row.dateFrom1, row.dateTo1) }}
                  </span>
                </div>
              </div>
              <!-- Fee Inputs -->
              <div class="bg-[#f4f6f9] p-4 rounded-lg">
                <h4 class="text-base font-semibold text-[#222d32] mb-4 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-[#3c8dbc]" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  নিবন্ধন ফি
                </h4>
                <div class="space-y-4">
                  <div v-for="(label, key) in regularFeeLabels" :key="key" class="flex items-center">
                    <div class="w-40 text-base text-[#222d32]">{{ label }}</div>
                    <div class="flex-1">
                      <div class="relative rounded-md">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                          <span class="text-[#b5bbc7] sm:text-base">৳</span>
                        </div>
                        <input type="number" v-model="row[key]"
                          class="block w-full pl-8 pr-3 py-2 border border-[#d2d6de] rounded-md text-[#222d32] focus:outline-none focus:ring-2 focus:ring-[#3c8dbc] focus:border-[#3c8dbc] bg-white"
                          placeholder="0.00" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Late Fee Section -->
          <div v-if="activeTab[index] === 'late'">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-7">
              <!-- Date Range -->
              <div class="bg-[#f4f6f9] p-4 rounded-lg">
                <h4 class="text-base font-semibold text-[#222d32] mb-4 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-[#f39c12]" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  বিলম্ব ফি সময়সীমা
                </h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-xs text-[#b5bbc7] mb-1">শুরুর তারিখ</label>
                    <input type="date" v-model="row.dateFrom2"
                      class="block w-full border border-[#d2d6de] rounded-md py-2 px-3 text-[#222d32] focus:outline-none focus:ring-2 focus:ring-[#f39c12] focus:border-[#f39c12] bg-white" />
                  </div>
                  <div>
                    <label class="block text-xs text-[#b5bbc7] mb-1">শেষের তারিখ</label>
                    <input type="date" v-model="row.dateTo2"
                      class="block w-full border border-[#d2d6de] rounded-md py-2 px-3 text-[#222d32] focus:outline-none focus:ring-2 focus:ring-[#f39c12] focus:border-[#f39c12] bg-white" />
                  </div>
                </div>
                <div class="text-xs text-[#b5bbc7] mt-3 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1 text-[#f39c12]" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  বিলম্ব কাল:
                  <span class="ml-1 font-bold text-[#f39c12]">
                    {{ calculateDateDifference(row.dateFrom2, row.dateTo2) }}
                  </span>
                </div>
              </div>
              <!-- Fee Inputs -->
              <div class="bg-[#f4f6f9] p-4 rounded-lg">
                <h4 class="text-base font-semibold text-[#222d32] mb-4 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-[#f39c12]" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  বিলম্ব ফি
                </h4>
                <div class="space-y-4">
                  <div v-for="(label, key) in lateFeeLabels" :key="key" class="flex items-center">
                    <div class="w-40 text-base text-[#222d32]">{{ label }}</div>
                    <div class="flex-1">
                      <div class="relative rounded-md">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                          <span class="text-[#b5bbc7] sm:text-base">৳</span>
                        </div>
                        <input type="number" v-model="row[key]"
                          class="block w-full pl-8 pr-3 py-2 border border-[#d2d6de] rounded-md text-[#222d32] focus:outline-none focus:ring-2 focus:ring-[#f39c12] focus:border-[#f39c12] bg-white"
                          placeholder="0.00" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Summary and Extra Actions -->
          <div class="mt-7 p-4 bg-[#f4f6f9] rounded-lg">
            <div class="flex flex-wrap items-center justify-between gap-4">
              <div>
                <h4 class="text-base font-semibold text-[#222d32] flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-[#605ca8]" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  ফি সারসংক্ষেপ
                </h4>
                <div class="mt-2 grid grid-cols-2 gap-x-8 gap-y-1 text-base">
                  <div class="text-[#b5bbc7]">নিয়মিত ফি:</div>
                  <div class="text-[#222d32] font-bold">৳ {{ formatAmount(row.fee1) }}</div>
                  <div class="text-[#b5bbc7]">বিলম্ব ফি:</div>
                  <div class="text-[#222d32] font-bold">৳ {{ formatAmount(row.fee2) }}</div>
                </div>
              </div>
              <div class="flex gap-2">
                <button @click="copyToAllCards(row)"
                  class="inline-flex items-center px-3 py-1.5 bg-[#e9ecef] border border-[#d2d6de] rounded text-[#367fa9] hover:bg-[#f4f6f9] transition text-base">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  সব কার্ডে কপি করুন
                </button>
                <button @click="resetSingleCard(index)"
                  class="inline-flex items-center px-3 py-1.5 bg-[#f2dede] border border-[#ebcccc] rounded text-[#dd4b39] hover:bg-[#f9e7e7] transition text-base">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  রিসেট করুন
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Submit Button - Fixed at Bottom -->
    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-[#d2d6de] p-4 flex justify-end shadow-lg z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full flex justify-between items-center">
        <div class="flex items-center">
          <div class="bg-[#e9ecef] text-[#367fa9] px-3 py-1 rounded-full text-base flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            সম্পূর্ণ করা হয়েছে:
            <span class="ml-1.5 font-bold">{{ filledCards() }} / {{ rows.length }}</span>
          </div>
        </div>
        <div class="flex gap-3">
          <button @click="resetForm"
            class="inline-flex items-center px-4 py-2.5 bg-white border border-[#d2d6de] rounded text-[#222d32] hover:bg-[#f4f6f9] transition">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            সব রিসেট করুন
          </button>
          <button @click="submitWithValidation"
            class="inline-flex items-center px-4 py-2.5 bg-gradient-to-r from-[#3c8dbc] to-[#367fa9] border border-transparent rounded text-white hover:from-[#367fa9] hover:to-[#3c8dbc] focus:ring-2 focus:ring-offset-2 focus:ring-[#3c8dbc] transition shadow-lg font-bold">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            সংরক্ষণ করুন
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'

const regularFeeLabels = {
  fee1: 'নিয়মিত ফি',
  invest1Men: 'অনিয়মিত (যেমনি)',
  invest1Madan: 'অনিয়মিত (মানোন্নয়ন)',
  invest1Others: 'অনিয়মিত (অন্যান্য)'
}
const lateFeeLabels = {
  fee2: 'নিয়মিত ফি',
  invest2Men: 'অনিয়মিত (যেমনি)',
  invest2Madan: 'অনিয়মিত (মানোন্নয়ন)',
  invest2Others: 'অনিয়মিত (অন্যান্য)'
}

const examSetupList = ref([])
const selectedExamSetupId = ref(null)
const examSetup = ref(null)
const rows = ref([])
const marhalaNames = ref([])

const expandedCards = ref({ 0: true })
const activeTab = ref({ 0: 'regular' })
const expandAll = ref(false)

const formattedTitle = computed(() => {
  if (!examSetup.value) return ''
  return `${examSetup.value.exam_name} ${examSetup.value.arabic_year} হিজরি/${examSetup.value.bangla_year} বঙ্গাব্দ/${examSetup.value.english_year} ইসাব্দ`
})

const getCurrentDate = () => {
  const date = new Date()
  return date.toLocaleDateString('bn-BD', { year: 'numeric', month: 'long', day: 'numeric' })
}

const getCurrentTime = () => {
  const date = new Date()
  return date.toLocaleTimeString('bn-BD', { hour: '2-digit', minute: '2-digit' })
}

function formatAmount(amount) {
  if (!amount) return '0'
  return new Intl.NumberFormat('bn-BD').format(amount)
}

function calculateDateDifference(start, end) {
  if (!start || !end) return 'নির্ধারিত নয়'
  const startDate = new Date(start)
  const endDate = new Date(end)
  if (isNaN(startDate.getTime()) || isNaN(endDate.getTime())) return 'অবৈধ তারিখ'
  if (endDate < startDate) return 'অবৈধ সময়কাল'
  const diffTime = Math.abs(endDate.getTime() - startDate.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return `${diffDays} দিন`
}

function isCardFilled(row) {
  return !!(row.dateFrom1 && row.dateTo1 && row.fee1 &&
            row.dateFrom2 && row.dateTo2 && row.fee2)
}

function filledCards() {
  return rows.value.filter(row => isCardFilled(row)).length
}

function toggleCard(index) {
  expandedCards.value[index] = !expandedCards.value[index]
  if (!activeTab.value[index]) {
    activeTab.value[index] = 'regular'
  }
}

function toggleExpand() {
  expandAll.value = !expandAll.value
  rows.value.forEach((_, index) => {
    expandedCards.value[index] = expandAll.value
    if (expandAll.value && !activeTab.value[index]) {
      activeTab.value[index] = 'regular'
    }
  })
}

function copyToAllCards(sourceRow) {
  if (confirm('আপনি কি নিশ্চিত যে এই কার্ডের ডাটা সমস্ত কার্ডে কপি করতে চান?')) {
    rows.value = rows.value.map(row => ({
      ...row,
      dateFrom1: sourceRow.dateFrom1,
      dateTo1: sourceRow.dateTo1,
      fee1: sourceRow.fee1,
      invest1Men: sourceRow.invest1Men,
      invest1Madan: sourceRow.invest1Madan,
      invest1Others: sourceRow.invest1Others,
      dateFrom2: sourceRow.dateFrom2,
      dateTo2: sourceRow.dateTo2,
      fee2: sourceRow.fee2,
      invest2Men: sourceRow.invest2Men,
      invest2Madan: sourceRow.invest2Madan,
      invest2Others: sourceRow.invest2Others
    }))
  }
}

function resetSingleCard(index) {
  if (confirm('আপনি কি নিশ্চিত যে এই কার্ডের ডাটা রিসেট করতে চান?')) {
    rows.value[index] = {
      ...rows.value[index],
      dateFrom1: null, dateTo1: null, fee1: null,
      invest1Men: null, invest1Madan: null, invest1Others: null,
      dateFrom2: null, dateTo2: null, fee2: null,
      invest2Men: null, invest2Madan: null, invest2Others: null
    }
  }
}

function resetForm() {
  if (confirm('আপনি কি নিশ্চিত যে সমস্ত ডাটা রিসেট করতে চান?')) {
    rows.value = rows.value.map(row => ({
      ...row,
      dateFrom1: null, dateTo1: null, fee1: null,
      invest1Men: null, invest1Madan: null, invest1Others: null,
      dateFrom2: null, dateTo2: null, fee2: null,
      invest2Men: null, invest2Madan: null, invest2Others: null
    }))
    expandedCards.value = { 0: true }
    activeTab.value = { 0: 'regular' }
  }
}

async function fetchExamSetupList() {
  const response = await axios.get('http://127.0.0.1:8000/api/central-exam/exam-setups/list/')
  if (response.data && Array.isArray(response.data)) {
    examSetupList.value = response.data
    if (examSetupList.value.length > 0) {
      selectedExamSetupId.value = examSetupList.value[0].id
      examSetup.value = examSetupList.value[0]
    }
  }
}

function onExamSetupChange() {
  const found = examSetupList.value.find(s => s.id === selectedExamSetupId.value)
  examSetup.value = found || null
}

const fetchMarhalaNames = async () => {
  const response = await axios.get('http://127.0.0.1:8000/api/marhalas/')
  if (response.data.success) {
    const marhalas = response.data.data
    marhalaNames.value = marhalas.map(m => m.marhala_name_bn)
    rows.value = marhalas.map(m => ({
      examName: m.marhala_name_bn,
      marhala_id: m.id,
      dateFrom1: null, dateTo1: null, fee1: null,
      invest1Men: null, invest1Madan: null, invest1Others: null,
      dateFrom2: null, dateTo2: null, fee2: null,
      invest2Men: null, invest2Madan: null, invest2Others: null
    }))
    expandedCards.value = { 0: true }
    activeTab.value = { 0: 'regular' }
  }
}

async function submit() {
  if (!selectedExamSetupId.value) {
    alert('কোনো কেন্দ্রীয় পরীক্ষা পাওয়া যায়নি!')
    return
  }

  const fees = rows.value.map(row => ({
    exam_setup: selectedExamSetupId.value,
    marhala: row.marhala_id,
    reg_date_from: row.dateFrom1,
    reg_date_to: row.dateTo1,
    reg_regular_fee: row.fee1,
    reg_irregular_jemni: row.invest1Men,
    reg_irregular_manonnoyon: row.invest1Madan,
    reg_irregular_others: row.invest1Others,
    late_date_from: row.dateFrom2,
    late_date_to: row.dateTo2,
    late_regular_fee: row.fee2,
    late_irregular_jemni: row.invest2Men,
    late_irregular_manonnoyon: row.invest2Madan,
    late_irregular_others: row.invest2Others
  }))

  try {
    const response = await axios.post(
      'http://127.0.0.1:8000/api/central-exam/exam-fees/bulk-create/',
      { fees }
    )

    if (response.data.success) {
      alert(`সফলভাবে সংরক্ষণ হয়েছে! ${response.data.message}`)
    } else {
      let errorMessage = 'সংরক্ষণে সমস্যা হয়েছে:\n\n'
      if (response.data.errors && Array.isArray(response.data.errors)) {
        response.data.errors.forEach(error => {
          errorMessage += `আইটেম ${error.index + 1}: `
          if (error.errors) {
            Object.keys(error.errors).forEach(field => {
              errorMessage += `${field}: ${error.errors[field].join(', ')}\n`
            })
          }
        })
      }
      alert(errorMessage)
    }
  } catch (error) {
    if (error.response && error.response.data) {
      alert(`API Error: ${error.response.data.message || 'অজানা সমস্যা'}`)
    } else {
      alert('নেটওয়ার্ক সমস্যা! আবার চেষ্টা করুন।')
    }
  }
}

function validateBeforeSubmit() {
  const errors = []

  rows.value.forEach((row, index) => {
    const rowErrors = []

    if (!row.marhala_id) {
      rowErrors.push('মারহালা আইডি নেই')
    }

    if (row.dateFrom1 && row.dateTo1 && new Date(row.dateFrom1) > new Date(row.dateTo1)) {
      rowErrors.push('নিয়মিত ফি এর শুরুর তারিখ শেষের তারিখের চেয়ে বড় হতে পারে না')
    }

    if (row.dateFrom2 && row.dateTo2 && new Date(row.dateFrom2) > new Date(row.dateTo2)) {
      rowErrors.push('বিলম্ব ফি এর শুরুর তারিখ শেষের তারিখের চেয়ে বড় হতে পারে না')
    }

    if (rowErrors.length > 0) {
      errors.push(`মারহালা ${index + 1} (${row.examName}): ${rowErrors.join(', ')}`)
    }
  })

  return errors
}

async function submitWithValidation() {
  const validationErrors = validateBeforeSubmit()

  if (validationErrors.length > 0) {
    console.error('Validation errors:', validationErrors)
    return
  }

  await submit()
}

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/central-exam/exam-setups/latest/')
    if (response.data && response.data.success && response.data.data && response.data.data.id) {
      selectedExamSetupId.value = response.data.data.id
    } else {
      alert('কোনো কেন্দ্রীয় পরীক্ষা পাওয়া যায়নি!')
    }
  } catch  {
    alert('সর্বশেষ কেন্দ্রীয় পরীক্ষা আইডি ফেচ করতে সমস্যা হয়েছে!')
  }
})

onMounted(() => {
  expandedCards.value = { 0: true }
  activeTab.value = { 0: 'regular' }
  fetchExamSetupList()
  fetchMarhalaNames()
})

watch(selectedExamSetupId, () => {
  onExamSetupChange()
})

function downloadExcel() {
  alert('এক্সেল ডাউনলোড ফাংশন এখানে আসবে।')
}
</script>
