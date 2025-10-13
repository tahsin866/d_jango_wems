<script setup>
import { defineEmits, defineProps, computed } from 'vue'
import InputText from 'primevue/inputtext'
import InputMask from 'primevue/inputmask'
import Calendar from 'primevue/calendar'

const emit = defineEmits(['update:modelValue', 'next'])
const props = defineProps({
  modelValue: Object,
  marhalaName: String,
  marhalaId: [String, Number]
})

// মারহালা আইডি থেকে মারহালা নাম ম্যাপিং
const marhalaNames = {
  9: 'ফযিলত',
  10: 'সানাবিয়া',
  11: 'সানাবিয়া উলইয়া',
  12: 'মুতাওয়াসসিতা',
  14: 'ইবতেদাইয়্যাহ',
  15: 'হিফজুল কোরাআন',
  16: 'ক্বিরাআত'
}

// কম্পিউটেড প্রপার্টি যা মারহালা আইডি থেকে মারহালা নাম নির্ধারণ করবে
const displayMarhalaName = computed(() => {
  // যদি মারহালা নাম প্রপস হিসেবে আসে, তাহলে সেটা ব্যবহার করুন
  if (props.marhalaName) {
    return props.marhalaName
  }

  // অন্যথায় মারহালা আইডি থেকে নাম নির্ধারণ করুন
  const marhalaId = props.marhalaId || props.modelValue?.marhala_id
  if (marhalaId && marhalaNames[marhalaId]) {
    return marhalaNames[marhalaId]
  }

  // ডিফল্ট মান
  return 'মারহালা'
})

const updateField = (field, value) => {
  emit('update:modelValue', { ...props.modelValue, [field]: value })
}
</script>

<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
  class="bg-white overflow-hidden shadow-sm sm:rounded-lg mb-6">
    <div class="p-6 bg-white border-b border-gray-200">
      <h2 class="font-semibold text-xl text-gray-800 leading-tight mb-4">
        ব্যক্তিগত তথ্য - {{ displayMarhalaName }}
      </h2>
      <form class="space-y-6" @submit.prevent="emit('next')">
        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">নাম (বাংলা)</label>
            <InputText :modelValue="props.modelValue.student_name_bn" class="w-full mt-1" @update:modelValue="updateField('student_name_bn', $event)" />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">নাম (ইংরেজি)</label>
            <InputText :modelValue="props.modelValue.student_name_en" class="w-full mt-1" @update:modelValue="updateField('student_name_en', $event)" />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">নাম (আরবি)</label>
            <InputText :modelValue="props.modelValue.student_name_ar" class="w-full mt-1" @update:modelValue="updateField('student_name_ar', $event)" />
          </div>
        </div>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">মাতার নাম (বাংলা)</label>
            <InputText :modelValue="props.modelValue.mother_name_bn" class="w-full mt-1" @update:modelValue="updateField('mother_name_bn', $event)" />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">মাতার নাম (ইংরেজি)</label>
            <InputText :modelValue="props.modelValue.mother_name_en" class="w-full mt-1" @update:modelValue="updateField('mother_name_en', $event)" />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">মাতার নাম (আরবি)</label>
            <InputText :modelValue="props.modelValue.mother_name_ar" class="w-full mt-1" @update:modelValue="updateField('mother_name_ar', $event)" />
          </div>
        </div>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">পিতার নাম (বাংলা)</label>
            <InputText :modelValue="props.modelValue.father_name_bn" class="w-full mt-1" @update:modelValue="updateField('father_name_bn', $event)" />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">পিতার নাম (ইংরেজি)</label>
            <InputText :modelValue="props.modelValue.father_name_en" class="w-full mt-1" @update:modelValue="updateField('father_name_en', $event)" />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">পিতার নাম (আরবি)</label>
            <InputText :modelValue="props.modelValue.father_name_ar" class="w-full mt-1" @update:modelValue="updateField('father_name_ar', $event)" />
          </div>
        </div>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">জন্ম-তারিখ</label>
            <Calendar :modelValue="props.modelValue.date_of_birth" dateFormat="dd/mm/yy" class="w-full mt-1"
                      @update:modelValue="updateField('date_of_birth', $event)" showIcon />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">জন্ম-নিবন্ধন নম্বর</label>
            <InputText :modelValue="props.modelValue.birth_no" class="w-full mt-1" @update:modelValue="updateField('birth_no', $event)" />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">জাতীয় পরিচয়পত্র নম্বর</label>
            <InputMask :modelValue="props.modelValue.nid_no" mask="9999-9999-9999-9999" placeholder="0000-0000-0000-0000"
                       class="w-full mt-1" @update:modelValue="updateField('nid_no', $event)" />
          </div>
        </div>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">মোবাইল নম্বর</label>
            <InputMask :modelValue="props.modelValue.mobile" mask="99999-999999" placeholder="01XXX-XXXXXX"
                       class="w-full mt-1" @update:modelValue="updateField('mobile', $event)" />
          </div>
        </div>
        <div class="flex justify-end mt-6">
          <button type="submit" class="inline-flex items-center px-4 py-2 bg-gray-800 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-gray-700 active:bg-gray-900">
            পরবর্তী ধাপ
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
