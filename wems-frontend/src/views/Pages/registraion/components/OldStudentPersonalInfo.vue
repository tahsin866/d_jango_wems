<template>
  <div
    class="rounded border shadow"
    :class="[!isDark ? 'bg-white' : 'bg-gray-800']"
  >
    <div
      class="flex bg-gray-800 rounded-t gap-3 items-center px-6 py-3"
    >
      <i class="text-2xl text-gray-300 fa-user-circle fas"></i>
      <h5 class="text-gray-200 text-xl">ব্যক্তিগত তথ্য</h5>
    </div>

    <div class="p-6">
      <!-- নাম -->
      <div class="grid grid-cols-1 gap-6 mb-6 md:grid-cols-3">
        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-1">নাম (বাংলা)</label>
          <input v-model="local.name_bn" type="text" disabled
            :class="[!isDark ? 'bg-gray-100 border border-gray-300 text-gray-700' : 'bg-gray-700 border border-gray-600 text-gray-300', 'rounded w-full cursor-not-allowed pl-10 pr-3 py-2']" />
          <p :class="[!isDark ? 'text-gray-500' : 'text-gray-400']" class="text-xs italic mt-1">* এই ফিল্ডটি পরিবর্তন করা যাবে না</p>
        </div>

        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-1">নাম (ইংরেজি)</label>
          <input v-model="local.name_en" type="text"
            :class="[!isDark ? 'border border-gray-300' : 'border border-gray-600', 'rounded w-full focus:outline-none focus:ring-2 focus:ring-gray-500 pl-10 pr-3 py-2', isDark ? 'bg-gray-700 text-gray-300' : '']" />
        </div>

        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-1">নাম (আরবি)</label>
          <input v-model="local.name_ar" type="text" dir="rtl"
            :class="[!isDark ? 'border border-gray-300' : 'border border-gray-600', 'rounded w-full focus:outline-none focus:ring-2 focus:ring-gray-500 pl-10 pr-3 py-2', isDark ? 'bg-gray-700 text-gray-300' : '']" />
        </div>
      </div>

      <!-- পিতার নাম -->
      <div class="grid grid-cols-1 gap-6 mb-6 md:grid-cols-3">
        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-1">পিতার নাম (বাংলা)</label>
          <input v-model="local.father_name_bn" type="text" disabled
            :class="[!isDark ? 'bg-gray-100 border border-gray-300 text-gray-700' : 'bg-gray-700 border border-gray-600 text-gray-300', 'rounded w-full cursor-not-allowed pl-10 pr-3 py-2']" />
          <p :class="[!isDark ? 'text-gray-500' : 'text-gray-400']" class="text-xs italic mt-1">* এই ফিল্ডটি পরিবর্তন করা যাবে না</p>
        </div>

        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-1">পিতার নাম (ইংরেজি)</label>
          <input v-model="local.father_name_en" type="text"
            :class="[!isDark ? 'border border-gray-300' : 'border border-gray-600', 'rounded w-full focus:outline-none focus:ring-2 focus:ring-gray-500 pl-10 pr-3 py-2', isDark ? 'bg-gray-700 text-gray-300' : '']" />
        </div>

        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-1">পিতার নাম (আরবি)</label>
          <input v-model="local.father_name_ar" type="text" dir="rtl"
            :class="[!isDark ? 'border border-gray-300' : 'border border-gray-600', 'rounded w-full focus:outline-none focus:ring-2 focus:ring-gray-500 pl-10 pr-3 py-2', isDark ? 'bg-gray-700 text-gray-300' : '']" />
        </div>
      </div>

      <!-- মাতার নাম -->
      <div class="grid grid-cols-1 gap-6 mb-6 md:grid-cols-3">
        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-1">মাতার নাম (বাংলা)</label>
          <input v-model="local.mother_name_bn" type="text"
            :class="[!isDark ? 'border border-gray-300 text-gray-700' : 'border border-gray-600 bg-gray-700 text-gray-300', 'rounded w-full pl-10 pr-3 py-2']" />
        </div>

        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-1">মাতার নাম (ইংরেজি)</label>
          <input v-model="local.mother_name_en" type="text"
            :class="[!isDark ? 'border border-gray-300' : 'border border-gray-600', 'rounded w-full focus:outline-none focus:ring-2 focus:ring-gray-500 pl-10 pr-3 py-2', isDark ? 'bg-gray-700 text-gray-300' : '']" />
        </div>

        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-1">মাতার নাম (আরবি)</label>
          <input v-model="local.mother_name_ar" type="text" dir="rtl"
            :class="[!isDark ? 'border border-gray-300' : 'border border-gray-600', 'rounded w-full focus:outline-none focus:ring-2 focus:ring-gray-500 pl-10 pr-3 py-2', isDark ? 'bg-gray-700 text-gray-300' : '']" />
        </div>
      </div>

      <!-- জন্ম-তারিখ, জন্ম-নিবন্ধন ও NID -->
      <div class="grid grid-cols-1 gap-6 mb-6 md:grid-cols-3">
        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-1">জন্ম-তারিখ</label>
          <input v-model="local.Date_of_birth" type="date" disabled
            :class="[!isDark ? 'border border-gray-300' : 'border border-gray-600 bg-gray-700 text-gray-300', 'rounded w-full pl-10 pr-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-500']" />
        </div>

        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-1">জন্ম-নিবন্ধন নম্বর</label>
          <input v-model="local.BRN_no" type="text"
            :class="[!isDark ? 'border border-gray-300' : 'border border-gray-600 bg-gray-700 text-gray-300', 'rounded w-full pl-10 pr-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-500']" />
        </div>

        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-1">জাতীয় পরিচয়পত্র নম্বর</label>
          <input v-model="local.NID_no" type="text"
            :class="[!isDark ? 'border border-gray-300' : 'border border-gray-600 bg-gray-700 text-gray-300', 'rounded w-full pl-10 pr-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-500']" />
        </div>
      </div>

      <!-- ফোন নম্বর -->
      <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
        <div class="relative">
          <label :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-1">অভিভাবকের ফোন নম্বর</label>
          <input v-model="local.mobile_no" type="tel"
            :class="[!isDark ? 'border border-gray-300' : 'border border-gray-600 bg-gray-700 text-gray-300', 'rounded w-full pl-10 pr-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-500']" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue';

type StudentInfo = {
  name_bn?: string;
  name_en?: string;
  name_ar?: string;
  father_name_bn?: string;
  father_name_en?: string;
  father_name_ar?: string;
  mother_name_bn?: string;
  mother_name_en?: string;
  mother_name_ar?: string;
  Date_of_birth?: string;
  BRN_no?: string;
  NID_no?: string;
  mobile_no?: string;
  [key: string]: any;
};

const props = defineProps<{
  modelValue?: StudentInfo;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: StudentInfo): void;
}>();

const isDark = computed(() => document.documentElement.classList.contains('dark'));

// local reactive copy to avoid mutating prop directly
const local = reactive<StudentInfo>({
  name_bn: props.modelValue?.name_bn ?? '',
  name_en: props.modelValue?.name_en ?? '',
  name_ar: props.modelValue?.name_ar ?? '',
  father_name_bn: props.modelValue?.father_name_bn ?? '',
  father_name_en: props.modelValue?.father_name_en ?? '',
  father_name_ar: props.modelValue?.father_name_ar ?? '',
  mother_name_bn: props.modelValue?.mother_name_bn ?? '',
  mother_name_en: props.modelValue?.mother_name_en ?? '',
  mother_name_ar: props.modelValue?.mother_name_ar ?? '',
  Date_of_birth: props.modelValue?.Date_of_birth ?? '',
  BRN_no: props.modelValue?.BRN_no ?? '',
  NID_no: props.modelValue?.NID_no ?? '',
  mobile_no: props.modelValue?.mobile_no ?? ''
});

// keep local in sync when parent changes modelValue
watch(
  () => props.modelValue,
  (newVal) => {
    if (!newVal) return;
    Object.assign(local, {
      name_bn: newVal.name_bn ?? '',
      name_en: newVal.name_en ?? '',
      name_ar: newVal.name_ar ?? '',
      father_name_bn: newVal.father_name_bn ?? '',
      father_name_en: newVal.father_name_en ?? '',
      father_name_ar: newVal.father_name_ar ?? '',
      mother_name_bn: newVal.mother_name_bn ?? '',
      mother_name_en: newVal.mother_name_en ?? '',
      mother_name_ar: newVal.mother_name_ar ?? '',
      Date_of_birth: newVal.Date_of_birth ?? '',
      BRN_no: newVal.BRN_no ?? '',
      NID_no: newVal.NID_no ?? '',
      mobile_no: newVal.mobile_no ?? ''
    });
  },
  { deep: true, immediate: true }
);

// emit updates when local changes
watch(
  local,
  (val) => {
    emit('update:modelValue', { ...val });
  },
  { deep: true }
);
</script>

<style scoped>
/* All styling is Tailwind CSS utilities only. */
</style>
