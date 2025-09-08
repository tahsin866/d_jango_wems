<template>
    <div class="mb-6">
        <label class="block font-medium text-xl text-gray-700 mb-2"> মারকাযের স্তর নির্বাচন করুন <span class="text-red-500">*</span> </label>
        <select :value="modelValue" @change="$emit('update:modelValue', $event.target.value)" class="border-gray-300 focus:border-emerald-500 focus:ring-emerald-500 rounded-lg shadow-sm mt-1 block w-full px-4 py-3 text-lg bg-white transition-all">
            <option value="" class="text-md">নির্বাচন করুন</option>
            <option value="দরসিয়াত">দরসিয়াত</option>
            <option value="তাহফিজুল কোরআন">তাহফিজুল কোরআন</option>
            <option value="কিরাআত">কিরাআত</option>
        </select>
        <p v-if="!modelValue" class="text-md text-red-500 mt-1">মারকাযের স্তর নির্বাচন করুন</p>
    </div>
</template>

<script setup lang="ts">
import { defineEmits, defineProps } from 'vue';
const props = defineProps({ modelValue: String });
defineEmits(['update:modelValue']);
</script>
