<template>
    <div class="mb-6">
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
            <div class="p-6 bg-white border-b border-gray-200">
                <label class="block font-medium text-sm text-gray-700 mb-2"> মারকায প্রাপ্তির প্রয়োজনীয়তা </label>
                <textarea :value="modelValue" @input="$emit('update:modelValue', $event.target.value)" class="border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 rounded-md shadow-sm mt-1 block w-full" rows="4"></textarea>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { defineProps } from 'vue';
const props = defineProps({ modelValue: String });
</script>
