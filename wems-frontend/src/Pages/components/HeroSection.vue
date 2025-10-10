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
      <div class="w-full h-full border-2 border-slate-400 rounded-2xl transform rotate-12"></div>
    </div>
    <div class="absolute bottom-20 left-10 w-24 h-24 opacity-5">
      <div class="w-full h-full bg-emerald-200 rounded-full transform -rotate-12"></div>
    </div>

    <div class="container mx-auto px-6 lg:px-8 relative z-10">
      <div class="max-w-5xl mx-auto">

        <!-- Top Badge -->
        <div class="flex justify-center mb-12">
          <div class="inline-flex items-center gap-2 bg-white/80 backdrop-blur-sm border border-slate-200/80 rounded-full px-6 py-2.5 shadow-sm">
            <div class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
            <span class="text-sm font-medium text-slate-600">বাংলাদেশের শীর্ষস্থানীয় কওমি শিক্ষা প্রতিষ্ঠান</span>
          </div>
        </div>


        <!-- Main Heading -->
        <div class="text-center mb-8">
          <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-slate-900 leading-[1.1] tracking-tight">
            বেফাকুল মাদারিসিল   আরাবিয়া বাংলাদেশ
          </h1>
        </div>

        <!-- Subtitle -->
        <div class="text-center mb-12">
          <div class="inline-block bg-white/90 backdrop-blur-sm border border-slate-200/60 rounded-2xl px-8 py-4 shadow-sm">
            <h2 class="text-lg md:text-xl text-slate-700 font-medium">
              বাংলাদেশ কওমী মাদরাসা শিক্ষাবোর্ড
            </h2>
          </div>
        </div>

        <!-- Description -->
        <div class="text-center mb-16 max-w-3xl mx-auto">
          <p class="text-lg md:text-xl text-slate-600 leading-relaxed">
            ঐতিহ্যবাহী ইসলামিক শিক্ষা ব্যবস্থার আধুনিকায়ন এবং ডিজিটাল প্রযুক্তির মাধ্যমে
            মানসম্পন্ন শিক্ষা নিশ্চিতকরণে বেফাকুল মাদারিসিল আরাবিয়া বাংলাদেশ কাজ করে যাচ্ছে।
          </p>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <div class="bg-white/70 backdrop-blur-sm border border-slate-200/60 rounded-2xl p-8 text-center shadow-sm hover:shadow-md transition-all duration-300 group">
            <div class="w-16 h-16 bg-gradient-to-br from-emerald-100 to-emerald-200 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
              <svg class="w-8 h-8 text-emerald-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              </svg>
            </div>
            <div class="text-3xl font-bold text-slate-900 mb-2">১৫,০০০+</div>
            <div class="text-slate-600 font-medium">নিবন্ধিত মাদরাসা</div>
          </div>

          <div class="bg-white/70 backdrop-blur-sm border border-slate-200/60 rounded-2xl p-8 text-center shadow-sm hover:shadow-md transition-all duration-300 group">
            <div class="w-16 h-16 bg-gradient-to-br from-blue-100 to-blue-200 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
              <svg class="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M16 4c0-1.11.89-2 2-2s2 .89 2 2-.89 2-2 2-2-.89-2-2zm4 18v-6h2.5l-2.54-7.63A2.95 2.95 0 0 0 17.06 7H16c-.8 0-1.54.37-2.01.99L12 10l-1.99-2.01A2.99 2.99 0 0 0 8 7H6.94c-1.4 0-2.6.99-2.9 2.37L1.5 16H4v6h16zM12.5 11.5L15 16h-3l-1.5-4.5z"/>
              </svg>
            </div>
            <div class="text-3xl font-bold text-slate-900 mb-2">৫ লাখ+</div>
            <div class="text-slate-600 font-medium">শিক্ষক-শিক্ষার্থী</div>
          </div>

          <div class="bg-white/70 backdrop-blur-sm border border-slate-200/60 rounded-2xl p-8 text-center shadow-sm hover:shadow-md transition-all duration-300 group">
            <div class="w-16 h-16 bg-gradient-to-br from-purple-100 to-purple-200 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
              <svg class="w-8 h-8 text-purple-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
              </svg>
            </div>
            <div class="text-3xl font-bold text-slate-900 mb-2">১৯৭৮</div>
            <div class="text-slate-600 font-medium">প্রতিষ্ঠার বছর</div>
          </div>
        </div>

        <!-- CTA Section -->
        <div class="text-center">
          <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a
              href="/dashboard"
              class="group inline-flex items-center gap-3 bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-700 hover:to-emerald-800 text-white font-semibold px-8 py-4 rounded-xl shadow-lg hover:shadow-emerald-500/25 transition-all duration-300 transform hover:scale-105"
            >
              <span>সিস্টেমে প্রবেশ করুন</span>
              <svg class="w-5 h-5 transition-transform duration-300 group-hover:translate-x-1" fill="currentColor" viewBox="0 0 24 24">
                <path d="M4 12h12m0 0l-4-4m4 4l-4 4"/>
              </svg>
            </a>

            <a
              href="#about"
              class="inline-flex items-center gap-3 bg-white/80 hover:bg-white text-slate-700 hover:text-slate-900 font-semibold px-8 py-4 rounded-xl border border-slate-200 hover:border-slate-300 shadow-sm hover:shadow-md transition-all duration-300"
            >
              <span>আরও জানুন</span>
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </a>
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
                  <path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm4 0h2v-2H7v2zm0-4h2v-2H7v2zm4 0h2v-2h-2v2zm0 4h2v-2h-2v2zm4 0h2v-2h-2v2zm0-4h2v-2h-2v2z"/>
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

<script setup lang="ts">
// Clean, professional component with no unnecessary JavaScript
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
</style>
