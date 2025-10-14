<template>
  <section
    style="font-family: 'Merriweather', 'SolaimanLipi', sans-serif;"
    class="py-16 bg-gradient-to-r from-emerald-50 to-emerald-100 relative overflow-hidden"
  >
    <!-- Decorative Background -->
    <div class="absolute inset-0 opacity-10 pointer-events-none">
      <svg class="w-full h-full" preserveAspectRatio="none">
        <pattern id="faq-video-pattern" x="0" y="0" width="60" height="60" patternUnits="userSpaceOnUse">
          <path d="M30 0L60 30L30 60L0 30z" stroke="currentColor" stroke-width="0.5" class="text-emerald-900" fill="none"/>
          <circle cx="30" cy="30" r="10" stroke="currentColor" stroke-width="0.5" class="text-emerald-900" fill="none"/>
          <circle cx="30" cy="30" r="5" stroke="currentColor" stroke-width="0.5" class="text-emerald-900" fill="none"/>
        </pattern>
        <rect width="100%" height="100%" fill="url(#faq-video-pattern)" />
      </svg>
    </div>
    <div class="absolute top-12 left-12 w-32 h-32 bg-emerald-300/20 rounded-full blur-2xl"></div>
    <div class="absolute bottom-12 right-12 w-48 h-48 bg-teal-300/20 rounded-full blur-3xl"></div>

    <div class="container mx-auto grid grid-cols-1 md:grid-cols-2 gap-8 relative z-10">
      <!-- FAQ Section -->
      <div class="bg-white/90 p-8 rounded-2xl shadow-xl hover:shadow-emerald-400/20 transition-all duration-300">
        <div class="flex items-center mb-6">
          <div class="w-10 h-10 mr-4">
            <svg class="text-emerald-600 w-full h-full" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-4h2v2h-2zm1.61-9.96c-2.06-.3-3.88.97-4.43 2.79-.18.58.26 1.17.87 1.17h.2c.41 0 .74-.29.88-.67.32-.89 1.27-1.5 2.3-1.28.95.2 1.65 1.13 1.57 2.1-.1 1.34-1.62 1.63-2.45 2.88 0 .01-.01.01-.01.02-.01.02-.02.03-.03.05-.09.15-.18.32-.25.5-.01.03-.03.05-.04.08-.01.02-.01.04-.02.07-.12.34-.2.75-.2 1.25h2c0-.42.11-.77.28-1.07.02-.03.03-.06.05-.09.08-.14.18-.27.28-.39.01-.01.02-.03.03-.04.1-.12.21-.23.33-.34.96-.91 2.26-1.65 1.99-3.56-.24-1.74-1.61-3.21-3.35-3.47z"/>
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-emerald-800">মাদরাসা নির্দেশিকা</h3>
        </div>
        <div class="space-y-4">
          <div v-for="(faq, index) in faqs" :key="index" class="border-b border-emerald-100 last:border-0">
            <button
              class="w-full py-4 text-left flex justify-between items-center hover:text-emerald-600 transition-colors duration-300"
              @click="toggleFAQ(index)">
              <span class="font-semibold text-lg">{{ faq.question }}</span>
              <span class="transform transition-transform duration-300"
                    :class="{ 'rotate-180': activeFAQ === index }">
                ▼
              </span>
            </button>
            <div v-show="activeFAQ === index"
                 class="p-4 bg-emerald-50 rounded-lg mb-4 text-gray-700 transition-all duration-500">
              {{ faq.answer }}
            </div>
          </div>
        </div>
      </div>
      <!-- Video Tutorial Section -->
      <div class="bg-white/90 p-8 rounded-2xl shadow-xl hover:shadow-teal-400/20 transition-all duration-300">
        <div class="flex items-center mb-6">
          <div class="w-10 h-10 mr-4">
            <svg class="text-emerald-600 w-full h-full" fill="currentColor" viewBox="0 0 24 24">
              <path d="M21 3H3c-1.11 0-2 .89-2 2v12c0 1.1.89 2 2 2h5v2h8v-2h5c1.1 0 1.99-.9 1.99-2L23 5c0-1.11-.9-2-2-2zm0 14H3V5h18v12z"/>
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-emerald-800">ভিডিও নির্দেশনা</h3>
        </div>
        <div class="relative aspect-video rounded-xl overflow-hidden shadow-lg mb-6">
          <iframe
            class="w-full h-full absolute inset-0"
            src="https://www.youtube.com/embed/your-video-id"
            title="Tutorial Video"
            allowfullscreen
            loading="lazy">
          </iframe>
        </div>
        <h4 class="font-semibold text-lg text-emerald-800 mb-2">সম্পর্কিত ভিডিও সমূহ</h4>
        <div class="grid grid-cols-2 gap-4">
          <div v-for="n in 2" :key="n"
               class="p-3 bg-emerald-50 rounded-lg cursor-pointer hover:bg-emerald-100 transition-colors duration-300">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-emerald-600 rounded-full flex items-center justify-center text-white font-bold">
                {{ n }}
              </div>
              <span class="ml-3 text-sm">অতিরিক্ত টিউটোরিয়াল {{ n }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
const faqs = [
  {
    question: 'যেভাবে নিবন্ধন করবেন',
    answer: 'নিবন্ধনের জন্য নির্দেশনা...'
  },
  {
    question: 'ফলাফল কিভাবে দেখবেন',
    answer: 'ফলাফল দেখার জন্য নির্দেশনা...'
  },
  {
    question: 'সনদ আবেদন প্রক্রিয়া',
    answer: 'সনদ আবেদনের বিস্তারিত প্রক্রিয়া...'
  },
  {
    question: 'যোগাযোগ মাধ্যম',
    answer: 'আমাদের সাথে যোগাযোগের বিভিন্ন মাধ্যম...'
  }
]
const activeFAQ = ref(null)
const toggleFAQ = (index) => {
  activeFAQ.value = activeFAQ.value === index ? null : index
}
</script>
