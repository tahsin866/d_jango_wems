<template>
  <div class="rounded-sm shadow border border-gray-300 bg-white text-gray-800">
    <!-- Header Section -->
    <div class="p-6 border-b border-gray-300 bg-gradient-to-r from-gray-800 to-gray-700">
      <div class="flex flex-col md:flex-row items-center justify-between gap-4 mb-6">
        <div class="flex items-center gap-3">
          <div class="p-3 rounded-sm flex items-center justify-center bg-gray-700 text-white">
            <i class="pi pi-book text-2xl" aria-hidden="true"></i>
          </div>

          <div>
            <h2 class="text-xl md:text-2xl font-bold text-white">
              মারকায প্রাপ্তির শর্ত ও পালনীয় কর্তব্য
            </h2>
            <p class="mt-1 text-sm text-gray-300">
              দরসিয়াত • {{ getCurrentDateTime() }}
            </p>
          </div>
        </div>

        <div class="rounded-sm px-4 py-2 flex items-center gap-2 bg-gray-700 border border-gray-600">
          <i class="pi pi-file-pdf text-lg text-white" aria-hidden="true"></i>
          <span class="text-sm font-medium text-white">REF: HEFAQ/MK/2025/341</span>
        </div>
      </div>

      <div class="p-4 rounded-r-sm bg-gray-700/30 border-l-4 border-gray-400">
        <div class="flex items-start">
          <div class="flex-shrink-0 pt-0.5 text-gray-300">
            <i class="pi pi-info-circle" aria-hidden="true"></i>
          </div>
          <div class="ml-3">
            <p class="text-sm text-gray-200">
              নিম্নের শর্তাবলী পড়ুন এবং আবেদন পরবর্তী ধাপে যেতে সম্মতিপত্রে টিক চিহ্ন দিন। সকল শর্তাবলী মেনে চলতে আপনাকে বাধ্য থাকতে হবে। অন্যথায় আপনার মারকাজ আবেদন বাতিল হতে পারে।
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Terms Scrollable Section with Classic Styling -->
    <div class="px-6 py-5 bg-white">
      <!-- Document Progress Bar -->
      <div class="mb-5 flex items-center gap-3">
        <div class="w-full h-2 rounded-sm overflow-hidden bg-gray-200">
          <div
            class="h-full transition-all duration-500 ease-out bg-gray-700"
            :style="{ width: scrollPercentage + '%' }"
          ></div>
        </div>

        <span class="text-sm whitespace-nowrap font-medium text-gray-600">
          {{ Math.round(scrollPercentage) }}%
        </span>
      </div>

      <div
        ref="termsContainer"
        @scroll="handleScroll"
        class="overflow-y-auto max-h-[500px] pr-2 mb-6 border border-gray-300 rounded-sm bg-gray-50"
      >
        <div class="space-y-4 p-4">
          <!-- Section Headers -->
          <div class="p-4 rounded-r-sm mb-4 bg-gray-100 border-l-4 border-gray-500">
            <h3 class="text-lg font-bold text-gray-800">ক. সাধারণ শর্তাবলী</h3>
          </div>

          <!-- Regular Terms Items -->
          <div
            v-for="index in 5"
            :key="`section1-${index}`"
            class="p-5 rounded-sm border border-gray-300 bg-white"
          >
            <div class="border-l-2 border-gray-500 pl-3">
              <p v-if="index === 1" class="font-medium text-gray-800">১. মারকায আবেদনের জন্য বেফাকের কেন্দ্রীয় পরীক্ষায় কমপক্ষে ৩ বছর অংশগ্রহণ করতে হবে।</p>
              <p v-else-if="index === 2" class="font-medium text-gray-800">২. বেফাক হতে প্রকাশিত পাঠ্যবই পড়াতে হবে এবং বেফাক কর্তৃক নির্ধারিত বার্ষিক চাঁদা ও ফি পরিশোধ থাকতে হবে।</p>

              <div v-else-if="index === 3">
                <p class="font-medium text-gray-800 mb-3">৩. মারকায-বিধি অনুসারে পরীক্ষার্থীর সংখ্যা পূর্ণ হতে হবে:</p>
                <ul class="ml-5 space-y-3 mt-3">
                  <li class="p-3 rounded-sm bg-gray-50 border border-gray-200">
                    <div class="flex gap-2">
                      <span class="font-medium text-gray-700">ক.</span>
                      <span class="text-gray-800">দরসিয়াত ছাত্র: ঢাকা মহানগরী ২২৫ জন, ঢাকা মফস্বল ও জেলা শহর ১৫০ জন এবং মফস্বল ১২৫ জন।</span>
                    </div>
                  </li>
                  <li class="p-3 rounded-sm bg-gray-50 border border-gray-200">
                    <div class="flex gap-2">
                      <span class="font-medium text-gray-700">খ.</span>
                      <span class="text-gray-800">দরসিয়াত ছাত্রী: ঢাকা মহানগরী ১৫০ জন, ঢাকা মফস্বল ও জেলা শহর ১২৫ জন এবং মফস্বল ১০০ জন।</span>
                    </div>
                  </li>
                </ul>
              </div>

              <p v-else-if="index === 4" class="font-medium text-gray-800">৪. আবেদনকৃত মারকায মাদরাসার নিজ পরীক্ষার্থী কমপক্ষে এক-তৃতীয়াংশ হতে হবে।</p>
              <p v-else-if="index === 5" class="font-medium text-gray-800">৫. পূর্বের মারকায ও পার্শ্ববর্তী মারকাযের ক্ষতি না হয়; এমন অবস্থানে থাকতে হবে।</p>
            </div>
          </div>

          <!-- Section Headers -->
          <div class="p-4 rounded-r-sm mb-4 mt-8 bg-gray-100 border-l-4 border-gray-500">
            <h3 class="text-lg font-bold text-gray-800">খ. অবকাঠামো ও সুবিধা সংক্রান্ত</h3>
          </div>

          <div
            v-for="index in 7"
            :key="`section2-${index}`"
            class="p-5 rounded-sm border border-gray-300 bg-white"
          >
            <div class="border-l-2 border-gray-500 pl-3">
              <p v-if="index === 1" class="font-medium text-gray-800">৬. আবেদনকৃত মারকায মাদরাসার ইলহাক কমপক্ষে সানাবিয়া উলিয়া মারহালা পর্যন্ত থাকতে হবে।</p>
              <p v-else-if="index === 2" class="font-medium text-gray-800">৭. আবেদনকৃত মারকায মাদরাসা আবাসিক হতে হবে।</p>
              <p v-else-if="index === 3" class="font-medium text-gray-800">৮. পূর্বের মারকাযের সিল-স্বাক্ষরসহ অনাপত্তিপত্র অনলাইনে দাখিল করতে হবে।</p>
              <p v-else-if="index === 4" class="font-medium text-gray-800">৯. মাদরাসা কমিটির মারকায নেওয়ার সিদ্ধান্তের রেজুলেশন অনলাইনে দাখিল করতে হবে।</p>
              <p v-else-if="index === 5" class="font-medium text-gray-800">১০. বেফাক জেলা বা থানা কমিটির সভাপতি/সেক্রেটারির সুপারিশ অনলাইনে দাখিল করতে হবে।</p>
              <p v-else-if="index === 6" class="font-medium text-gray-800">১১. আবেদনকৃত মারকাযে পরীক্ষা দিতে ইচ্ছুক মাদরাসাসমূহের সম্মতিপত্র এবং গত বছর পরীক্ষায় অংশগ্রহণ করে থাকলে পূর্বের মারকাযের সিল-স্বাক্ষরসহ অনাপত্তিপত্র অনলাইনে দাখিল করতে হবে।</p>

              <div v-else-if="index === 7">
                <p class="font-medium text-gray-800 mb-3">১২. মারকায-বিধি অনুসারে পরীক্ষার্থীর সংখ্যা অনুপাতে প্রশস্ত পরীক্ষার হল থাকতে হবে:</p>
                <ul class="ml-5 space-y-3 mt-3">
                  <li class="p-3 rounded-sm bg-gray-50 border border-gray-200">
                    <div class="flex gap-2">
                      <span class="font-medium text-gray-700">ক.</span>
                      <span class="text-gray-800">প্রতি ৪ (চার) ফুট লম্বা তেপায়ায় ২জন, ৬ (ছয়) ফুট তেপায়ায় ৩জন পরীক্ষার্থী বসবে; এ অনুপাতে পর্যাপ্ত তেপায়ার ব্যবস্থা থাকতে হবে।</span>
                    </div>
                  </li>
                  <li class="p-3 rounded-sm bg-gray-50 border border-gray-200">
                    <div class="flex gap-2">
                      <span class="font-medium text-gray-700">খ.</span>
                      <span class="text-gray-800">তেপায়ার দুই সারির মাঝে কমপক্ষে ৩ (তিন) ফুট দূরত্ব থাকতে হবে।</span>
                    </div>
                  </li>
                  <li class="p-3 rounded-sm bg-gray-50 border border-gray-200">
                    <div class="flex gap-2">
                      <span class="font-medium text-gray-700">গ.</span>
                      <span class="text-gray-800">পরীক্ষা চলাকালীন পরবর্তী সময়ে হল তালাবদ্ধ থাকতে হবে।</span>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Section Headers -->
          <div class="p-4 rounded-r-sm mb-4 mt-8 bg-gray-100 border-l-4 border-gray-500">
            <h3 class="text-lg font-bold text-gray-800">গ. আর্থিক ও প্রশাসনিক বিষয়াবলী</h3>
          </div>

          <div
            v-for="index in 6"
            :key="`section3-${index}`"
            class="p-5 rounded-sm border border-gray-300 bg-white"
          >
            <div class="border-l-2 border-gray-500 pl-3">
              <p v-if="index === 1" class="font-medium text-gray-800">১৩. হলের নিকটবর্তী স্থানে ইস্তিঞ্জাখানা থাকতে হবে।</p>
              <p v-else-if="index === 2" class="font-medium text-gray-800">১৭. বিধি মোতাবেক মারকায কমিটি গঠন করে অর্পিত দায়িত্ব যথাযথভাবে আদায় করা এবং পরীক্ষা চলাকালীন প্রতিদিন মারকাযে উপস্থিত থাকতে হবে।</p>
              <p v-else-if="index === 3" class="font-medium text-gray-800">১৮. পরীক্ষার্থীর সংখ্যানুপাতে যোগ্য নেগরান-মুমতাহিন প্রদান করতে হবে।</p>
              <p v-else-if="index === 4" class="font-medium text-gray-800">
                ১৯. বেফাক-এর পরীক্ষা সংক্রান্ত যাবতীয় বিজ্ঞপ্তি/ঘোষণা যথাসময়ে মারকাযের অধীন মাদরাসাসমূহকে অবগত করতে হবে। মাদরাসাগুলোর সাথে সার্বিক যোগাযোগ ও সৌহার্দপূর্ণ আচরণ করতে হবে। প্রয়োজনে পরীক্ষা চলাকালীন তাদের থাকা-খাওয়ার
                সু-ব্যবস্থা করবে।
              </p>
              <p v-else-if="index === 5" class="font-medium text-gray-800">
                ২০. মারকাযের অনলাইন কার্যক্রম পরিচালনা, মারকাযের অধীন মাদরাসাসমূহের এডমিনদেরকে প্রশিক্ষণ দিয়ে অনলাইন কার্যক্রম সম্পাদনে সহায়তা এবং পরীক্ষা চলাকালীন পূর্ণ সময়ে নেগরানে আলাকে সার্বিক সহযোগিতা করতে, অনলাইন কাজ বুঝে এমন একজন
                মারকায এডমিন (দায়িত্বশীল)-এর ব্যবস্থা করতে হবে।
              </p>
              <p v-else-if="index === 6" class="font-medium text-gray-800">
                ২১. বিগত ৭/৮/১৮ ঈ. তারিখের ইমতিহান কমিটির বৈঠকের সিদ্ধান্ত মোতাবেক, দরসিয়াত মারকায (ছাত্র/ছাত্রী) মঞ্জুরি-ফি (এককালীন)- ঢাকা মহানগর ২৪০০০/-, ঢাকা মফস্বল ও জেলা শহরগুলোতে ১৫,০০০/- এবং মফস্বল এলাকায় ৯,০০০/- মারকায মঞ্জুর
                হওয়া-সাপেক্ষে প্রদান করতে হবে।
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Agreement Section -->
    <div class="flex justify-end p-4 rounded-b-sm bg-gray-100 border-t border-gray-300">
      <div class="flex items-center gap-4">
        <label class="flex items-center gap-2 cursor-pointer select-none">
          <input type="checkbox" v-model="agreed" class="form-checkbox h-5 w-5 text-gray-700 border border-gray-300 rounded-sm focus:ring-gray-500" />
          <span class="font-medium text-gray-700">শর্তাবলী পড়েছি এবং সম্মত</span>
        </label>

        <button
          :disabled="!agreed"
          @click="emitContinue"
          :class="[
            'flex items-center gap-2 px-6 py-2 rounded-sm font-semibold transition-colors',
            agreed ? 'bg-gray-700 text-white hover:bg-gray-600' : 'bg-gray-200 text-gray-400 cursor-not-allowed'
          ]"
        >
          <span>পরবর্তী ধাপে যান</span>
          <i class="pi pi-arrow-right" aria-hidden="true"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

const emit = defineEmits<{
  (e: 'continue'): void;
}>();

// User agreement state
const agreed = ref(false);

// Scrolling progress tracking
const scrollPercentage = ref(0);
const termsContainer = ref<HTMLElement | null>(null);

const handleScroll = () => {
  const el = termsContainer.value;
  if (!el) return;
  const scrollTop = el.scrollTop;
  const scrollHeight = el.scrollHeight;
  const clientHeight = el.clientHeight;
  const percent = (scrollTop / (scrollHeight - clientHeight)) * 100;
  scrollPercentage.value = Number.isFinite(percent) ? Math.max(0, Math.min(100, percent)) : 0;
};

// Emit continue
function emitContinue() {
  if (!agreed.value) return;
  emit('continue');
}

// Helper function to get current date in formatted style
const getCurrentDateTime = () => {
  // Using the timestamp provided in the conversation for consistency
  return '2025-08-10 04:31:59';
};

onMounted(() => {
  if (termsContainer.value) {
    termsContainer.value.addEventListener('scroll', handleScroll, { passive: true });
  }
});

onUnmounted(() => {
  if (termsContainer.value) {
    termsContainer.value.removeEventListener('scroll', handleScroll);
  }
});
</script>

<style scoped>
/* Classic scrollbar styling */
:deep(.overflow-y-auto::-webkit-scrollbar) {
  width: 8px;
}

:deep(.overflow-y-auto::-webkit-scrollbar-track) {
  background: #f1f1f1;
  border-radius: 0;
}

:deep(.overflow-y-auto::-webkit-scrollbar-thumb) {
  background: #c1c1c1;
  border-radius: 0;
}

:deep(.overflow-y-auto::-webkit-scrollbar-thumb:hover) {
  background: #a8a8a8;
}
</style>
