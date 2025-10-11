<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="grid grid-cols-1 lg:grid-cols-3 gap-7 mt-7"
  >
    <!-- Notice Board -->
    <div class="lg:col-span-1">
      <div class="bg-white border border-gray-300 rounded-sm shadow-lg h-full">
        <!-- Header -->
        <div class="bg-gray-800 px-6 py-4 rounded-t-sm border-b border-gray-700 flex items-center justify-between">
          <h3 class="text-base font-bold text-white flex items-center tracking-tight">
            <i class="fas fa-bell mr-2 text-indigo-300"></i>
            নোটিশ বোর্ড
          </h3>
          <span class="text-xs text-gray-300">{{ currentDateTime }}</span>
        </div>
        <!-- Notice List -->
        <div class="divide-y divide-gray-100 max-h-[320px] overflow-y-auto bg-white">
          <div
            v-for="notice in notices"
            :key="notice.id"
            class="px-6 py-4 hover:bg-gray-50 transition-colors cursor-pointer"
            @click="showNoticeDetails(notice)"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h4 class="text-sm font-bold text-gray-900">{{ notice.title }}</h4>
                <div class="flex items-center mt-1 text-xs text-gray-500 space-x-2">
                  <span class="flex items-center">
                    <i class="fas fa-calendar-alt mr-1 text-indigo-400"></i>
                    {{ notice.date }}
                  </span>
                  <span v-if="notice.attachment" class="flex items-center">
                    <i class="fas fa-paperclip mr-1 text-gray-400"></i>
                    সংযুক্তি
                  </span>
                </div>
              </div>
              <span
                class="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold border ml-2"
                :class="noticePriorityBadge(notice.priority)"
              >
                <i
                  :class="`fas fa-circle mr-1 ${noticePriorityIcon(notice.priority).type}`"
                  style="font-size: 0.7rem"
                ></i>
                {{ priorityText(notice.priority) }}
              </span>
            </div>
          </div>
          <div v-if="!notices.length" class="p-6 text-center text-gray-500 text-sm">কোনো নোটিশ নেই</div>
        </div>
        <!-- Footer -->
        <div class="px-6 py-3 bg-gray-50 border-t border-gray-300 rounded-b-xl flex justify-end">
          <button class="inline-flex items-center text-sm text-indigo-700 hover:text-indigo-900 font-semibold">
            <span>সকল নোটিশ দেখুন</span>
            <i class="fas fa-arrow-right ml-1"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Upcoming Exams -->
    <div class="lg:col-span-2">
      <div class="bg-white border border-gray-300 rounded-sm shadow-lg h-full">
        <!-- Header -->
        <div class="bg-gray-800 px-6 py-4 rounded-t-sm border-b border-gray-700 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <h3 class="text-base font-bold text-white flex items-center tracking-tight">
            <i class="fas fa-list-alt mr-2 text-indigo-300"></i>
            আসন্ন পরীক্ষাসমূহ
          </h3>
          <!-- Exam Search -->
          <div class="relative w-full sm:w-72">
            <input
              v-model="examSearch"
              type="text"
              class="w-full rounded-lg border border-gray-400 bg-gray-100 py-2 pl-10 pr-4 text-sm text-gray-900 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
              placeholder="পরীক্ষার নাম, তারিখ, কেন্দ্র..."
            />
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
              <i class="fas fa-search"></i>
            </span>
          </div>
        </div>
        <!-- Table -->
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 bg-white">
            <thead class="bg-gray-100">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wide">পরীক্ষার নাম</th>
                <th class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wide">তারিখ</th>
                <th class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wide">রেজিস্ট্রেশন</th>
                <th class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wide">কেন্দ্র</th>
                <th class="px-6 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wide">অবস্থা</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="exam in filteredExams" :key="exam.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <i class="fas fa-graduation-cap mr-2 text-indigo-500"></i>
                    <span class="text-sm font-bold text-gray-900">{{ exam.name }}</span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-700">{{ exam.date }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-bold text-gray-900">{{ exam.registeredStudents }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-700">{{ exam.centers }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2.5 py-0.5 inline-flex text-xs font-bold rounded bg-green-100 text-green-800">
                    {{ exam.statusText }}
                  </span>
                </td>
              </tr>
              <tr v-if="!filteredExams.length">
                <td colspan="5" class="px-6 py-8 text-center text-gray-500 text-sm">কোনো পরীক্ষা পাওয়া যায়নি</td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- Footer -->
        <div class="px-6 py-3 bg-gray-50 border-t border-gray-300 rounded-b-xl flex justify-between items-center">
          <span class="text-xs text-gray-600 flex items-center">
            <i class="fas fa-user mr-1"></i>
            {{ currentUser }}
          </span>
          <button class="inline-flex items-center text-sm text-indigo-700 hover:text-indigo-900 font-semibold">
            <span>সকল পরীক্ষা দেখুন</span>
            <i class="fas fa-arrow-right ml-1"></i>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Notice Details Modal (AdminLTE flavor, Tailwind only) -->
  <div
    v-if="showNoticeModal"
    class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50 p-4"
    @click.self="closeNoticeDetails"
  >
    <div
      class="bg-white border border-gray-300 rounded-xl shadow-2xl max-w-lg w-full relative"
      :class="showNoticeModal ? 'opacity-100 scale-100' : 'opacity-0 scale-95'"
    >
      <!-- Modal Header -->
      <div class="px-6 py-4 bg-gray-800 border-b border-gray-700 rounded-t-xl flex justify-between items-center">
        <div class="flex items-center">
          <span
            class="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-bold border mr-2"
            :class="selectedNotice ? noticePriorityBadge(selectedNotice.priority) : ''"
          >
            <i
              v-if="selectedNotice"
              :class="`fas fa-circle mr-1 ${noticePriorityIcon(selectedNotice.priority).type}`"
              style="font-size: 0.8rem"
            ></i>
            {{ selectedNotice ? priorityText(selectedNotice.priority) : '' }}
          </span>
          <h3 class="text-sm font-bold text-white truncate max-w-xs">{{ selectedNotice ? selectedNotice.title : '' }}</h3>
        </div>
        <button
          @click="closeNoticeDetails"
          class="text-gray-300 hover:text-white focus:outline-none"
          aria-label="Close"
        >
          <i class="fas fa-times text-lg"></i>
        </button>
      </div>
      <!-- Modal Body -->
      <div class="px-6 py-6 bg-gray-50">
        <p class="text-sm text-gray-800">{{ selectedNotice ? selectedNotice.content : '' }}</p>
        <div v-if="selectedNotice && selectedNotice.attachment" class="mt-4">
          <a
            :href="`/notices/${selectedNotice.attachment}`"
            download
            class="inline-flex items-center px-4 py-2 border border-gray-400 shadow-sm text-xs font-bold rounded text-gray-800 bg-white hover:bg-gray-100"
          >
            <i class="fas fa-paperclip mr-2"></i>
            সংযুক্তি ডাউনলোড
          </a>
        </div>
        <div class="text-xs text-gray-500 mt-6 flex items-center">
          <i class="fas fa-calendar-alt mr-1"></i>
          প্রকাশিত: {{ selectedNotice ? selectedNotice.date : '' }}
        </div>
      </div>
      <!-- Modal Footer -->
      <div class="px-6 py-4 bg-gray-100 border-t border-gray-300 rounded-b-xl text-right">
        <button
          @click="closeNoticeDetails"
          class="inline-flex justify-center py-2 px-5 border border-gray-400 shadow-sm text-sm font-bold rounded-md text-gray-800 bg-white hover:bg-gray-100"
        >বন্ধ করুন</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

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
]);

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
]);

const selectedNotice = ref(null);
const showNoticeModal = ref(false);

function showNoticeDetails(notice) {
  selectedNotice.value = notice;
  showNoticeModal.value = true;
}

function closeNoticeDetails() {
  setTimeout(() => {
    selectedNotice.value = null;
  }, 200);
  showNoticeModal.value = false;
}

function noticePriorityBadge(priority) {
  switch (priority) {
    case "high":
      return "bg-red-100 text-red-700 border-red-300";
    case "medium":
      return "bg-amber-100 text-amber-700 border-amber-300";
    case "low":
      return "bg-blue-100 text-blue-700 border-blue-300";
    default:
      return "bg-gray-100 text-gray-600 border-gray-300";
  }
}

function noticePriorityIcon(priority) {
  switch (priority) {
    case "high":
      return {
        path: "",
        type: "text-red-500"
      };
    case "medium":
      return {
        path: "",
        type: "text-amber-500"
      };
    case "low":
      return {
        path: "",
        type: "text-blue-500"
      };
    default:
      return {
        path: "",
        type: "text-gray-500"
      };
  }
}

function priorityText(priority) {
  switch (priority) {
    case "high":
      return "জরুরি";
    case "medium":
      return "গুরুত্বপূর্ণ";
    case "low":
      return "সাধারণ";
    default:
      return "সাধারণ";
  }
}

// Exam search/filter feature
const examSearch = ref("");
const filteredExams = computed(() => {
  if (!examSearch.value) return upcomingExams.value;
  const searchTerm = examSearch.value.toLowerCase();
  return upcomingExams.value.filter(
    e =>
      e.name.toLowerCase().includes(searchTerm) ||
      e.date.toLowerCase().includes(searchTerm) ||
      e.registeredStudents.toLowerCase().includes(searchTerm) ||
      e.centers.toLowerCase().includes(searchTerm)
  );
});

// Current date and user from the provided info
const currentDateTime = "2025-08-07 06:50:26";
const currentUser = "tahsin866";
</script>
