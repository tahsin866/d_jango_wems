<template>
  <Fieldset legend="ব্যক্তিগত তথ্য" :pt="{
    legend: { className: 'text-xl font-bold text-gray-200 bg-gray-800 px-6 py-3 rounded-t' },
    content: { className: 'p-6' }
  }">
    <template #legend>
      <div class="flex items-center gap-3">
        <i class="text-2xl text-gray-300 fa-user-circle fas"></i>
        <span class="text-gray-200 text-xl">ব্যক্তিগত তথ্য</span>
      </div>
    </template>

    <!-- নাম -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6 w-full">
      <div class="w-full">
        <label for="name_bn" :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-2">নাম (বাংলা)</label>
        <InputText
          id="name_bn"
          v-model="local.name_bn"
          :disabled="true"
          placeholder="নাম (বাংলা)"
          class="w-full"
          :pt="{
            root: { class: ['w-full', isDark ? 'bg-gray-700 border-gray-600 text-gray-300' : 'bg-gray-100 border-gray-300 text-gray-700'] }
          }"
        />
        <small :class="[!isDark ? 'text-gray-500' : 'text-gray-400']" class="block mt-1 italic">* এই ফিল্ডটি পরিবর্তন করা যাবে না</small>
      </div>

      <div class="w-full">
        <label for="name_en" :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-2">নাম (ইংরেজি)</label>
        <InputText
          id="name_en"
          v-model="local.name_en"
          placeholder="Name (English)"
          class="w-full"
          :pt="{
            root: { class: ['w-full', isDark ? 'bg-gray-700 border-gray-600 text-gray-300' : 'bg-white border-gray-300 text-gray-700'] }
          }"
        />
      </div>

      <div class="w-full">
        <label for="name_ar" :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-2">নাম (আরবি)</label>
        <InputText
          id="name_ar"
          v-model="local.name_ar"
          dir="rtl"
          placeholder="الاسم (العربية)"
          class="w-full"
          :pt="{
            root: { class: ['w-full', isDark ? 'bg-gray-700 border-gray-600 text-gray-300' : 'bg-white border-gray-300 text-gray-700'] }
          }"
        />
      </div>
    </div>

    <!-- পিতার নাম -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6 w-full">
      <div class="w-full">
        <label for="father_name_bn" :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-2">পিতার নাম (বাংলা)</label>
        <InputText
          id="father_name_bn"
          v-model="local.father_name_bn"
          :disabled="true"
          placeholder="পিতার নাম (বাংলা)"
          class="w-full"
          :pt="{
            root: { class: ['w-full', isDark ? 'bg-gray-700 border-gray-600 text-gray-300' : 'bg-gray-100 border-gray-300 text-gray-700'] }
          }"
        />
        <small :class="[!isDark ? 'text-gray-500' : 'text-gray-400']" class="block mt-1 italic">* এই ফিল্ডটি পরিবর্তন করা যাবে না</small>
      </div>

      <div class="w-full">
        <label for="father_name_en" :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-2">পিতার নাম (ইংরেজি)</label>
        <InputText
          id="father_name_en"
          v-model="local.father_name_en"
          placeholder="Father's Name (English)"
          class="w-full"
          :pt="{
            root: { class: ['w-full', isDark ? 'bg-gray-700 border-gray-600 text-gray-300' : 'bg-white border-gray-300 text-gray-700'] }
          }"
        />
      </div>

      <div class="w-full">
        <label for="father_name_ar" :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-2">পিতার নাম (আরবি)</label>
        <InputText
          id="father_name_ar"
          v-model="local.father_name_ar"
          dir="rtl"
          placeholder="اسم الأب (العربية)"
          class="w-full"
          :pt="{
            root: { class: ['w-full', isDark ? 'bg-gray-700 border-gray-600 text-gray-300' : 'bg-white border-gray-300 text-gray-700'] }
          }"
        />
      </div>
    </div>

    <!-- মাতার নাম -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6 w-full">
      <div class="w-full">
        <label for="mother_name_bn" :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-2">মাতার নাম (বাংলা)</label>
        <InputText
          id="mother_name_bn"
          v-model="local.mother_name_bn"
          placeholder="মাতার নাম (বাংলা)"
          class="w-full"
          :pt="{
            root: { class: ['w-full', isDark ? 'bg-gray-700 border-gray-600 text-gray-300' : 'bg-white border-gray-300 text-gray-700'] }
          }"
        />
      </div>

      <div class="w-full">
        <label for="mother_name_en" :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-2">মাতার নাম (ইংরেজি)</label>
        <InputText
          id="mother_name_en"
          v-model="local.mother_name_en"
          placeholder="Mother's Name (English)"
          class="w-full"
          :pt="{
            root: { class: ['w-full', isDark ? 'bg-gray-700 border-gray-600 text-gray-300' : 'bg-white border-gray-300 text-gray-700'] }
          }"
        />
      </div>

      <div class="w-full">
        <label for="mother_name_ar" :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-2">মাতার নাম (আরবি)</label>
        <InputText
          id="mother_name_ar"
          v-model="local.mother_name_ar"
          dir="rtl"
          placeholder="اسم الأم (العربية)"
          class="w-full"
          :pt="{
            root: { class: ['w-full', isDark ? 'bg-gray-700 border-gray-600 text-gray-300' : 'bg-white border-gray-300 text-gray-700'] }
          }"
        />
      </div>
    </div>

    <!-- জন্ম-তারিখ, জন্ম-নিবন্ধন ও NID -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6 w-full">
      <div class="w-full">
        <label for="date_of_birth" :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-2">জন্ম-তারিখ</label>
        <Calendar
          id="date_of_birth"
          v-model="local.Date_of_birth"
          :disabled="true"
          dateFormat="yy-mm-dd"
          placeholder="জন্ম-তারিখ নির্বাচন করুন"
          class="w-full"
          :pt="{
            root: { class: ['w-full', isDark ? 'bg-gray-700 border-gray-600 text-gray-300' : 'bg-gray-100 border-gray-300 text-gray-700'] },
            input: { class: ['w-full', isDark ? 'bg-gray-700 border-gray-600 text-gray-300' : 'bg-gray-100 border-gray-300 text-gray-700'] }
          }"
        />
      </div>

      <div class="w-full">
        <label for="brn_no" :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-2">জন্ম-নিবন্ধন নম্বর</label>
        <InputText
          id="brn_no"
          v-model="local.BRN_no"
          placeholder="জন্ম-নিবন্ধন নম্বর"
          class="w-full"
          :pt="{
            root: { class: ['w-full', isDark ? 'bg-gray-700 border-gray-600 text-gray-300' : 'bg-white border-gray-300 text-gray-700'] }
          }"
        />
      </div>

      <div class="w-full">
        <label for="nid_no" :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-2">জাতীয় পরিচয়পত্র নম্বর</label>
        <InputText
          id="nid_no"
          v-model="local.NID_no"
          placeholder="জাতীয় পরিচয়পত্র নম্বর"
          class="w-full"
          :pt="{
            root: { class: ['w-full', isDark ? 'bg-gray-700 border-gray-600 text-gray-300' : 'bg-white border-gray-300 text-gray-700'] }
          }"
        />
      </div>
    </div>

    <!-- ফোন নম্বর -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6 w-full">
      <div class="w-full lg:col-span-1">
        <label for="mobile_no" :class="[!isDark ? 'text-gray-700' : 'text-gray-300']" class="text-lg block font-medium mb-2">অভিভাবকের ফোন নম্বর</label>
        <InputText
          id="mobile_no"
          v-model="local.mobile_no"
          type="tel"
          placeholder="অভিভাবকের ফোন নম্বর"
          class="w-full"
          :pt="{
            root: { class: ['w-full', isDark ? 'bg-gray-700 border-gray-600 text-gray-300' : 'bg-white border-gray-300 text-gray-700'] }
          }"
        />
      </div>
      <div class="w-full lg:col-span-2"></div>
    </div>
  </Fieldset>
</template>

<script setup>
import { reactive, watch, computed } from 'vue'
import InputText from 'primevue/inputtext'
import Calendar from 'primevue/calendar'
import Fieldset from 'primevue/fieldset'

const props = defineProps({
  modelValue: Object
})

const emit = defineEmits(['update:modelValue'])

const isDark = computed(() => document.documentElement.classList.contains('dark'))

// Helper function to convert string to Date object
function stringToDate(dateString) {
  if (!dateString) return null
  const date = new Date(dateString)
  return isNaN(date.getTime()) ? null : date
}

// Helper function to convert Date object to string
function dateToString(date) {
  if (!date) return ''
  const d = new Date(date)
  if (isNaN(d.getTime())) return ''
  return d.toISOString().split('T')[0] // Format: YYYY-MM-DD
}

// local reactive copy to avoid mutating prop directly
const local = reactive({
  name_bn: props.modelValue?.name_bn ?? '',
  name_en: props.modelValue?.name_en ?? '',
  name_ar: props.modelValue?.name_ar ?? '',
  father_name_bn: props.modelValue?.father_name_bn ?? '',
  father_name_en: props.modelValue?.father_name_en ?? '',
  father_name_ar: props.modelValue?.father_name_ar ?? '',
  mother_name_bn: props.modelValue?.mother_name_bn ?? '',
  mother_name_en: props.modelValue?.mother_name_en ?? '',
  mother_name_ar: props.modelValue?.mother_name_ar ?? '',
  Date_of_birth: stringToDate(props.modelValue?.Date_of_birth),
  BRN_no: props.modelValue?.BRN_no ?? '',
  NID_no: props.modelValue?.NID_no ?? '',
  mobile_no: props.modelValue?.mobile_no ?? ''
})

// keep local in sync when parent changes modelValue
watch(
  () => props.modelValue,
  (newVal) => {
    if (!newVal) return
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
      Date_of_birth: stringToDate(newVal.Date_of_birth),
      BRN_no: newVal.BRN_no ?? '',
      NID_no: newVal.NID_no ?? '',
      mobile_no: newVal.mobile_no ?? ''
    })
  },
  { deep: true, immediate: true }
)

// emit updates when local changes
watch(
  local,
  (val) => {
    // Convert Date back to string when emitting
    emit('update:modelValue', {
      ...val,
      Date_of_birth: dateToString(val.Date_of_birth)
    })
  },
  { deep: true }
)
</script>

<style scoped>
/* All styling is Tailwind CSS utilities only. */
</style>
