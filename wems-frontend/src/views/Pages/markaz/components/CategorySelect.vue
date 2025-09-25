<template>
  <div class="mb-6">
    <label class="block font-bold text-lg text-gray-700 mb-2 flex items-center">
      <i class="fas fa-layer-group mr-2 text-indigo-400"></i>
      মারকাযের স্তর নির্বাচন করুন <span class="text-red-500 ml-1">*</span>
    </label>
    <select
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
      class="border border-gray-400 focus:border-indigo-500 focus:ring-indigo-500 rounded shadow bg-white px-4 py-3 text-lg block w-full transition-all font-bold text-gray-800"
    >
      <option value="" class="text-md">নির্বাচন করুন</option>
      <option value="দরসিয়াত">দরসিয়াত</option>
      <option value="তাহফিজুল কোরআন">তাহফিজুল কোরআন</option>
      <option value="কিরাআত">কিরাআত</option>
    </select>
    <p v-if="!modelValue" class="text-md text-red-500 mt-1">
      <i class="fas fa-exclamation-circle mr-1"></i>
      মারকাযের স্তর নির্বাচন করুন
    </p>
  </div>
</template>

<script setup lang="ts">
import { defineEmits, defineProps } from 'vue';
const props = defineProps({ modelValue: String });
defineEmits(['update:modelValue']);
</script>
