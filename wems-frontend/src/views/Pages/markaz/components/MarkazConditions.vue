<template>
  <div class="rounded-xl shadow-lg bg-white text-gray-800 dark:bg-slate-800 dark:text-gray-100">
    <!-- Header Section -->
    <div class="p-6 border-b bg-white dark:bg-slate-800/70 border-gray-100 dark:border-slate-700">
      <div class="flex flex-col md:flex-row items-center justify-between gap-4 mb-6">
        <div class="flex items-center gap-3">
          <div class="p-3 rounded-lg flex items-center justify-center bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-300">
            <i class="pi pi-book text-2xl" aria-hidden="true"></i>
          </div>

          <div>
            <h2 class="text-xl md:text-2xl font-bold text-slate-800 dark:text-gray-100">
              মারকায প্রাপ্তির শর্ত ও পালনীয় কর্তব্য
            </h2>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
              দরসিয়াত • {{ getCurrentDateTime() }}
            </p>
          </div>
        </div>

        <div class="rounded-md px-4 py-2 flex items-center gap-2 bg-blue-50 border border-blue-100 dark:bg-blue-900/20 dark:border-blue-800">
          <i class="pi pi-file-pdf text-lg text-blue-600 dark:text-blue-300" aria-hidden="true"></i>
          <span class="text-sm font-medium text-blue-600 dark:text-blue-300">REF: HEFAQ/MK/2025/341</span>
        </div>
      </div>

      <div class="p-4 rounded-r-md bg-blue-50/70 border-l-4 border-blue-500 dark:bg-blue-900/20 dark:border-blue-700">
        <div class="flex items-start">
          <div class="flex-shrink-0 pt-0.5 text-blue-500 dark:text-blue-400">
            <i class="pi pi-info-circle" aria-hidden="true"></i>
          </div>
          <div class="ml-3">
            <p class="text-sm text-blue-700 dark:text-blue-300">
              নিম্নের শর্তাবলী পড়ুন এবং আবেদন পরবর্তী ধাপে যেতে সম্মতিপত্রে টিক চিহ্ন দিন। সকল শর্তাবলী মেনে চলতে আপনাকে বাধ্য থাকতে হবে। অন্যথায় আপনার মারকাজ আবেদন বাতিল হতে পারে।
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Terms Scrollable Section with Improved Styling -->
    <div class="px-6 py-5 bg-white dark:bg-slate-800">
      <!-- Document Progress Bar -->
      <div class="mb-5 flex items-center gap-3">
        <div class="w-full h-1.5 rounded-full overflow-hidden bg-gray-200 dark:bg-slate-700">
          <div
            class="h-full transition-all duration-500 ease-out bg-blue-600 dark:bg-blue-500"
            :style="{ width: scrollPercentage + '%' }"
          ></div>
        </div>

        <span class="text-sm whitespace-nowrap font-medium text-gray-600 dark:text-gray-400">
          {{ Math.round(scrollPercentage) }}%
        </span>
      </div>

      <div
        ref="termsContainer"
        @scroll="handleScroll"
        class="overflow-y-auto max-h-[500px] pr-2 mb-6 scrollbar-thin scrollbar-thumb-rounded-full scrollbar-track-gray-100 scrollbar-thumb-blue-200 dark:scrollbar-track-slate-700 dark:scrollbar-thumb-slate-600"
      >
        <div class="space-y-4">
          <!-- Section Headers -->
          <div class="p-4 rounded-r-md mb-4 bg-blue-50/70 border-l-4 border-blue-500 dark:bg-slate-700/50 dark:border-blue-500">
            <h3 class="text-lg font-bold text-slate-800 dark:text-white">ক. সাধারণ শর্তাবলী</h3>
          </div>

          <!-- Regular Terms Items -->
          <div
            v-for="index in 5"
            :key="`section1-${index}`"
            class="p-5 rounded-lg shadow-sm border transition-all bg-white hover:bg-gray-50 dark:bg-slate-700/30 dark:hover:bg-slate-700/50"
          >
            <div class="border-l-2 border-blue-500 pl-3">
              <p v-if="index === 1" class="font-medium">১. মারকায আবেদনের জন্য বেফাকের কেন্দ্রীয় পরীক্ষায় কমপক্ষে ৩ বছর অংশগ্রহণ করতে হবে।</p>
              <p v-else-if="index === 2" class="font-medium">২. বেফাক হতে প্রকাশিত পাঠ্যবই পড়াতে হবে এবং বেফাক কর্তৃক নির্ধারিত বার্ষিক চাঁদা ও ফি পরিশোধ থাকতে হবে।</p>

              <div v-else-if="index === 3">
                <p class="font-medium mb-3">৩. মারকায-বিধি অনুসারে পরীক্ষার্থীর সংখ্যা পূর্ণ হতে হবে:</p>
                <ul class="ml-5 space-y-3 mt-3">
                  <li class="p-3 rounded-md bg-blue-50 dark:bg-slate-800/60">
                    <div class="flex gap-2">
                      <span class="font-medium text-blue-700 dark:text-blue-300">ক.</span>
                      <span>দরসিয়াত ছাত্র: ঢাকা মহানগরী ২২৫ জন, ঢাকা মফস্বল ও জেলা শহর ১৫০ জন এবং মফস্বল ১২৫ জন।</span>
                    </div>
                  </li>
                  <li class="p-3 rounded-md bg-blue-50 dark:bg-slate-800/60">
                    <div class="flex gap-2">
                      <span class="font-medium text-blue-700 dark:text-blue-300">খ.</span>
                      <span>দরসিয়াত ছাত্রী: ঢাকা মহানগরী ১৫০ জন, ঢাকা মফস্বল ও জেলা শহর ১২৫ জন এবং মফস্বল ১০০ জন।</span>
                    </div>
                  </li>
                </ul>
              </div>

              <p v-else-if="index === 4" class="font-medium">৪. আবেদনকৃত মারকায মাদরাসার নিজ পরীক্ষার্থী কমপক্ষে এক-তৃতীয়াংশ হতে হবে।</p>
              <p v-else-if="index === 5" class="font-medium">৫. পূর্বের মারকায ও পার্শ্ববর্তী মারকাযের ক্ষতি না হয়; এমন অবস্থানে থাকতে হবে।</p>
            </div>
          </div>

          <!-- Section Headers -->
          <div class="p-4 rounded-r-md mb-4 mt-8 bg-blue-50/70 border-l-4 border-blue-500 dark:bg-slate-700/50 dark:border-blue-500">
            <h3 class="text-lg font-bold text-slate-800 dark:text-white">খ. অবকাঠামো ও সুবিধা সংক্রান্ত</h3>
          </div>

          <div
            v-for="index in 7"
            :key="`section2-${index}`"
            class="p-5 rounded-lg shadow-sm border transition-all bg-white hover:bg-gray-50 dark:bg-slate-700/30 dark:hover:bg-slate-700/50"
          >
            <div class="border-l-2 border-blue-500 pl-3">
              <p v-if="index === 1" class="font-medium">৬. আবেদনকৃত মারকায মাদরাসার ইলহাক কমপক্ষে সানাবিয়া উলিয়া মারহালা পর্যন্ত থাকতে হবে।</p>
              <p v-else-if="index === 2" class="font-medium">৭. আবেদনকৃত মারকায মাদরাসা আবাসিক হতে হবে।</p>
              <p v-else-if="index === 3" class="font-medium">৮. পূর্বের মারকাযের সিল-স্বাক্ষরসহ অনাপত্তিপত্র অনলাইনে দাখিল করতে হবে।</p>
              <p v-else-if="index === 4" class="font-medium">৯. মাদরাসা কমিটির মারকায নেওয়ার সিদ্ধান্তের রেজুলেশন অনলাইনে দাখিল করতে হবে।</p>
              <p v-else-if="index === 5" class="font-medium">১০. বেফাক জেলা বা থানা কমিটির সভাপতি/সেক্রেটারির সুপারিশ অনলাইনে দাখিল করতে হবে।</p>
              <p v-else-if="index === 6" class="font-medium">১১. আবেদনকৃত মারকাযে পরীক্ষা দিতে ইচ্ছুক মাদরাসাসমূহের সম্মতিপত্র এবং গত বছর পরীক্ষায় অংশগ্রহণ করে থাকলে পূর্বের মারকাযের সিল-স্বাক্ষরসহ অনাপত্তিপত্র অনলাইনে দাখিল করতে হবে।</p>

              <div v-else-if="index === 7">
                <p class="font-medium mb-3">১২. মারকায-বিধি অনুসারে পরীক্ষার্থীর সংখ্যা অনুপাতে প্রশস্ত পরীক্ষার হল থাকতে হবে:</p>
                <ul class="ml-5 space-y-3 mt-3">
                  <li class="p-3 rounded-md bg-blue-50 dark:bg-slate-800/60">
                    <div class="flex gap-2">
                      <span class="font-medium text-blue-700 dark:text-blue-300">ক.</span>
                      <span>প্রতি ৪ (চার) ফুট লম্বা তেপায়ায় ২জন, ৬ (ছয়) ফুট তেপায়ায় ৩জন পরীক্ষার্থী বসবে; এ অনুপাতে পর্যাপ্ত তেপায়ার ব্যবস্থা থাকতে হবে।</span>
                    </div>
                  </li>
                  <li class="p-3 rounded-md bg-blue-50 dark:bg-slate-800/60">
                    <div class="flex gap-2">
                      <span class="font-medium text-blue-700 dark:text-blue-300">খ.</span>
                      <span>তেপায়ার দুই সারির মাঝে কমপক্ষে ৩ (তিন) ফুট দূরত্ব থাকতে হবে।</span>
                    </div>
                  </li>
                  <li class="p-3 rounded-md bg-blue-50 dark:bg-slate-800/60">
                    <div class="flex gap-2">
                      <span class="font-medium text-blue-700 dark:text-blue-300">গ.</span>
                      <span>পরীক্ষা চলাকালীন পরবর্তী সময়ে হল তালাবদ্ধ থাকতে হবে।</span>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Section Headers -->
          <div class="p-4 rounded-r-md mb-4 mt-8 bg-blue-50/70 border-l-4 border-blue-500 dark:bg-slate-700/50 dark:border-blue-500">
            <h3 class="text-lg font-bold text-slate-800 dark:text-white">গ. আর্থিক ও প্রশাসনিক বিষয়াবলী</h3>
          </div>

          <div
            v-for="index in 6"
            :key="`section3-${index}`"
            class="p-5 rounded-lg shadow-sm border transition-all bg-white hover:bg-gray-50 dark:bg-slate-700/30 dark:hover:bg-slate-700/50"
          >
            <div class="border-l-2 border-blue-500 pl-3">
              <p v-if="index === 1" class="font-medium">১৩. হলের নিকটবর্তী স্থানে ইস্তিঞ্জাখানা থাকতে হবে।</p>
              <p v-else-if="index === 2" class="font-medium">১৭. বিধি মোতাবেক মারকায কমিটি গঠন করে অর্পিত দায়িত্ব যথাযথভাবে আদায় করা এবং পরীক্ষা চলাকালীন প্রতিদিন মারকাযে উপস্থিত থাকতে হবে।</p>
              <p v-else-if="index === 3" class="font-medium">১৮. পরীক্ষার্থীর সংখ্যানুপাতে যোগ্য নেগরান-মুমতাহিন প্রদান করতে হবে।</p>
              <p v-else-if="index === 4" class="font-medium">
                ১৯. বেফাক-এর পরীক্ষা সংক্রান্ত যাবতীয় বিজ্ঞপ্তি/ঘোষণা যথাসময়ে মারকাযের অধীন মাদরাসাসমূহকে অবগত করতে হবে। মাদরাসাগুলোর সাথে সার্বিক যোগাযোগ ও সৌহার্দপূর্ণ আচরণ করতে হবে। প্রয়োজনে পরীক্ষা চলাকালীন তাদের থাকা-খাওয়ার
                সু-ব্যবস্থা করবে।
              </p>
              <p v-else-if="index === 5" class="font-medium">
                ২০. মারকাযের অনলাইন কার্যক্রম পরিচালনা, মারকাযের অধীন মাদরাসাসমূহের এডমিনদেরকে প্রশিক্ষণ দিয়ে অনলাইন কার্যক্রম সম্পাদনে সহায়তা এবং পরীক্ষা চলাকালীন পূর্ণ সময়ে নেগরানে আলাকে সার্বিক সহযোগিতা করতে, অনলাইন কাজ বুঝে এমন একজন
                মারকায এডমিন (দায়িত্বশীল)-এর ব্যবস্থা করতে হবে।
              </p>
              <p v-else-if="index === 6" class="font-medium">
                ২১. বিগত ৭/৮/১৮ ঈ. তারিখের ইমতিহান কমিটির বৈঠকের সিদ্ধান্ত মোতাবেক, দরসিয়াত মারকায (ছাত্র/ছাত্রী) মঞ্জুরি-ফি (এককালীন)- ঢাকা মহানগর ২৪০০০/-, ঢাকা মফস্বল ও জেলা শহরগুলোতে ১৫,০০০/- এবং মফস্বল এলাকায় ৯,০০০/- মারকায মঞ্জুর
                হওয়া-সাপেক্ষে প্রদান করতে হবে।
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Agreement Section -->
    <div class="flex justify-end p-4 rounded-b-lg mt-4 bg-gray-50 border-t border-gray-200 dark:bg-slate-700 dark:border-slate-600">
      <div class="flex items-center gap-4">
        <label class="flex items-center gap-2 cursor-pointer select-none">
          <input type="checkbox" v-model="agreed" class="form-checkbox h-5 w-5 text-blue-600" />
          <span class="font-medium text-gray-700 dark:text-gray-200">শর্তাবলী পড়েছি এবং সম্মত</span>
        </label>

        <button
          :disabled="!agreed"
          @click="emitContinue"
          :class="[
            'flex items-center gap-2 px-6 py-2 rounded font-semibold transition-colors',
            agreed ? 'bg-blue-600 text-white hover:bg-blue-700' : 'bg-gray-100 text-gray-400 cursor-not-allowed dark:bg-slate-700 dark:text-gray-400'
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
/* Tailwind handles most visuals; small polished scrollbar tweak for modern browsers */
:deep(.scrollbar-thin) {
  scrollbar-width: thin;
}
:deep(.scrollbar-thumb-rounded-full::-webkit-scrollbar) {
  height: 8px;
  width: 8px;
}
:deep(.scrollbar-thumb-rounded-full::-webkit-scrollbar-thumb) {
  border-radius: 9999px;
}
</style>
