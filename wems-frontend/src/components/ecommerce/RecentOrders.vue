<template>
  <div
    style="font-family: 'SolaimanLipi', sans-serif;"
    class="max-w-4xl mx-auto mt-8"
  >
    <!-- AdminLTE Box -->
    <div class="rounded border border-gray-300 bg-white shadow-lg">
      <!-- Box Header -->
      <div class="flex items-center justify-between px-5 py-3 box-header border-b border-gray-200 bg-gray-100 rounded-t">
        <h3 class="font-bold text-lg text-gray-800 flex items-center">
          <i class="fas fa-shopping-cart mr-2 text-gray-500"></i>
          Recent Orders
        </h3>
        <div class="flex items-center gap-2">
          <button
            class="px-3 py-1 rounded bg-white border border-gray-400 text-sm text-gray-700 font-semibold hover:bg-gray-200 transition flex items-center gap-1"
          >
            <i class="fas fa-filter"></i>
            Filter
          </button>
          <button
            class="px-3 py-1 rounded bg-white border border-gray-400 text-sm text-gray-700 font-semibold hover:bg-gray-200 transition flex items-center gap-1"
          >
            <i class="fas fa-list"></i>
            See all
          </button>
        </div>
      </div>

      <!-- Box Body: Classic Table -->
      <div class="overflow-x-auto">
        <table class="min-w-full bg-white box-table border-b border-gray-300">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-200">
              <th class="py-3 px-5 text-left text-xs font-bold text-gray-600 uppercase tracking-wide">Products</th>
              <th class="py-3 px-5 text-left text-xs font-bold text-gray-600 uppercase tracking-wide">Category</th>
              <th class="py-3 px-5 text-left text-xs font-bold text-gray-600 uppercase tracking-wide">Price</th>
              <th class="py-3 px-5 text-left text-xs font-bold text-gray-600 uppercase tracking-wide">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(product, index) in products"
              :key="index"
              :class="index % 2 === 0 ? 'bg-gray-50' : 'bg-white'"
              class="border-b border-gray-200 hover:bg-blue-50 transition"
            >
              <td class="py-3 px-5 whitespace-nowrap">
                <div class="flex items-center gap-3">
                  <div class="h-10 w-10 overflow-hidden rounded border border-gray-300 bg-gray-100">
                    <img :src="product.image" :alt="product.name" class="object-cover w-full h-full" />
                  </div>
                  <div>
                    <div class="text-sm font-bold text-gray-800">{{ product.name }}</div>
                    <div class="text-xs text-gray-500">{{ product.variants }} Variants</div>
                  </div>
                </div>
              </td>
              <td class="py-3 px-5 whitespace-nowrap">
                <span class="text-sm font-semibold text-gray-700">{{ product.category }}</span>
              </td>
              <td class="py-3 px-5 whitespace-nowrap">
                <span class="text-sm font-semibold text-gray-700">{{ product.price }}</span>
              </td>
              <td class="py-3 px-5 whitespace-nowrap">
                <span
                  class="rounded px-3 py-1 text-xs font-bold inline-flex items-center"
                  :class="{
                    'bg-green-100 text-green-800': product.status === 'Delivered',
                    'bg-yellow-100 text-yellow-800': product.status === 'Pending',
                    'bg-red-100 text-red-700': product.status === 'Canceled',
                  }"
                >
                  <i
                    :class="{
                      'fas fa-check-circle mr-1 text-green-600': product.status === 'Delivered',
                      'fas fa-clock mr-1 text-yellow-600': product.status === 'Pending',
                      'fas fa-times-circle mr-1 text-red-600': product.status === 'Canceled',
                    }"
                  ></i>
                  {{ product.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Box Footer -->
      <div class="px-5 py-2 bg-gray-100 border-t border-gray-200 rounded-b flex justify-end">
        <button class="inline-flex items-center text-sm text-indigo-700 hover:text-indigo-900 font-semibold">
          <span>All Orders</span>
          <i class="fas fa-arrow-right ml-1"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const products = ref([
  {
    name: 'Macbook pro 13"',
    variants: 2,
    image: '/images/product/product-01.jpg',
    category: 'Laptop',
    price: '$2399.00',
    status: 'Delivered',
  },
  {
    name: 'Apple Watch Ultra',
    variants: 1,
    image: '/images/product/product-02.jpg',
    category: 'Watch',
    price: '$879.00',
    status: 'Pending',
  },
  {
    name: 'iPhone 15 Pro Max',
    variants: 2,
    image: '/images/product/product-03.jpg',
    category: 'SmartPhone',
    price: '$1869.00',
    status: 'Delivered',
  },
  {
    name: 'iPad Pro 3rd Gen',
    variants: 2,
    image: '/images/product/product-04.jpg',
    category: 'Electronics',
    price: '$1699.00',
    status: 'Canceled',
  },
  {
    name: 'Airpods Pro 2nd Gen',
    variants: 1,
    image: '/images/product/product-05.jpg',
    category: 'Accessories',
    price: '$240.00',
    status: 'Delivered',
  },
])
</script>
