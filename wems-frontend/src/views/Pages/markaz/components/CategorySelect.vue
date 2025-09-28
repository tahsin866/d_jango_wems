<template>
  <div class="mb-8">
    <label class="block font-semibold text-gray-800 mb-3 flex items-center text-lg">
      <i class="fas fa-layer-group mr-3 text-blue-700"></i>
      মারকাযের স্তর নির্বাচন করুন <span class="text-red-500 ml-2">*</span>
    </label>
    <div class="relative">
      <select
        :value="modelValue"
        @change="$emit('update:modelValue', $event.target.value)"
        class="appearance-none w-full bg-white border-2 border-gray-300 rounded-sm py-4 px-5 text-gray-800 font-medium text-lg leading-tight focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 shadow-sm transition-all duration-200"
      >
        <option value="" class="text-gray-500">নির্বাচন করুন</option>
        <option value="দরসিয়াত">দরসিয়াত</option>
        <option value="তাহফিজুল কোরআন">তাহফিজুল কোরআন</option>
        <option value="কিরাআত">কিরাআত</option>
      </select>
      <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-gray-700">
        <i class="fas fa-chevron-down text-xl"></i>
      </div>
    </div>
    <p v-if="!modelValue" class="text-red-500 mt-2 flex items-center">
      <i class="fas fa-exclamation-circle mr-2"></i>
      <span class="font-medium">মারকাযের স্তর নির্বাচন করুন</span>
    </p>
  </div>
</template>

<script setup lang="ts">
import { defineEmits, defineProps } from 'vue';
const props = defineProps({ modelValue: String });
defineEmits(['update:modelValue']);
</script>
