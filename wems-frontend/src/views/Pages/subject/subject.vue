<template>

    <div class=" font-[SolaimanLipi]">
      <div class="bg-white dark:bg-slate-800 rounded-lg  dark:border-slate-700 p-6">
        <div class="mb-4">
          <h2 class="text-xl  font-semibold text-slate-800 dark:text-slate-100">মারহালা বিষয় সারসংক্ষেপ</h2>
          <p class="text-md text-slate-500 dark:text-slate-300">মারহালা অনুযায়ী মোট বিষয় ও ছাত্র-ছাত্রী বিভাজন</p>
        </div>

        <div class="overflow-x-auto text-xl">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-slate-700">
            <thead class="bg-gray-50 dark:bg-slate-900">
              <tr>
                <th class="px-4 py-3 text-left  font-medium text-slate-700 dark:text-slate-300">মারহালা নাম</th>
                <th class="px-6 py-3 text-center  font-medium text-slate-700 dark:text-slate-300">মোট বিষয়</th>
                <th class="px-6 py-3 text-center  font-medium text-slate-700 dark:text-slate-300">পুরুষ</th>
                <th class="px-6 py-3 text-center  font-medium text-slate-700 dark:text-slate-300">মহিলা</th>
                <th class="px-6 py-3 text-center  font-medium text-slate-700 dark:text-slate-300">উভয়</th>
                <th class="px-6 py-3 text-center  font-medium text-slate-700 dark:text-slate-300">অ্যাকশন</th>
              </tr>
            </thead>

            <tbody class="bg-white dark:bg-slate-800 divide-y divide-gray-100 dark:divide-slate-700 text-xl">
              <tr v-for="row in displayedRows" :key="row.id" class="hover:bg-gray-50 dark:hover:bg-slate-700/50">
                <td class="px-4 py-4  text-slate-800 dark:text-slate-100">
                  {{ row.marhala_name_bn }}
                </td>

                <td class="px-6 py-4 text-center  font-semibold text-slate-800 dark:text-slate-100">
                  {{ formatNumber(row.total_subjects) }}
                </td>

                <td class="px-6 py-4 text-center  text-slate-700 dark:text-slate-200">
                  {{ formatNumber(row.male_subjects) }}
                </td>

                <td class="px-6 py-4 text-center  text-slate-700 dark:text-slate-200">
                  {{ formatNumber(row.female_subjects) }}
                </td>

                <td class="px-6 py-4 text-center  text-slate-700 dark:text-slate-200">
                  {{ formatNumber(row.both_subjects) }}
                </td>

                <td class="px-6 py-4 text-center">
                  <!-- action button styled like screenshot -->
                  <button
                    @click="onSetup(row)"
                    type="button"
                    class="inline-flex items-center px-4 py-2 bg-slate-800 text-white rounded-md shadow-sm hover:bg-slate-900 dark:bg-slate-700 dark:hover:bg-slate-600"
                  >
                    বিষয় সেটাপ করুন
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- optional: summary / pagination placeholder -->
        <div class="mt-4 flex items-center justify-between text-sm text-slate-500 dark:text-slate-400">
          <div>মোট মারহালা: <span class="font-semibold text-slate-700 dark:text-slate-100">{{ rows.length }}</span></div>
          <div v-if="rows.length > displayedRows.length" class="text-right">
            <button @click="showAll = !showAll" class="text-blue-600 dark:text-blue-400 underline">
              {{ showAll ? 'সংকীর্ণ করুন' : 'সব দেখুন' }}
            </button>
          </div>
        </div>
      </div>
    </div>

</template>

<script setup lang="ts">
defineOptions({ name: 'SubjectSummary' })
import { computed, defineEmits, defineProps, ref, onMounted } from 'vue';
import axios from 'axios';


interface Row {
  id: number | string;
  marhala_name_bn: string;
  total_subjects: number;
  male_subjects: number;
  female_subjects: number;
  both_subjects: number;
}

const props = defineProps<{
  data?: Row[]; // optional prop so parent can pass real data
}>();

const emit = defineEmits<{
  (e: 'setup', row: Row): void;
}>();

// reactive data
const rows = ref<Row[]>([]);
const loading = ref(false);
const error = ref('');

// mock data to match the screenshot layout when API fails
const defaultRows = [
  { id: 1, marhala_name_bn: 'ফজীলত', total_subjects: 11, male_subjects: 4, female_subjects: 4, both_subjects: 3 },
  { id: 2, marhala_name_bn: 'সানাবিয়া উলীয়া', total_subjects: 10, male_subjects: 1, female_subjects: 2, both_subjects: 7 },
  { id: 3, marhala_name_bn: 'সানাবিয়া', total_subjects: 8, male_subjects: 8, female_subjects: 0, both_subjects: 0 },
  { id: 4, marhala_name_bn: 'মুলতাওয়াসিতা', total_subjects: 9, male_subjects: 1, female_subjects: 0, both_subjects: 8 },
  { id: 5, marhala_name_bn: 'ইবতিদাইয়া', total_subjects: 9, male_subjects: 2, female_subjects: 1, both_subjects: 6 },
  { id: 6, marhala_name_bn: 'তাহফিজুল কুরআন', total_subjects: 3, male_subjects: 0, female_subjects: 0, both_subjects: 3 },
  { id: 7, marhala_name_bn: 'ইলমুত তাজবিদ ওয়াল কিরাআত', total_subjects: 4, male_subjects: 0, female_subjects: 0, both_subjects: 4 }
] as Row[];

const showAll = ref<boolean>(false);

// computed slice to mimic screenshot that may show limited rows
const displayedRows = computed(() => {
  return showAll.value ? rows.value : rows.value.slice(0, rows.value.length);
});

// API call function
async function fetchMarhalaData() {
  try {
    loading.value = true;
    error.value = '';

    const response = await axios.get('http://localhost:8000/api/marhalas/with-counts/', {
      withCredentials: true,
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (response.data.success) {
      rows.value = response.data.data;
    } else {
      error.value = response.data.message || 'ডেটা লোড করতে সমস্যা হয়েছে';
      rows.value = defaultRows; // fallback to mock data
    }
  } catch (err: unknown) {
    console.error('API Error:', err);
    error.value = 'সার্ভার থেকে ডেটা আনতে সমস্যা হয়েছে';
    rows.value = defaultRows; // fallback to mock data
  } finally {
    loading.value = false;
  }
}

// formatting helper (Bangla locale)
function formatNumber(n: number) {
  try {
    return new Intl.NumberFormat('bn-BD').format(n);
  } catch {
    return String(n);
  }
}

function onSetup(row: Row) {
  // emit event to parent so parent can navigate / open modal
  emit('setup', row);
}

// Load data on component mount
onMounted(() => {
  if (props.data && props.data.length) {
    rows.value = props.data;
  } else {
    fetchMarhalaData();
  }
});
</script>

<style scoped>
/* minor visual tweaks to better match screenshot spacing */
table th {
  border-bottom: 1px solid rgba(15,23,42,0.06);
}
table td {
  vertical-align: middle;
}
</style>
