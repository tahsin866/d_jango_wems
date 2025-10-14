<template>
  <section
    class="relative py-20 lg:py-32 overflow-hidden bg-gradient-to-br from-slate-50 via-gray-50 to-slate-100"
    style="font-family: 'Inter', 'SolaimanLipi', sans-serif;"
  >
    <!-- Subtle Grid Pattern Background -->
    <div class="absolute inset-0 opacity-[0.03]">
      <div
        class="absolute inset-0"
        style="background-image: linear-gradient(rgba(15, 23, 42, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(15, 23, 42, 0.03) 1px, transparent 1px); background-size: 32px 32px;"
      ></div>
    </div>

    <!-- Geometric Elements -->
    <div class="absolute top-20 right-10 w-32 h-32 opacity-5">
      <div class="w-full h-full border-2 border-emerald-400 rounded-2xl transform rotate-12"></div>
    </div>
    <div class="absolute bottom-20 left-10 w-24 h-24 opacity-5">
      <div class="w-full h-full bg-emerald-200 rounded-full transform -rotate-12"></div>
    </div>

    <div class="container mx-auto px-6 lg:px-8 relative z-10">
      <div class="max-w-6xl mx-auto">

        <!-- Top Badge -->
        <div class="flex justify-center mb-12">
          <div class="inline-flex items-center gap-2 bg-white/80 backdrop-blur-sm border border-slate-200/80 rounded-full px-6 py-2.5 shadow-sm">
            <div class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
            <span class="text-sm font-medium text-slate-600">বেফাকুল মাদারিসিল আরাবিয়া বাংলাদেশ</span>
          </div>
        </div>

        <!-- Main Heading -->
        <div class="text-center mb-16">
          <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-slate-900 leading-[1.1] tracking-tight mb-6">
            ছাত্র-ছাত্রী সেবাসমূহ
          </h1>
          <div class="max-w-3xl mx-auto">
            <p class="text-lg md:text-xl text-slate-600 leading-relaxed">
              আধুনিক প্রযুক্তির সাথে ইসলামিক শিক্ষার সমন্বয়ে গড়া ডিজিটাল শিক্ষা পোর্টালে আপনাকে স্বাগতম
            </p>
          </div>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
          <div class="bg-white/70 backdrop-blur-sm border border-slate-200/60 rounded-2xl p-8 text-center shadow-sm hover:shadow-md transition-all duration-300 group">
            <div class="w-16 h-16 bg-gradient-to-br from-emerald-100 to-emerald-200 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
              <svg class="w-8 h-8 text-emerald-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M16 4c0-1.11.89-2 2-2s2 .89 2 2-.89 2-2 2-2-.89-2-2zm4 18v-6h2.5l-2.54-7.63A2.95 2.95 0 0 0 17.06 7H16c-.8 0-1.54.37-2.01.99L12 10l-1.99-2.01A2.99 2.99 0 0 0 8 7H6.94c-1.4 0-2.6.99-2.9 2.37L1.5 16H4v6h16z"/>
              </svg>
            </div>
            <div class="text-3xl font-bold text-slate-900 mb-2">৫০,০০০+</div>
            <div class="text-slate-600 font-medium">নিবন্ধিত শিক্ষার্থী</div>
          </div>

          <div class="bg-white/70 backdrop-blur-sm border border-slate-200/60 rounded-2xl p-8 text-center shadow-sm hover:shadow-md transition-all duration-300 group">
            <div class="w-16 h-16 bg-gradient-to-br from-emerald-100 to-emerald-200 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
              <svg class="w-8 h-8 text-emerald-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              </svg>
            </div>
            <div class="text-3xl font-bold text-slate-900 mb-2">৪৭তম</div>
            <div class="text-slate-600 font-medium">কেন্দ্রীয় পরীক্ষা</div>
          </div>

          <div class="bg-white/70 backdrop-blur-sm border border-slate-200/60 rounded-2xl p-8 text-center shadow-sm hover:shadow-md transition-all duration-300 group">
            <div class="w-16 h-16 bg-gradient-to-br from-emerald-100 to-emerald-200 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
              <svg class="w-8 h-8 text-emerald-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
              </svg>
            </div>
            <div class="text-3xl font-bold text-slate-900 mb-2">২৪/৭</div>
            <div class="text-slate-600 font-medium">অনলাইন সেবা</div>
          </div>
        </div>

        <!-- Service Cards Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-20">

          <!-- Result Search Card -->
          <div class="bg-white/70 backdrop-blur-sm border border-slate-200/60 rounded-2xl p-8 shadow-sm hover:shadow-lg transition-all duration-300 group">
            <div class="relative">
              <!-- Status Badge -->
              <div class="absolute -top-2 -right-2">
                <div class="bg-red-500 text-white px-3 py-1 rounded-full text-xs font-medium">
                  নতুন
                </div>
              </div>

              <!-- Header -->
              <div class="flex items-start gap-6 mb-6">
                <div class="w-16 h-16 bg-gradient-to-br from-emerald-100 to-emerald-200 rounded-2xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform duration-300">
                  <svg class="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="text-2xl font-bold text-slate-900 mb-2">ফলাফল অনুসন্ধান</h3>
                  <p class="text-slate-600">৪৭তম কেন্দ্রীয় পরীক্ষার সকল মারহালার ফলাফল দেখুন</p>
                </div>
              </div>

              <!-- Form Section -->
              <div class="bg-slate-50/80 backdrop-blur-sm border border-slate-200/60 rounded-xl p-6 mb-6">
                <form class="space-y-4">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <select class="w-full bg-white border border-slate-200 rounded-lg px-4 py-3 text-slate-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all">
                      <option value="" disabled selected>মারহালা নির্বাচন করুন</option>
                      <option value="1">ইবতিদাইয়্যাহ</option>
                      <option value="2">মুতাওয়াসসিতাহ</option>
                      <option value="3">সানাবিয়্যাহ আম্মাহ</option>
                      <option value="4">ফাজিল</option>
                      <option value="5">কামিল</option>
                    </select>

                    <select class="w-full bg-white border border-slate-200 rounded-lg px-4 py-3 text-slate-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all">
                      <option value="" disabled selected>সন নির্বাচন করুন</option>
                      <option value="2025">২০২৫</option>
                      <option value="2024">২০২৪</option>
                      <option value="2023">২০২৩</option>
                    </select>
                  </div>

                  <input
                    type="text"
                    placeholder="রোল নম্বর লিখুন"
                    class="w-full bg-white border border-slate-200 rounded-lg px-4 py-3 text-slate-700 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                  >
                </form>
              </div>

              <!-- Stats -->
              <div class="flex items-center justify-between text-sm text-slate-500 mb-6">
                <div class="flex items-center gap-2">
                  <div class="w-2 h-2 bg-emerald-500 rounded-full"></div>
                  <span>৩,৫৬,৮২৪ জন দেখেছেন</span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-2 h-2 bg-emerald-500 rounded-full"></div>
                  <span>১৭-০৭-২০২৫ প্রকাশিত</span>
                </div>
              </div>

              <!-- CTA Button -->
              <button class="w-full bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-700 hover:to-emerald-800 text-white font-semibold py-4 px-6 rounded-xl shadow-lg hover:shadow-emerald-500/25 transition-all duration-300 transform hover:scale-105">
                ফলাফল দেখুন
              </button>
            </div>
          </div>

          <!-- Student Portal Card -->
          <div class="bg-white/70 backdrop-blur-sm border border-slate-200/60 rounded-2xl p-8 shadow-sm hover:shadow-lg transition-all duration-300 group">
            <!-- Header -->
            <div class="flex items-start gap-6 mb-6">
              <div class="w-16 h-16 bg-gradient-to-br from-teal-100 to-teal-200 rounded-2xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform duration-300">
                <svg class="w-8 h-8 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
              </div>
              <div class="flex-1">
                <h3 class="text-2xl font-bold text-slate-900 mb-2">তালিবুল ইলম পোর্টাল</h3>
                <p class="text-slate-600">ব্যক্তিগত প্রোফাইল ব্যবস্থাপনা ও একাডেমিক সেবাসমূহ</p>
              </div>
            </div>

            <!-- Features List -->
            <div class="bg-slate-50/80 backdrop-blur-sm border border-slate-200/60 rounded-xl p-6 mb-6">
              <div class="space-y-4">
                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 bg-gradient-to-br from-emerald-100 to-emerald-200 rounded-xl flex items-center justify-center flex-shrink-0">
                    <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                    </svg>
                  </div>
                  <span class="text-slate-700 font-medium">প্রোফাইল ও তথ্য আপডেট সিস্টেম</span>
                </div>

                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 bg-gradient-to-br from-teal-100 to-teal-200 rounded-xl flex items-center justify-center flex-shrink-0">
                    <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                  </div>
                  <span class="text-slate-700 font-medium">সনদ ও সার্টিফিকেট অনলাইন আবেদন</span>
                </div>

                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 bg-gradient-to-br from-emerald-100 to-emerald-200 rounded-xl flex items-center justify-center flex-shrink-0">
                    <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                  </div>
                  <span class="text-slate-700 font-medium">মার্কশীট ও ট্রান্সক্রিপ্ট ডাউনলোড</span>
                </div>

                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 bg-gradient-to-br from-teal-100 to-teal-200 rounded-xl flex items-center justify-center flex-shrink-0">
                    <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5-5-5h5v-5a7.5 7.5 0 01-7.5-7.5C3.5 5.5 3.5 5.5 3.5 5.5S2 6 2 7.5a7.5 7.5 0 017.5 7.5v5z"/>
                    </svg>
                  </div>
                  <span class="text-slate-700 font-medium">রিয়েল-টাইম নোটিফিকেশন সিস্টেম</span>
                </div>
              </div>
            </div>

            <!-- User Status -->
            <div class="flex items-center justify-between text-sm text-slate-500 mb-6">
              <div class="flex items-center gap-2">
                <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                <span>{{ userStatus }}</span>
              </div>
              <div class="flex items-center gap-2">
                <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
                <span>৩ টি নতুন আপডেট</span>
              </div>
            </div>

            <!-- CTA Button -->
            <button class="w-full bg-gradient-to-r from-teal-600 to-teal-700 hover:from-teal-700 hover:to-teal-800 text-white font-semibold py-4 px-6 rounded-xl shadow-lg hover:shadow-teal-500/25 transition-all duration-300 transform hover:scale-105">
              পোর্টালে প্রবেশ করুন
            </button>
          </div>
        </div>

        <!-- News Ticker -->
        <div class="bg-white/70 backdrop-blur-sm border border-slate-200/60 rounded-2xl shadow-sm overflow-hidden">
          <div class="bg-gradient-to-r from-emerald-600 to-emerald-700 px-6 py-4 flex items-center">
            <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center mr-4">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h4 class="text-xl font-bold text-white">সর্বশেষ আপডেট ও ঘোষণা</h4>
          </div>

          <div class="relative h-16 overflow-hidden bg-slate-50/80">
            <div class="ticker-container absolute inset-0 flex items-center">
              <div class="ticker-content animate-ticker flex items-center whitespace-nowrap">
                <div class="flex items-center mx-8 text-slate-700">
                  <div class="w-3 h-3 bg-emerald-500 rounded-full mr-3"></div>
                  <span class="text-lg font-medium">৪৭তম কেন্দ্রীয় পরীক্ষার ফলাফল প্রকাশিত - ১৭/০৭/২০২৫</span>
                </div>

                <div class="flex items-center mx-8 text-slate-700">
                  <div class="w-3 h-3 bg-teal-500 rounded-full mr-3"></div>
                  <span class="text-lg font-medium">৪৮তম কেন্দ্রীয় পরীক্ষার নিবন্ধন চলমান - সময়সীমা বর্ধিত</span>
                </div>

                <div class="flex items-center mx-8 text-slate-700">
                  <div class="w-3 h-3 bg-emerald-500 rounded-full mr-3"></div>
                  <span class="text-lg font-medium">নতুন সিলেবাস ও গাইডলাইন প্রকাশিত - আপডেট করুন</span>
                </div>

                <div class="flex items-center mx-8 text-slate-700">
                  <div class="w-3 h-3 bg-teal-500 rounded-full mr-3"></div>
                  <span class="text-lg font-medium">অনলাইন ক্লাস ও ওয়েবিনার সিরিজ শুরু হচ্ছে শীঘ্রই</span>
                </div>
              </div>

              <!-- Duplicate for seamless loop -->
              <div class="ticker-content animate-ticker flex items-center whitespace-nowrap">
                <div class="flex items-center mx-8 text-slate-700">
                  <div class="w-3 h-3 bg-emerald-500 rounded-full mr-3"></div>
                  <span class="text-lg font-medium">৪৭তম কেন্দ্রীয় পরীক্ষার ফলাফল প্রকাশিত - ১৭/০৭/২০২৫</span>
                </div>

                <div class="flex items-center mx-8 text-slate-700">
                  <div class="w-3 h-3 bg-teal-500 rounded-full mr-3"></div>
                  <span class="text-lg font-medium">৪৮তম কেন্দ্রীয় পরীক্ষার নিবন্ধন চলমান - সময়সীমা বর্ধিত</span>
                </div>

                <div class="flex items-center mx-8 text-slate-700">
                  <div class="w-3 h-3 bg-emerald-500 rounded-full mr-3"></div>
                  <span class="text-lg font-medium">নতুন সিলেবাস ও গাইডলাইন প্রকাশিত - আপডেট করুন</span>
                </div>

                <div class="flex items-center mx-8 text-slate-700">
                  <div class="w-3 h-3 bg-teal-500 rounded-full mr-3"></div>
                  <span class="text-lg font-medium">অনলাইন ক্লাস ও ওয়েবিনার সিরিজ শুরু হচ্ছে শীঘ্রই</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Trust Indicators -->
        <div class="mt-20 pt-12 border-t border-slate-200/60">
          <div class="text-center mb-8">
            <p class="text-sm font-medium text-slate-500 uppercase tracking-wide">আমাদের বিশ্বস্ত অংশীদার</p>
          </div>

          <div class="flex flex-wrap items-center justify-center gap-12 opacity-60">
            <!-- Government Badge -->
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 bg-slate-100 rounded-xl flex items-center justify-center">
                <svg class="w-6 h-6 text-slate-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/>
                </svg>
              </div>
              <span class="text-sm font-medium text-slate-600">সরকার অনুমোদিত</span>
            </div>

            <!-- Digital Badge -->
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 bg-slate-100 rounded-xl flex items-center justify-center">
                <svg class="w-6 h-6 text-slate-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M4 6h16v2H4zm0 5h16v2H4zm0 5h16v2H4z"/>
                </svg>
              </div>
              <span class="text-sm font-medium text-slate-600">ডিজিটাল বাংলাদেশ</span>
            </div>

            <!-- Security Badge -->
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 bg-slate-100 rounded-xl flex items-center justify-center">
                <svg class="w-6 h-6 text-slate-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/>
                </svg>
              </div>
              <span class="text-sm font-medium text-slate-600">নিরাপদ ও সুরক্ষিত</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'

const isLoggedIn = ref(true)
const username = ref('tahsin866')
const userStatus = computed(() =>
  isLoggedIn.value ? `${username.value} হিসাবে সক্রিয় আছেন` : 'লগইন প্রয়োজন'
)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Ticker Animation */
@keyframes ticker {
  0% { transform: translateX(0); }
  100% { transform: translateX(-100%); }
}

.animate-ticker {
  animation: ticker 45s linear infinite;
}

.ticker-container {
  position: relative;
  overflow: hidden;
}

.ticker-content {
  display: inline-flex;
  padding-right: 100%;
  align-items: center;
}

/* Smooth transitions */
* {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
