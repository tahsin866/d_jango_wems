<script setup>
import { ref, computed } from "vue"

// Notice Data
const notices = ref([
  {
    id: 1,
    title: "দাওরায়ে হাদীস পরীক্ষার সময়সূচী প্রকাশিত হয়েছে",
    date: "১০ জুলাই, ২০২৩",
    priority: "high",
    content:
      "আগামী ১৫ আগস্ট থেকে দাওরায়ে হাদীস পরীক্ষা শুরু হবে। সকল মাদরাসাকে প্রস্তুতি নিতে অনুরোধ করা হচ্ছে।",
    attachment: "exam_schedule_2023.pdf"
  },
  {
    id: 2,
    title: "মারকাজ পরিদর্শন সংক্রান্ত বিজ্ঞপ্তি",
    date: "০৫ জুলাই, ২০২৩",
    priority: "medium",
    content:
      "আগামী মাসে সকল মারকাজ পরিদর্শন করা হবে। প্রয়োজনীয় ডকুমেন্ট প্রস্তুত রাখার জন্য অনুরোধ করা হচ্ছে।",
    attachment: null
  },
  {
    id: 3,
    title: "নতুন পাঠ্যক্রম সংক্রান্ত সভা",
    date: "০১ জুলাই, ২০২৩",
    priority: "low",
    content:
      "আগামী ২০ জুলাই সকল মাদরাসার প্রধান শিক্ষকদের উপস্থিতিতে নতুন পাঠ্যক্রম নিয়ে আলোচনা সভা অনুষ্ঠিত হবে।",
    attachment: null
  }
])

const upcomingExams = ref([
  {
    id: 1,
    name: "দাওরায়ে হাদীস",
    date: "১৫ আগস্ট, ২০২৩",
    registeredStudents: "১২,৫৬৭",
    centers: "১৫৬",
    status: "upcoming",
    statusText: "আসন্ন",
    color: "bg-green-100 text-green-800"
  },
  {
    id: 2,
    name: "জামাত-ই-মুতাওয়াসসিতাহ",
    date: "২০ আগস্ট, ২০২৩",
    registeredStudents: "২৩,৪৫৬",
    centers: "২৩৪",
    status: "upcoming",
    statusText: "আসন্ন",
    color: "bg-green-100 text-green-800"
  },
  {
    id: 3,
    name: "জামাত-ই-সানাবিয়া",
    date: "২৫ আগস্ট, ২০২৩",
    registeredStudents: "৩৪,৫৬৭",
    centers: "২৮৯",
    status: "upcoming",
    statusText: "আসন্ন",
    color: "bg-green-100 text-green-800"
  },
  {
    id: 4,
    name: "জামাত-ই-আলিয়া",
    date: "০১ সেপ্টেম্বর, ২০২৩",
    registeredStudents: "১৮,৯৮৭",
    centers: "১৭৮",
    status: "upcoming",
    statusText: "আসন্ন",
    color: "bg-green-100 text-green-800"
  }
])

const selectedNotice = ref(null)
const showNoticeModal = ref(false)

function showNoticeDetails(notice) {
  selectedNotice.value = notice
  showNoticeModal.value = true
}

function closeNoticeDetails() {
  setTimeout(() => {
    selectedNotice.value = null
  }, 200)
  showNoticeModal.value = false
}

function noticePriorityBadge(priority) {
  switch (priority) {
    case "high":
      return "bg-red-100 text-red-700 border-red-200"
    case "medium":
      return "bg-amber-100 text-amber-700 border-amber-200"
    case "low":
      return "bg-blue-100 text-blue-700 border-blue-200"
    default:
      return "bg-gray-100 text-gray-600 border-gray-200"
  }
}

function noticePriorityIcon(priority) {
  switch (priority) {
    case "high":
      return {
        path: "M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z",
        type: "text-red-500"
      }
    case "medium":
      return {
        path: "M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z",
        type: "text-amber-500"
      }
    case "low":
      return {
        path: "M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z",
        type: "text-blue-500"
      }
    default:
      return {
        path: "M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z",
        type: "text-gray-500"
      }
  }
}

function priorityText(priority) {
  switch (priority) {
    case "high":
      return "জরুরি"
    case "medium":
      return "গুরুত্বপূর্ণ"
    case "low":
      return "সাধারণ"
    default:
      return "সাধারণ"
  }
}

// Exam search/filter feature
const examSearch = ref("")
const filteredExams = computed(() => {
  if (!examSearch.value) return upcomingExams.value
  const searchTerm = examSearch.value.toLowerCase()
  return upcomingExams.value.filter(
    e =>
      e.name.toLowerCase().includes(searchTerm) ||
      e.date.toLowerCase().includes(searchTerm) ||
      e.registeredStudents.toLowerCase().includes(searchTerm) ||
      e.centers.toLowerCase().includes(searchTerm)
  )
})

// Current date and user from the provided info
const currentDateTime = "2025-08-07 06:50:26"
const currentUser = "tahsin866"
</script>

<template>
  <!-- ... template unchanged (see user's template above) ... -->
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-5">
    <!-- Notice Board -->
    <div class="lg:col-span-1">
      <div class="bg-white rounded-lg border border-gray-200 shadow-sm h-full">
        <!-- Header -->
        <div class="border-b border-gray-200 px-5 py-4 bg-gray-50">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-medium text-gray-900 flex items-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 text-indigo-600 mr-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                />
              </svg>
              নোটিশ বোর্ড
            </h3>
            <span class="text-xs text-gray-500">{{ currentDateTime }}</span>
          </div>
        </div>
        <!-- Notice List -->
        <div class="divide-y divide-gray-100 max-h-[320px] overflow-y-auto">
          <div
            v-for="notice in notices"
            :key="notice.id"
            class="px-5 py-4 hover:bg-gray-50 transition-colors cursor-pointer"
            @click="showNoticeDetails(notice)"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h4 class="text-sm font-medium text-gray-900">{{ notice.title }}</h4>
                <div class="flex items-center mt-1 text-xs text-gray-500 space-x-2">
                  <span class="flex items-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-3.5 w-3.5 mr-1"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                      />
                    </svg>
                    {{ notice.date }}
                  </span>
                  <span v-if="notice.attachment" class="flex items-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-3.5 w-3.5 mr-1"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"
                      />
                    </svg>
                    সংযুক্তি
                  </span>
                </div>
              </div>
              <span
                class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border ml-2"
                :class="noticePriorityBadge(notice.priority)"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-3 w-3 mr-0.5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    :d="noticePriorityIcon(notice.priority).path"
                  />
                </svg>
                {{ priorityText(notice.priority) }}
              </span>
            </div>
          </div>
          <div v-if="!notices.length" class="p-6 text-center text-gray-500 text-sm">কোনো নোটিশ নেই</div>
        </div>
        <!-- Footer -->
        <div class="px-5 py-3 bg-gray-50 border-t border-gray-200">
          <div class="flex justify-end">
            <button class="inline-flex items-center text-sm text-indigo-600 hover:text-indigo-800">
              <span>সকল নোটিশ দেখুন</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4 ml-1"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- Upcoming Exams -->
    <div class="lg:col-span-2">
      <div class="bg-white rounded-lg border border-gray-200 shadow-sm h-full">
        <!-- Header -->
        <div class="border-b border-gray-200 px-5 py-4 bg-gray-50">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <h3 class="text-base font-medium text-gray-900 flex items-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 text-indigo-600 mr-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
              আসন্ন পরীক্ষাসমূহ
            </h3>
            <!-- Exam Search -->
            <div class="relative w-full sm:w-64">
              <input
                v-model="examSearch"
                type="text"
                class="w-full rounded-md border border-gray-300 bg-white py-2 pl-10 pr-4 text-sm text-gray-900 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
                placeholder="পরীক্ষার নাম, তারিখ, কেন্দ্র..."
              />
              <div class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-4 w-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>
        <!-- Table -->
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >পরীক্ষার নাম</th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >তারিখ</th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >রেজিস্ট্রেশন</th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >কেন্দ্র</th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >অবস্থা</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="exam in filteredExams" :key="exam.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-5 w-5 text-indigo-500 mr-2"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="1.5"
                    >
                      <path d="M12 14l9-5-9-5-9 5 9 5z" />
                      <path
                        d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"
                      />
                    </svg>
                    <span class="text-sm font-medium text-gray-900">{{ exam.name }}</span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-700">{{ exam.date }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">{{ exam.registeredStudents }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-700">{{ exam.centers }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    class="px-2.5 py-0.5 inline-flex text-xs font-medium rounded bg-green-100 text-green-800"
                  >{{ exam.statusText }}</span>
                </td>
              </tr>
              <tr v-if="!filteredExams.length">
                <td
                  colspan="5"
                  class="px-6 py-8 text-center text-gray-500 text-sm"
                >কোনো পরীক্ষা পাওয়া যায়নি</td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- Footer -->
        <div class="px-5 py-3 bg-gray-50 border-t border-gray-200">
          <div class="flex justify-between items-center">
            <div class="text-xs text-gray-500 flex items-center">
              <span class="inline-flex items-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-4 w-4 mr-1"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
                {{ currentUser }}
              </span>
            </div>
            <button class="inline-flex items-center text-sm text-indigo-600 hover:text-indigo-800">
              <span>সকল পরীক্ষা দেখুন</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4 ml-1"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Notice Details Modal using only Tailwind CSS -->
  <div
    v-if="showNoticeModal"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    @click.self="closeNoticeDetails"
  >
    <div
      class="bg-white rounded-lg shadow-xl border border-gray-200 max-w-lg w-full relative transform transition-all duration-300 ease-in-out"
      :class="showNoticeModal ? 'opacity-100 scale-100' : 'opacity-0 scale-95'"
    >
      <div
        class="px-6 py-4 border-b border-gray-200 flex justify-between items-center bg-gray-50 rounded-t-lg"
      >
        <div class="flex items-center">
          <span
            class="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium border mr-2"
            :class="selectedNotice ? noticePriorityBadge(selectedNotice.priority) : ''"
          >
            <svg
              v-if="selectedNotice"
              xmlns="http://www.w3.org/2000/svg"
              class="h-3 w-3 mr-0.5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                :d="noticePriorityIcon(selectedNotice.priority).path"
              />
            </svg>
            {{ selectedNotice ? priorityText(selectedNotice.priority) : '' }}
          </span>
          <h3
            class="text-sm font-medium text-gray-900 truncate max-w-xs"
          >{{ selectedNotice ? selectedNotice.title : '' }}</h3>
        </div>
        <button
          @click="closeNoticeDetails"
          class="text-gray-400 hover:text-gray-600 focus:outline-none"
          aria-label="Close"
        >
          <svg
            class="h-5 w-5"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
      <div class="px-6 py-4">
        <p class="text-sm text-gray-700">{{ selectedNotice ? selectedNotice.content : '' }}</p>
        <div v-if="selectedNotice && selectedNotice.attachment" class="mt-4">
          <a
            :href="`/notices/${selectedNotice.attachment}`"
            download
            class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-4 w-4 mr-2"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"
              />
            </svg>
            সংযুক্তি ডাউনলোড
          </a>
        </div>
        <div class="text-xs text-gray-500 mt-6 flex items-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-4 w-4 mr-1"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
          প্রকাশিত: {{ selectedNotice ? selectedNotice.date : '' }}
        </div>
      </div>
      <div class="px-6 py-3 bg-gray-50 text-right rounded-b-lg">
        <button
          @click="closeNoticeDetails"
          class="inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >বন্ধ করুন</button>
      </div>
    </div>
  </div>
</template>
