<template>
  <div class="p-8 bg-blue-50">
    <h1 class="text-2xl font-bold text-blue-900">মারকায তালিকা টেস্ট পেজ</h1>
    <p class="mt-4 text-blue-700">এই পেজটি দেখা যাচ্ছে মানে router ঠিক আছে।</p>
    <div class="mt-6 p-4 bg-white rounded border">
      <p>Current Route: {{ $route.path }}</p>
      <p>Route Name: {{ $route.name }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
// Simple test component with no dependencies
</script>
