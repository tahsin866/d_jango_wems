<template>
  <section
    class="py-20 relative overflow-hidden bg-gradient-to-br from-slate-50 via-gray-50 to-slate-100"
    style="font-family: 'Inter', 'SolaimanLipi', sans-serif;"
  >
    <!-- Subtle Grid Pattern Background -->
    <div class="absolute inset-0 opacity-[0.02]">
      <div
        class="absolute inset-0"
        style="background-image: linear-gradient(rgba(15, 23, 42, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(15, 23, 42, 0.03) 1px, transparent 1px); background-size: 40px 40px;"
      ></div>
    </div>

    <!-- Geometric Elements -->
    <div class="absolute top-20 right-20 w-32 h-32 opacity-5">
      <div class="w-full h-full border-2 border-slate-400 rounded-full"></div>
    </div>
    <div class="absolute bottom-32 left-16 w-24 h-24 opacity-5">
      <div class="w-full h-full bg-emerald-200 rounded-2xl transform rotate-45"></div>
    </div>

    <div class="container mx-auto px-6 lg:px-8 relative z-10">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <div class="inline-flex items-center gap-2 bg-white/80 backdrop-blur-sm border border-slate-200/80 rounded-full px-4 py-2 mb-6">
          <div class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
          <span class="text-sm font-medium text-slate-600">সিস্টেম পরিসংখ্যান</span>
        </div>

        <h2 class="text-3xl md:text-4xl font-bold text-slate-900 mb-4">
          বেফাকুল মাদারিসিল আরাবিয়া বাংলাদেশ
        </h2>
        <p class="text-lg text-slate-600 max-w-2xl mx-auto">
          বাংলাদেশের সবচেয়ে বড় কওমী মাদরাসা শিক্ষাবোর্ড এর সর্বশেষ পরিসংখ্যান এবং সেবাসমূহ
        </p>
      </div>

      <div class="grid grid-cols-1 xl:grid-cols-2 gap-8">
        <!-- Statistics Card -->
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-sm border border-slate-200/60 p-8 hover:shadow-lg transition-all duration-300">
          <div class="flex items-center gap-4 mb-8">
            <div class="w-14 h-14 bg-gradient-to-br from-emerald-100 to-emerald-200 rounded-2xl flex items-center justify-center">
              <svg class="w-7 h-7 text-emerald-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm4 0h2v-2H7v2zm0-4h2v-2H7v2zm4 0h2v-2h-2v2zm0 4h2v-2h-2v2zm4 0h2v-2h-2v2zm0-4h2v-2h-2v2z"/>
              </svg>
            </div>
            <div>
              <h3 class="text-2xl font-bold text-slate-900">পরিসংখ্যান</h3>
              <p class="text-slate-500">সর্বশেষ আপডেট: {{ formattedDate }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div
              v-for="stat in stats"
              :key="stat.title"
              class="bg-slate-50/80 backdrop-blur-sm p-6 rounded-md border border-slate-200/40 hover:border-slate-300/60 transition-all duration-300 group"
            >
              <div class="flex items-center justify-between mb-4">
                <h4 class="font-semibold text-slate-700">{{ stat.title }}</h4>
                <div class="w-10 h-10 rounded-md flex items-center justify-center bg-white/80 group-hover:bg-emerald-50 transition-colors duration-300">
                  <component :is="stat.icon" class="w-5 h-5 text-emerald-600"/>
                </div>
              </div>

              <div class="flex items-baseline gap-2 mb-3">
                <span class="text-3xl font-bold text-slate-900">
                  <animated-number :value="stat.value" />
                </span>
                <span class="text-sm text-slate-500">{{ stat.unit }}</span>
              </div>

              <div class="w-full bg-slate-200 rounded-full h-2">
                <div
                  class="bg-gradient-to-r from-emerald-500 to-emerald-600 h-2 rounded-full transition-all duration-1000"
                  :style="{width: `${stat.percentage}%`}"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Registration Card -->
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-sm border border-slate-200/60 p-8 hover:shadow-lg transition-all duration-300">
          <div class="flex items-center gap-4 mb-8">
            <div class="w-14 h-14 bg-gradient-to-br from-blue-100 to-blue-200 rounded-2xl flex items-center justify-center">
              <svg class="w-7 h-7 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
              </svg>
            </div>
            <div>
              <h3 class="text-2xl font-bold text-slate-900">মাদরাসা রেজিস্ট্রেশন</h3>
              <p class="text-slate-500">সহজ এবং দ্রুত প্রক্রিয়া</p>
            </div>
          </div>

          <!-- Benefits List -->
          <div class="bg-slate-50/80 backdrop-blur-sm rounded-md p-6 mb-8 border border-slate-200/40">
            <h4 class="font-semibold text-slate-700 mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-emerald-500" fill="currentColor" viewBox="0 0 24 24">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              প্রধান সুবিধাসমূহ
            </h4>
            <ul class="space-y-3">
              <li v-for="benefit in benefits" :key="benefit" class="flex items-start gap-3">
                <svg class="w-5 h-5 text-emerald-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.285 2l-11.285 11.567-5.286-5.011-3.714 3.716 9 8.728 15-15.285z"/>
                </svg>
                <span class="text-slate-600 leading-relaxed">{{ benefit }}</span>
              </li>
            </ul>
          </div>

          <!-- CTA Section -->
          <div class="space-y-4">
            <a
              href="/MadrashaCheck"
              class="w-full bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-700 hover:to-emerald-800 text-white font-semibold py-4 px-6 rounded-md transition-all duration-300 flex items-center justify-center gap-2 shadow-sm hover:shadow-lg hover:shadow-emerald-500/25 transform hover:scale-[1.02]"
            >
              <span>রেজিস্ট্রেশন করুন</span>
              <svg class="w-5 h-5 transition-transform duration-300 group-hover:translate-x-1" fill="currentColor" viewBox="0 0 24 24">
                <path d="M13.025 1l-2.847 2.828 6.176 6.176h-16.354v3.992h16.354l-6.176 6.176 2.847 2.828 10.975-11z"/>
              </svg>
            </a>

            <p class="text-center text-slate-500 text-sm">
              ইতিমধ্যে রেজিস্টার্ড?
              <a href="/login" class="text-emerald-600 font-medium hover:text-emerald-700 transition-colors duration-200">
                লগইন করুন
              </a>
            </p>
          </div>
        </div>
      </div>

      <!-- Testimonial Section -->
      <div class="mt-16">
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-sm border border-slate-200/60 p-8">
          <div class="text-center mb-8">
            <h3 class="text-2xl font-bold text-slate-900 mb-2">ব্যবহারকারীদের মতামত</h3>
            <p class="text-slate-600">আমাদের সিস্টেম ব্যবহারকারীদের অভিজ্ঞতা</p>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div v-for="testimonial in testimonials" :key="testimonial.name" class="bg-slate-50/80 backdrop-blur-sm rounded-md p-6 border border-slate-200/40">
              <div class="flex items-start gap-4">
                <div class="w-16 h-16 rounded-2xl overflow-hidden border-2 border-slate-200 flex-shrink-0">
                  <img :src="testimonial.image" :alt="testimonial.name" class="w-full h-full object-cover">
                </div>
                <div class="flex-1">
                  <div class="mb-4">
                    <svg class="w-8 h-8 text-emerald-200 mb-2" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/>
                    </svg>
                    <p class="text-slate-600 italic leading-relaxed">{{ testimonial.quote }}</p>
                  </div>
                  <div>
                    <p class="font-semibold text-slate-900">{{ testimonial.name }}</p>
                    <p class="text-sm text-emerald-600">{{ testimonial.title }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Trust Indicators -->
      <div class="mt-16 pt-12 border-t border-slate-200/60">
        <div class="text-center mb-8">
          <p class="text-sm font-medium text-slate-500 uppercase tracking-wide">বিশ্বস্ত এবং নিরাপদ</p>
        </div>
        <div class="flex flex-wrap items-center justify-center gap-12 opacity-60">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-slate-100 rounded-md flex items-center justify-center">
              <svg class="w-6 h-6 text-slate-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/>
              </svg>
            </div>
            <span class="text-sm font-medium text-slate-600">SSL সুরক্ষিত</span>
          </div>
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-slate-100 rounded-md flex items-center justify-center">
              <svg class="w-6 h-6 text-slate-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <span class="text-sm font-medium text-slate-600">সরকার অনুমোদিত</span>
          </div>
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-slate-100 rounded-md flex items-center justify-center">
              <svg class="w-6 h-6 text-slate-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M4 6h16v2H4zm0 5h16v2H4zm0 5h16v2H4z"/>
              </svg>
            </div>
            <span class="text-sm font-medium text-slate-600">২৪/৭ সেবা</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, defineComponent } from 'vue'

// Define icons as components
const StudentIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
    </svg>
  `
}

const MarkazIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
    </svg>
  `
}

const NegranIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
    </svg>
  `
}

const MumtahinIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
    </svg>
  `
}

// Animated Number Component
const AnimatedNumber = defineComponent({
  props: {
    value: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      displayValue: 0
    };
  },
  mounted() {
    this.animateValue(0, this.value, 1500);
  },
  methods: {
    animateValue(start, end, duration) {
      let startTimestamp = null;
      const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        this.displayValue = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
          window.requestAnimationFrame(step);
        }
      };
      window.requestAnimationFrame(step);
    }
  },
  template: `<span>{{ displayValue.toLocaleString() }}</span>`
});

// Current formatted date
const formattedDate = computed(() => {
  const date = new Date()
  return new Intl.DateTimeFormat('bn-BD', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
})

// Statistics data
const stats = [
  {
    title: 'পরীক্ষার্থী',
    value: 53543,
    unit: 'জন',
    icon: StudentIcon,
    percentage: 85
  },
  {
    title: 'মারকাজ',
    value: 3000,
    unit: '',
    icon: MarkazIcon,
    percentage: 70
  },
  {
    title: 'নেগরান',
    value: 4500,
    unit: 'জন',
    icon: NegranIcon,
    percentage: 65
  },
  {
    title: 'মুমতাহিন',
    value: 7800,
    unit: 'জন',
    icon: MumtahinIcon,
    percentage: 90
  }
]

// Benefits for madrasa signup
const benefits = [
  'অনলাইনে পরীক্ষার রেজিস্ট্রেশন করার সুবিধা',
  'মাদরাসার সকল ছাত্র-ছাত্রীদের তথ্য ডিজিটাল পদ্ধতিতে সংরক্ষণ',
  'রেজাল্ট অনলাইনে প্রকাশ এবং নিরীক্ষণ',
  'সার্টিফিকেট অনলাইন ভেরিফিকেশন সিস্টেম',
  'মাদরাসার সকল নোটিশ ও পরীক্ষার রুটিন সরাসরি পাওয়া'
]

// Testimonials
const testimonials = [
  {
    quote: "অনলাইন ম্যানেজমেন্ট সিস্টেমের কারণে আমাদের মাদরাসার অ্যাডমিনিস্ট্রেটিভ কাজের চাপ অনেক কমেছে এবং সময় বেঁচেছে।",
    name: "মাওলানা আব্দুল হামিদ",
    title: "মুহতামিম, জামিয়া আরাবিয়া ইসলামিয়া",
    image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face"
  },
  {
    quote: "পরীক্ষার ফলাফল এখন দ্রুত পাওয়া যায়, এছাড়া সার্টিফিকেট ভেরিফিকেশন সিস্টেম আমাদের অনেক উপকার করেছে।",
    name: "মাওলানা রফিকুল ইসলাম",
    title: "প্রিন্সিপাল, দারুল উলুম মাদরাসা",
    image: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face"
  }
]
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
</style>
