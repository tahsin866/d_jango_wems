<template>
  <aside
    style="font-family: 'SolaimanLipi', sans-serif;"
    :class="[
      'fixed flex flex-col top-0 left-0 h-screen transition-all duration-300 z-50 bg-gray-800 text-gray-300 shadow-lg border-r border-gray-700',
      isMobileOpen ? 'translate-x-0 w-[280px]' : '-translate-x-full',
      isExpanded || isMobileOpen || isHovered ? 'lg:w-[290px]' : 'lg:w-[60px]',
      'lg:translate-x-0'
    ]"
    @mouseenter="!isExpanded && (isHovered = true)"
    @mouseleave="isHovered = false"
  >
    <!-- Sidebar Header / Logo -->
    <div class="flex items-center justify-center h-16 border-b border-gray-700 bg-gray-900 px-3">
      <template v-if="isExpanded || isHovered || isMobileOpen">
        <h1 class="text-xl font-bold text-gray-200 tracking-wide font-sans" style="letter-spacing: 1px;">
          <span class="ml-2">মাদরাসা</span>
        </h1>
      </template>
      <template v-else>
        <div class="w-10 h-10 bg-gray-700 rounded-lg flex items-center justify-center border border-gray-600">
          <span class="text-gray-200 text-lg font-bold">M</span>
        </div>
      </template>
    </div>

    <!-- Navigation -->
    <div class="flex-1 overflow-y-auto bg-gray-800 classic-scrollbar">
      <nav class="py-4">
        <ul class="space-y-1 px-2">
          <li v-for="(item, index) in menuItems" :key="item.label">
            <!-- Submenu Items -->
            <template v-if="item.items">
              <button
                @click="toggleSubmenu(index)"
                :class="[
                  'w-full flex items-center text-left px-3 py-2 rounded font-medium transition-all duration-150 group classic-menu-btn',
                  isSubmenuOpen(index)
                    ? 'bg-gray-700 text-gray-100 border-l-4 border-gray-500'
                    : 'hover:bg-gray-700 hover:text-gray-100',
                  !isExpanded && !isHovered ? 'justify-center' : ''
                ]"
                style="letter-spacing: 0.5px;"
              >
                <span class="w-5 h-5 mr-3 flex items-center justify-center">
                  <component :is="item.icon" class="w-full h-full" />
                </span>
                <span v-if="isExpanded || isHovered || isMobileOpen" class="flex-1 text-left font-sans">{{ item.label }}</span>
                <ChevronDownIcon
                  v-if="isExpanded || isHovered || isMobileOpen"
                  class="ml-2 w-4 h-4 text-gray-400 transition-transform"
                  :class="{ 'rotate-180': isSubmenuOpen(index) }"
                />
              </button>
              <transition name="slide-fade">
                <ul
                  v-show="isSubmenuOpen(index) && (isExpanded || isHovered || isMobileOpen)"
                  class="pl-8 mt-2 space-y-1 classic-submenu"
                  style="border-left:2px solid #4b5563;"
                >
                  <li v-for="subItem in item.items" :key="subItem.label">
                    <router-link
                      :to="subItem.to"
                      :class="[
                        'flex items-center px-3 py-2 rounded font-medium transition-all duration-150 classic-submenu-btn',
                        isActive(subItem.to)
                          ? 'bg-gray-700 text-gray-100 font-medium'
                          : 'hover:bg-gray-700 hover:text-gray-100'
                      ]"
                    >
                      <span class="w-4 h-4 mr-3 flex items-center justify-center">
                        <component :is="subItem.icon" class="w-full h-full" />
                      </span>
                      <span class="flex-1 text-left font-sans">{{ subItem.label }}</span>
                      <div class="flex items-center gap-1">
                        <span v-if="subItem.new"
                          class="px-2 py-1 text-xs font-medium bg-gray-600 text-gray-100 rounded">NEW</span>
                        <span v-if="subItem.pro"
                          class="px-2 py-1 text-xs font-medium bg-gray-600 text-gray-100 rounded">PRO</span>
                      </div>
                    </router-link>
                  </li>
                </ul>
              </transition>
            </template>
            <!-- Direct Link Items -->
            <router-link
              v-else-if="item.to"
              :to="item.to"
              :class="[
                'w-full flex items-center px-3 py-2 rounded font-medium transition-all duration-150 classic-menu-btn',
                isActive(item.to)
                  ? 'bg-gray-700 text-gray-100 font-medium'
                  : 'hover:bg-gray-700 hover:text-gray-100',
                !isExpanded && !isHovered ? 'justify-center' : ''
              ]"
              style="letter-spacing: 0.5px;"
            >
              <span class="w-5 h-5 mr-3 flex items-center justify-center">
                <component :is="item.icon" class="w-full h-full" />
              </span>
              <span v-if="isExpanded || isHovered || isMobileOpen" class="font-sans">{{ item.label }}</span>
            </router-link>
          </li>
        </ul>
      </nav>
    </div>
  </aside>
</template>

<script setup>
import { markRaw } from "vue";
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

const menuItems = [
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
    label: 'মারকায় সংক্রান্ত',
    icon: markRaw(BoxCubeIcon),
    key: 'markaz',
    items: [
      { label: 'মারকায় আবেদন', icon: markRaw(SendIcon), to: '/user/markaz/list' },
      { label: 'মারকায় পরিবর্তন', icon: markRaw(RefreshIcon), to: '/user/markaz/change' },
      { label: 'মারকায় সেটাপ', icon: markRaw(BoxCubeIcon), to: '/user/markaz/setup' },
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

const isActive = (path) => route.path === path;

const toggleSubmenu = (groupIndex) => {
  const currentKey = `${groupIndex}`;
  openSubmenu.value = openSubmenu.value === currentKey ? null : currentKey;
};

const isSubmenuOpen = (groupIndex) => {
  const key = `${groupIndex}`;
  return (
    openSubmenu.value === key ||
    (
      Array.isArray(menuItems[groupIndex].items) &&
      menuItems[groupIndex].items.some(subItem => isActive(subItem.to))
    )
  );
};
</script>

<style scoped>
.classic-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #6b7280 #1f2937;
  max-height: 100%;
}
.classic-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.classic-scrollbar::-webkit-scrollbar-thumb {
  background: #6b7280;
  border-radius: 4px;
}
.classic-scrollbar::-webkit-scrollbar-track {
  background: #1f2937;
  border-radius: 4px;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.18s ease-in-out;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-4px);
  opacity: 0;
}

.classic-menu-btn {
  border-left: 3px solid transparent;
}
.classic-menu-btn:active, .classic-menu-btn:focus {
  outline: none;
  border-left: 3px solid #4b5563;
}
.classic-menu-btn.bg-gray-700 {
  border-left: 3px solid #4b5563;
}

.classic-submenu {
  background: #1f2937;
  border-radius: 0 0 4px 4px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.classic-submenu-btn {
  border-left: 2px solid transparent;
}
.classic-submenu-btn.bg-gray-700 {
  border-left: 2px solid #4b5563;
}
</style>
