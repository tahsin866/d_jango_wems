<template>
  <div>
    <!-- Navbar -->
    <Navbar />

    <!-- Hero Section -->
    <HeroSection />

    <!-- Features Section -->
    <FeatureSection />

    <!-- Contact Section -->
    <ContactSection />

    <!-- FAQ and Video Section -->
    <FAQVideoSection />

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script setup>
import Navbar from '@/Pages/components/navbar.vue'
import HeroSection from '@/Pages/components/HeroSection.vue'
import FeatureSection from '@/Pages/components/FeatureSection.vue'
import ContactSection from '@/Pages/components/ContactSection.vue'
import FAQVideoSection from '@/Pages/components/FAQVideoSection.vue'
import Footer from '@/Pages/components/Footer.vue'
</script>
