<template>
  <div class="mb-6">
    <div class="bg-white rounded border border-gray-300 shadow-lg">
      <div class="p-8 border-b border-gray-200">
        <label class="block font-bold text-lg text-gray-700 mb-3 flex items-center">
          <i class="fas fa-clipboard-list mr-2 text-indigo-400"></i>
          মারকায প্রাপ্তির প্রয়োজনীয়তা
        </label>
        <textarea
          :value="modelValue"
          @input="$emit('update:modelValue', $event.target.value)"
          class="border border-gray-400 focus:border-indigo-500 focus:ring-indigo-500 rounded-lg shadow px-4 py-3 mt-1 block w-full text-gray-800 font-semibold bg-gray-50"
          rows="4"
        ></textarea>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { defineProps } from 'vue';
const props = defineProps({ modelValue: String });
</script>
