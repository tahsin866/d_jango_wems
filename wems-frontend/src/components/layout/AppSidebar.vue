<template>
  <aside style="font-family: 'SolaimanLipi', sans-serif;" :class="[
    'fixed flex flex-col lg:mt-0 top-0 px-0 left-0 bg-[#18222e] text-[#e0e6ed] h-screen transition-all duration-300 ease-in-out z-99999 border-none shadow-none',
    {
      'lg:w-[280px]': isExpanded || isMobileOpen || isHovered,
      'lg:w-[70px]': !isExpanded && !isHovered,
      'translate-x-0 w-[280px]': isMobileOpen,
      '-translate-x-full': !isMobileOpen,
      'lg:translate-x-0': true,
    },
  ]" @mouseenter="!isExpanded && (isHovered = true)" @mouseleave="isHovered = false">
    <!-- Header -->
    <div :class="[
      'py-5 bg-gradient-to-r from-emerald-600/80 to-emerald-800/80  border-emerald-900/30',
      !isExpanded && !isHovered ? 'lg:px-3' : 'px-4',
    ]">
      <div v-if="isExpanded || isHovered || isMobileOpen" class="flex items-center">
        <h1 class="text-base font-semibold text-emerald-50 text-xl text-center tracking-wide">
          মাদরাসা পেনেল
        </h1>
      </div>
      <div v-else class="flex justify-center">
        <div class="w-8 h-8 bg-emerald-600 rounded-lg flex items-center justify-center">
          <span class="text-white text-sm font-semibold">M</span>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <div class="flex-1 overflow-y-auto bg-[#18222e] custom-scrollbar">
      <nav class="px-0 py-2">
        <div class="space-y-1">
          <div v-for="(item, index) in menuItems" :key="item.label">
            <!-- Submenu Items -->
            <div v-if="item.items">
              <button @click="toggleSubmenu(index)" :class="[
                'w-full flex items-center text-left px-5 py-2 text-xl font-medium rounded transition-all duration-150',
                {
                  'bg-emerald-50/10 text-emerald-400 border-l-4 border-emerald-400': isSubmenuOpen(index),
                  'text-[#e0e6ed] hover:bg-[#223049] hover:text-emerald-400 border-l-4 border-transparent': !isSubmenuOpen(index),
                },
                !isExpanded && !isHovered ? 'justify-center' : '',
              ]">
                <span class="flex-shrink-0 w-5 h-5">
                  <component :is="item.icon" class="w-full h-full" />
                </span>
                <span v-if="isExpanded || isHovered || isMobileOpen" class="ml-3 flex-1">
                  {{ item.label }}
                </span>
                <ChevronDownIcon v-if="isExpanded || isHovered || isMobileOpen" :class="[
                  'ml-2 w-4 h-4 transition-transform duration-200',
                  { 'rotate-180': isSubmenuOpen(index) },
                ]" />
              </button>

              <!-- Submenu -->
              <transition @enter="startTransition" @after-enter="endTransition" @before-leave="startTransition"
                @after-leave="endTransition">
                <div v-show="isSubmenuOpen(index) && (isExpanded || isHovered || isMobileOpen)"
                  class="bg-[#1d2737] rounded-md ml-3 my-1 py-1">
                  <router-link v-for="subItem in item.items" :key="subItem.label" :to="subItem.to" :class="[
                    'flex items-center w-full px-5 py-2 text-xl rounded transition-all duration-150',
                    {
                      'bg-emerald-50/10 text-emerald-400': isActive(subItem.to),
                      'text-[#e0e6ed] hover:bg-[#223049] hover:text-emerald-400': !isActive(subItem.to),
                    },
                  ]">
                    <span class="flex-shrink-0 w-4 h-4 mr-3">
                      <component :is="subItem.icon" class="w-full h-full" />
                    </span>
                    <span class="flex-1 text-left">{{ subItem.label }}</span>
                    <div class="flex items-center gap-1">
                      <span v-if="subItem.new"
                        class="px-1.5 py-0.5 text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300 rounded-full">
                        new
                      </span>
                      <span v-if="subItem.pro"
                        class="px-1.5 py-0.5 text-xs font-medium bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300 rounded-full">
                        pro
                      </span>
                    </div>
                  </router-link>
                </div>
              </transition>
            </div>

            <!-- Direct Link Items -->
            <router-link v-else-if="item.to" :to="item.to" :class="[
              'w-full flex items-center px-5 py-2 text-xl font-medium rounded transition-all duration-150',
              {
                'bg-emerald-50/10 text-emerald-400 border-l-4 border-emerald-400': isActive(item.to),
                'text-[#e0e6ed] hover:bg-[#223049] hover:text-emerald-400 border-l-4 border-transparent': !isActive(item.to),
              },
              !isExpanded && !isHovered ? 'justify-center' : '',
            ]">
              <span class="flex-shrink-0 w-5 h-5">
                <component :is="item.icon" class="w-full h-full" />
              </span>
              <span v-if="isExpanded || isHovered || isMobileOpen" class="ml-3">
                {{ item.label }}
              </span>
            </router-link>
          </div>
        </div>
      </nav>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { type Component, markRaw } from "vue";
import { useRoute } from "vue-router";

import {
  CalenderIcon,
  UserCircleIcon,
  ChatIcon,
  MailIcon,
  DocsIcon,
  ChevronDownIcon,
  ListIcon,
  BoxCubeIcon,
  FolderIcon,
  SettingsIcon,
  HomeIcon,
  SupportIcon,
  BarChartIcon,
  TaskIcon,
  RefreshIcon,
  SendIcon,
  DraftIcon,
  TrashIcon,
  UserGroupIcon,
} from "../../icons";
import { useSidebar } from "@/composables/useSidebar";

const route = useRoute();

const { isExpanded, isMobileOpen, isHovered, openSubmenu } = useSidebar();

type SubMenuItem = {
  label: string;
  icon: Component;
  to: string;
  new?: boolean;
  pro?: boolean;
};

type MenuItem = {
  label: string;
  icon: Component;
  to?: string;
  key?: string;
  items?: SubMenuItem[];
};

const menuItems: MenuItem[] = [
  {
    label: 'ড্যাশবোর্ড',
    icon: markRaw(HomeIcon),
    to: '/dashboard'
  },
  {
    label: 'সেটাপ সংক্রান্ত',
    icon: markRaw(SettingsIcon),
    key: 'setup',
    items: [
      { label: 'বিষয় সেটাপ', icon: markRaw(TaskIcon), to: '/subject/list' },
      { label: 'সেটিংস', icon: markRaw(SettingsIcon), to: '/settings' },
    ]
  },
  {
    label: 'মারকায সংক্রান্ত',
    icon: markRaw(BoxCubeIcon),
    key: 'markaz',
    items: [
      { label: 'মারকায আবেদন', icon: markRaw(SendIcon), to: '/user/markaz/list' },
      { label: 'মারকায পরিবর্তন', icon: markRaw(RefreshIcon), to: '/user/markaz/change' },
      { label: 'মারকায সেটাপ', icon: markRaw(BoxCubeIcon), to: '/user/markaz/setup' },
      { label: 'মারহালা পরিবর্তন', icon: markRaw(RefreshIcon), to: '/user/marhala/change' },
      { label: 'মন্জুরিপত্র আবেদন', icon: markRaw(DocsIcon), to: '/user/confirmation' }
    ]
  },
  {
    label: 'নিবন্ধন সংক্রান্ত',
    icon: markRaw(UserCircleIcon),
    key: 'registration',
    items: [
      { label: 'পরীক্ষার্থী নিবন্ধন', icon: markRaw(UserCircleIcon), to: '/user/registration/overview' },
      { label: 'নিবন্ধন তালিকা', icon: markRaw(ListIcon), to: '/user/registration/list' },
      { label: 'বিগত পরীক্ষার্থী তালিকা', icon: markRaw(UserGroupIcon), to: '/user/old-student/list' },
      { label: 'নিবন্ধন পত্র', icon: markRaw(DocsIcon), to: '/user/registration/card' },
      { label: 'ড্রাফ্ট/সফ্ট ডিলিট', icon: markRaw(DraftIcon), to: '/restore' },
      { label: 'পেমেন্ট তালিকা', icon: markRaw(BarChartIcon), to: '/payment' }
    ]
  },
  {
    label: 'অন্তর্ভুক্তি সংক্রান্ত',
    icon: markRaw(UserGroupIcon),
    key: 'admission',
    items: [
      { label: 'অন্তর্ভুক্তি তালিকা', icon: markRaw(UserGroupIcon), to: '/admission-list' },
      { label: 'ড্রাফ্ট/সফ্ট ডিলিট', icon: markRaw(DraftIcon), to: '/admission-draft' },
      { label: 'প্রবেশ পত্র', icon: markRaw(DocsIcon), to: '/admit-card' },
      { label: 'পেমেন্ট', icon: markRaw(BarChartIcon), to: '/admission-payment' }
    ]
  },
  {
    label: 'নেগরান/মুমতাহিন',
    icon: markRaw(UserGroupIcon),
    key: 'negran',
    items: [
      { label: 'নেগ:মুম আবেদন', icon: markRaw(SendIcon), to: '/negran-mumtahin-apply' },
      { label: 'নেগ:মুম আবেদন তালিকা', icon: markRaw(ListIcon), to: '/negran-mumtahin-list' },
      { label: 'নিয়োগ পত্র', icon: markRaw(DocsIcon), to: '/appointment-letter' }
    ]
  },
  {
    label: 'রিপোর্টস',
    icon: markRaw(BarChartIcon),
    key: 'reports',
    items: [
      { label: 'নিবন্ধন রিপোর্ট', icon: markRaw(BarChartIcon), to: '/report-registration' },
      { label: 'অন্তর্ভুক্তি রিপোর্ট', icon: markRaw(BarChartIcon), to: '/report-admission' },
      { label: 'নেগ:মুম রিপোর্ট', icon: markRaw(BarChartIcon), to: '/report-negran' },
      { label: 'হাজিরা রিপোর্ট', icon: markRaw(CalenderIcon), to: '/report-attendance' },
      { label: 'পেমেন্ট রিপোর্ট', icon: markRaw(BarChartIcon), to: '/report-payment' },
      { label: 'নিয়োগ রিপোর্ট', icon: markRaw(BarChartIcon), to: '/report-appointment' }
    ]
  },
  {
    label: 'প্রয়োজনীয় ডকুমেন্টস',
    icon: markRaw(FolderIcon),
    key: 'documents',
    items: [
      { label: 'নিবন্ধন রিপোর্ট', icon: markRaw(DocsIcon), to: '/doc-registration' },
      { label: 'অন্তর্ভুক্তি রিপোর্ট', icon: markRaw(DocsIcon), to: '/doc-admission' },
      { label: 'নেগ:মুম রিপোর্ট', icon: markRaw(DocsIcon), to: '/doc-negran' },
      { label: 'হাজিরা রিপোর্ট', icon: markRaw(DocsIcon), to: '/doc-attendance' },
      { label: 'পেমেন্ট রিপোর্ট', icon: markRaw(DocsIcon), to: '/doc-payment' },
      { label: 'নিয়োগ রিপোর্ট', icon: markRaw(DocsIcon), to: '/doc-appointment' }
    ]
  },
  {
    label: 'ইমেইল',
    icon: markRaw(MailIcon),
    key: 'email',
    items: [
      { label: 'ইনবক্স', icon: markRaw(MailIcon), to: '/email-inbox' },
      { label: 'সেন্ট', icon: markRaw(SendIcon), to: '/email-sent' },
      { label: 'ড্রাফ্ট', icon: markRaw(DraftIcon), to: '/email-draft' },
      { label: 'ট্রাস', icon: markRaw(TrashIcon), to: '/email-trash' }
    ]
  },
  {
    label: 'ভাউচার',
    icon: markRaw(DocsIcon),
    key: 'voucher',
    items: [
      { label: 'ভাউচার তৈরি', icon: markRaw(DocsIcon), to: '/voucher-create' },
      { label: 'ভাউচার লিস্ট', icon: markRaw(ListIcon), to: '/voucher-list' },
      { label: 'অনুমোদনকৃত ভাউচার', icon: markRaw(DocsIcon), to: '/voucher-approved' },
      { label: 'ট্রাস', icon: markRaw(TrashIcon), to: '/voucher-trash' }
    ]
  },
  {
    label: 'ফলাফল',
    icon: markRaw(BarChartIcon),
    key: 'result',
    items: [
      { label: 'ফলাফল যাচিই', icon: markRaw(BarChartIcon), to: '/result-verify' },
      { label: 'মারহালাওয়ারী ফলাফল', icon: markRaw(BarChartIcon), to: '/result-marhala' },
      { label: 'মেধাতালিকা', icon: markRaw(BarChartIcon), to: '/result-merit' },
      { label: 'ফলাফল ওভারভিউ', icon: markRaw(BarChartIcon), to: '/result-overview' },
      { label: 'ফলাফল যাচাই', icon: markRaw(BarChartIcon), to: '/result-check' }
    ]
  },
  {
    label: 'মেসেজিং',
    icon: markRaw(ChatIcon),
    to: '/messaging'
  },
  {
    label: 'সাপোর্টস',
    icon: markRaw(SupportIcon),
    to: '/supports'
  }
];

const isActive = (path: string) => route.path === path;

// Fixed toggleSubmenu function - now only takes groupIndex
const toggleSubmenu = (groupIndex: number) => {
  const currentKey = `${groupIndex}`;
  // If clicking on the same submenu, close it; otherwise open the new one
  openSubmenu.value = openSubmenu.value === currentKey ? null : currentKey;
};

// Fixed isSubmenuOpen function
const isSubmenuOpen = (groupIndex: number) => {
  const key = `${groupIndex}`;
  // Check if submenu is open or any subItem is active
  return (
    openSubmenu.value === key ||
    (
      Array.isArray(menuItems[groupIndex].items) &&
      menuItems[groupIndex].items.some((subItem: SubMenuItem) => isActive(subItem.to))
    )
  );
};

const endTransition = (el: Element) => {
  (el as HTMLElement).style.height = "";
};

const startTransition = (el: Element) => {
  (el as HTMLElement).style.height = "auto";
};
</script>

<style scoped>
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #3ba97b #18222e;
  max-height: 100%;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 7px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #3ba97b;
  border-radius: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #18222e;
  border-radius: 8px;
}
</style>
