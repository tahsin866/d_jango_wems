<script setup>
import { defineEmits, defineProps } from 'vue'
import InputText from 'primevue/inputtext'
import InputMask from 'primevue/inputmask'
import Calendar from 'primevue/calendar'

const emit = defineEmits(['update:modelValue', 'next'])
const props = defineProps({
  modelValue: Object,
  marhalaName: String
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
        ব্যক্তিগত তথ্য - {{ marhalaName }}
      </h2>
      <form class="space-y-6" @submit.prevent="emit('next')">
        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">নাম (বাংলা)</label>
            <InputText v-model="props.modelValue.name_bn" class="w-full mt-1" @input="updateField('name_bn', $event.target.value)" />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">নাম (ইংরেজি)</label>
            <InputText v-model="props.modelValue.name_en" class="w-full mt-1" @input="updateField('name_en', $event.target.value)" />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">নাম (আরবি)</label>
            <InputText v-model="props.modelValue.name_ar" class="w-full mt-1" @input="updateField('name_ar', $event.target.value)" />
          </div>
        </div>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">মাতার নাম (বাংলা)</label>
            <InputText v-model="props.modelValue.mother_name_bn" class="w-full mt-1" @input="updateField('mother_name_bn', $event.target.value)" />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">মাতার নাম (ইংরেজি)</label>
            <InputText v-model="props.modelValue.mother_name_en" class="w-full mt-1" @input="updateField('mother_name_en', $event.target.value)" />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">মাতার নাম (আরবি)</label>
            <InputText v-model="props.modelValue.mother_name_ar" class="w-full mt-1" @input="updateField('mother_name_ar', $event.target.value)" />
          </div>
        </div>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">পিতার নাম (বাংলা)</label>
            <InputText v-model="props.modelValue.father_name_bn" class="w-full mt-1" @input="updateField('father_name_bn', $event.target.value)" />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">পিতার নাম (ইংরেজি)</label>
            <InputText v-model="props.modelValue.father_name_en" class="w-full mt-1" @input="updateField('father_name_en', $event.target.value)" />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">পিতার নাম (আরবি)</label>
            <InputText v-model="props.modelValue.father_name_ar" class="w-full mt-1" @input="updateField('father_name_ar', $event.target.value)" />
          </div>
        </div>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">জন্ম-তারিখ</label>
            <Calendar v-model="props.modelValue.Date_of_birth" dateFormat="dd/mm/yy" class="w-full mt-1"
                      @update:modelValue="updateField('Date_of_birth', $event)" showIcon />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">জন্ম-নিবন্ধন নম্বর</label>
            <InputText v-model="props.modelValue.BRN_no" class="w-full mt-1" @input="updateField('BRN_no', $event.target.value)" />
          </div>
          <div class="field">
            <label class="block font-medium text-sm text-gray-700">জাতীয় পরিচয়পত্র নম্বর</label>
            <InputMask v-model="props.modelValue.NID_no" mask="9999-9999-9999-9999" placeholder="0000-0000-0000-0000"
                       class="w-full mt-1" @input="updateField('NID_no', $event.target.value)" />
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
