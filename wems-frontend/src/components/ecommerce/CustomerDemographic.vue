<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="max-w-3xl mx-auto mt-8"
  >
    <div class="border border-gray-300 rounded shadow-lg bg-white">
      <!-- Box Header -->
      <div class="px-5 py-3 bg-gray-100 border-b border-gray-200 rounded-t flex items-center">
        <div>
          <h3 class="font-bold text-base text-gray-800 flex items-center">
            <i class="fas fa-globe-americas mr-2 text-indigo-500"></i>
            Customers Demographic
          </h3>
          <p class="mt-1 text-gray-600 text-sm">
            Number of customer based on country
          </p>
        </div>
      </div>

      <!-- Box Body -->
      <div class="px-5 py-7 bg-white">
        <!-- Classic AdminLTE Map Card with jsVectorMap -->
        <div class="mb-8 flex flex-col items-center justify-center">
          <div class="w-full max-w-md border border-gray-300 rounded bg-gray-50 py-5 px-4 flex items-center justify-center shadow">
            <!-- jsVectorMap container -->
            <div
              ref="mapOneRef"
              id="mapOne"
              class="h-[212px] w-[252px] sm:w-[400px] md:w-[500px] lg:w-[634px] xl:w-[393px] 2xl:w-[554px] rounded"
              style="min-width:220px;"
            ></div>
          </div>
        </div>
        <!-- Country Stats (Classic info-box style) -->
        <div class="space-y-5">
          <!-- USA -->
          <div class="flex items-center justify-between py-2 border-b border-gray-100">
            <div class="flex items-center gap-3">
              <span class="inline-block h-8 w-8 rounded-full overflow-hidden border border-gray-300 bg-white flex items-center justify-center">
                <img src="/images/country/country-01.svg" alt="usa" class="h-6 w-6" />
              </span>
              <div>
                <p class="font-bold text-gray-800 text-sm">USA</p>
                <span class="block text-gray-500 text-xs">2,379 Customers</span>
              </div>
            </div>
            <div class="flex items-center gap-3 w-36">
              <div class="relative block h-3 w-full max-w-[100px] rounded bg-gray-200 overflow-hidden border border-gray-300">
                <div
                  class="absolute left-0 top-0 h-full bg-indigo-500 rounded"
                  style="width: 79%;"
                ></div>
              </div>
              <span class="font-bold text-gray-700 text-xs">79%</span>
            </div>
          </div>
          <!-- France -->
          <div class="flex items-center justify-between py-2 border-b border-gray-100">
            <div class="flex items-center gap-3">
              <span class="inline-block h-8 w-8 rounded-full overflow-hidden border border-gray-300 bg-white flex items-center justify-center">
                <img src="/images/country/country-02.svg" alt="france" class="h-6 w-6" />
              </span>
              <div>
                <p class="font-bold text-gray-800 text-sm">France</p>
                <span class="block text-gray-500 text-xs">589 Customers</span>
              </div>
            </div>
            <div class="flex items-center gap-3 w-36">
              <div class="relative block h-3 w-full max-w-[100px] rounded bg-gray-200 overflow-hidden border border-gray-300">
                <div
                  class="absolute left-0 top-0 h-full bg-indigo-400 rounded"
                  style="width: 23%;"
                ></div>
              </div>
              <span class="font-bold text-gray-700 text-xs">23%</span>
            </div>
          </div>
          <!-- Egypt -->
          <div class="flex items-center justify-between py-2">
            <div class="flex items-center gap-3">
              <span class="inline-block h-8 w-8 rounded-full overflow-hidden border border-gray-300 bg-white flex items-center justify-center">
                <img src="/images/country/country-03.svg" alt="egypt" class="h-6 w-6" />
              </span>
              <div>
                <p class="font-bold text-gray-800 text-sm">Egypt</p>
                <span class="block text-gray-500 text-xs">233 Customers</span>
              </div>
            </div>
            <div class="flex items-center gap-3 w-36">
              <div class="relative block h-3 w-full max-w-[100px] rounded bg-gray-200 overflow-hidden border border-gray-300">
                <div
                  class="absolute left-0 top-0 h-full bg-yellow-500 rounded"
                  style="width: 12%;"
                ></div>
              </div>
              <span class="font-bold text-gray-700 text-xs">12%</span>
            </div>
          </div>
        </div>
      </div>
      <!-- Box Footer -->
      <div class="bg-gray-50 border-t border-gray-200 rounded-b px-5 py-2 flex justify-end">
        <button class="inline-flex items-center text-sm text-indigo-700 hover:text-indigo-900 font-semibold">
          <span>All Customers</span>
          <i class="fas fa-arrow-right ml-1"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import jsVectorMap from 'jsvectormap'
import 'jsvectormap/dist/maps/world'

const mapOneRef = ref(null)
const mapInstance = ref(null)

const initMap = () => {
  if (mapOneRef.value) {
    mapInstance.value = new jsVectorMap({
      selector: mapOneRef.value,
      map: 'world',
      zoomButtons: false,
      regionStyle: {
        initial: {
          fontFamily: 'Outfit',
          fill: '#D9D9D9',
        },
        hover: {
          fillOpacity: 1,
          fill: '#465fff',
        },
      },
      markers: [
        {
          name: 'Egypt',
          coords: [26.8206, 30.8025],
        },
        {
          name: 'United States',
          coords: [55.3781, 3.436],
        },
        {
          name: 'United States',
          coords: [37.0902, -95.7129],
        },
      ],
      markerStyle: {
        initial: {
          strokeWidth: 1,
          fill: '#465fff',
          fillOpacity: 1,
          r: 4,
        },
        hover: {
          fill: '#465fff',
          fillOpacity: 1,
        },
        selected: {},
        selectedHover: {},
      },
      onRegionTooltipShow: function (event, tooltip) {
        const code = event.target.getAttribute('data-code')
        if (code === 'EG') {
          tooltip.setContent(tooltip.text() + ' (Hello Egypt)')
        }
      },
    })
  }
}

onMounted(() => {
  initMap()
})
</script>
