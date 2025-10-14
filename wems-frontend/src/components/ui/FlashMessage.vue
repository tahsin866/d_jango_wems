<template>
  <transition name="flash-slide">
    <div
      v-if="show"
      :class="[
        'fixed top-6 right-6 z-50 max-w-md min-w-[320px]',
        'transform transition-all duration-300 ease-out'
      ]"
      :style="dynamicStyles"
    >
      <!-- Main flash container -->
      <div
        :class="[
          'relative rounded-lg shadow-2xl border-2 p-4',
          'backdrop-blur-sm transition-all duration-300',
          getContainerClasses()
        ]"
      >
        <!-- Flash icon -->
        <div class="flex items-start">
          <div class="flex-shrink-0 mr-3">
            <div
              :class="[
                'w-10 h-10 rounded-full flex items-center justify-center',
                'animate-pulse',
                getIconClasses()
              ]"
            >
              <component :is="getIcon()" class="w-5 h-5" />
            </div>
          </div>

          <!-- Content -->
          <div class="flex-1 min-w-0">
            <h3
              :class="[
                'font-bold text-sm mb-1 truncate',
                getTitleClasses()
              ]"
            >
              {{ title }}
            </h3>
            <p
              :class="[
                'text-sm break-words',
                getMessageClasses()
              ]"
            >
              {{ message }}
            </p>

            <!-- Progress bar for auto-hide -->
            <div
              v-if="autoHide && !showCloseButton"
              class="mt-2 w-full bg-gray-200/30 rounded-full h-1 overflow-hidden"
            >
              <div
                class="h-full rounded-full transition-all ease-linear"
                :class="getProgressBarClass()"
                :style="{ width: progressWidth + '%' }"
              ></div>
            </div>
          </div>

          <!-- Close button -->
          <button
            v-if="showCloseButton"
            @click="closeFlash"
            :class="[
              'flex-shrink-0 ml-3 p-1 rounded-full',
              'transition-colors duration-200',
              getCloseButtonClasses()
            ]"
          >
            <XMarkIcon class="w-4 h-4" />
          </button>
        </div>

        <!-- Additional visual elements for enhanced flash effect -->
        <div
          v-if="type === 'success'"
          class="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-ping"
        ></div>
        <div
          v-if="type === 'error'"
          class="absolute -top-1 -right-1 w-3 h-3 bg-red-400 rounded-full animate-pulse"
        ></div>
      </div>

      <!-- Glow effect overlay -->
      <div
        v-if="glowEffect"
        :class="[
          'absolute inset-0 rounded-lg blur-lg opacity-50',
          'animate-pulse',
          getGlowClasses()
        ]"
        style="transform: scale(1.1); z-index: -1;"
      ></div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import {
  CheckCircleIcon,
  ExclamationCircleIcon,
  XCircleIcon,
  InformationCircleIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
  },
  message: {
    type: String,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  autoHide: {
    type: Boolean,
    default: true
  },
  duration: {
    type: Number,
    default: 5000
  },
  showCloseButton: {
    type: Boolean,
    default: true
  },
  glowEffect: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close'])

const show = ref(false)
const progressWidth = ref(100)
const progressInterval = ref(null)
const hideTimeout = ref(null)

// Dynamic styles based on type
const dynamicStyles = computed(() => {
  const baseTransform = 'translateX(0)'
  const animations = {
    success: 'translateX(0) scale(1)',
    error: 'translateX(0) scale(1) rotateX(0deg)',
    warning: 'translateX(0) scale(1)',
    info: 'translateX(0) scale(1)'
  }
  return {
    transform: animations[props.type] || baseTransform
  }
})

// Computed properties for classes
const getContainerClasses = () => {
  const baseClasses = 'transform transition-all duration-300 hover:scale-105'
  const typeClasses = {
    success: 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-300 text-green-800 dark:from-green-900/90 dark:to-emerald-900/90 dark:border-green-600 dark:text-green-100',
    error: 'bg-gradient-to-r from-red-50 to-rose-50 border-red-300 text-red-800 dark:from-red-900/90 dark:to-rose-900/90 dark:border-red-600 dark:text-red-100',
    warning: 'bg-gradient-to-r from-yellow-50 to-amber-50 border-yellow-300 text-yellow-800 dark:from-yellow-900/90 dark:to-amber-900/90 dark:border-yellow-600 dark:text-yellow-100',
    info: 'bg-gradient-to-r from-blue-50 to-cyan-50 border-blue-300 text-blue-800 dark:from-blue-900/90 dark:to-cyan-900/90 dark:border-blue-600 dark:text-blue-100'
  }
  return `${baseClasses} ${typeClasses[props.type]}`
}

const getIconClasses = () => {
  const typeClasses = {
    success: 'bg-green-200 text-green-700 dark:bg-green-800 dark:text-green-200',
    error: 'bg-red-200 text-red-700 dark:bg-red-800 dark:text-red-200',
    warning: 'bg-yellow-200 text-yellow-700 dark:bg-yellow-800 dark:text-yellow-200',
    info: 'bg-blue-200 text-blue-700 dark:bg-blue-800 dark:text-blue-200'
  }
  return typeClasses[props.type]
}

const getTitleClasses = () => {
  const typeClasses = {
    success: 'text-green-800 dark:text-green-100',
    error: 'text-red-800 dark:text-red-100',
    warning: 'text-yellow-800 dark:text-yellow-100',
    info: 'text-blue-800 dark:text-blue-100'
  }
  return typeClasses[props.type]
}

const getMessageClasses = () => {
  const typeClasses = {
    success: 'text-green-700 dark:text-green-200',
    error: 'text-red-700 dark:text-red-200',
    warning: 'text-yellow-700 dark:text-yellow-200',
    info: 'text-blue-700 dark:text-blue-200'
  }
  return typeClasses[props.type]
}

const getCloseButtonClasses = () => {
  const typeClasses = {
    success: 'hover:bg-green-200 dark:hover:bg-green-800 text-green-600 dark:text-green-300',
    error: 'hover:bg-red-200 dark:hover:bg-red-800 text-red-600 dark:text-red-300',
    warning: 'hover:bg-yellow-200 dark:hover:bg-yellow-800 text-yellow-600 dark:text-yellow-300',
    info: 'hover:bg-blue-200 dark:hover:bg-blue-800 text-blue-600 dark:text-blue-300'
  }
  return typeClasses[props.type]
}

const getProgressBarClass = () => {
  const typeClasses = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    warning: 'bg-yellow-500',
    info: 'bg-blue-500'
  }
  return typeClasses[props.type]
}

const getGlowClasses = () => {
  const typeClasses = {
    success: 'bg-green-300',
    error: 'bg-red-300',
    warning: 'bg-yellow-300',
    info: 'bg-blue-300'
  }
  return typeClasses[props.type]
}

const getIcon = () => {
  const icons = {
    success: CheckCircleIcon,
    error: XCircleIcon,
    warning: ExclamationCircleIcon,
    info: InformationCircleIcon
  }
  return icons[props.type]
}

const startProgressAnimation = () => {
  if (!props.autoHide || props.showCloseButton) return

  const steps = 50
  const stepDuration = props.duration / steps
  let currentStep = steps

  progressInterval.value = setInterval(() => {
    currentStep--
    progressWidth.value = (currentStep / steps) * 100

    if (currentStep <= 0) {
      clearInterval(progressInterval.value)
      closeFlash()
    }
  }, stepDuration)
}

const closeFlash = () => {
  clearInterval(progressInterval.value)
  clearTimeout(hideTimeout.value)
  show.value = false
  emit('close')
}

const showFlash = () => {
  show.value = true
  progressWidth.value = 100

  if (props.autoHide) {
    hideTimeout.value = setTimeout(() => {
      closeFlash()
    }, props.duration)
  }

  startProgressAnimation()
}

// Lifecycle
onMounted(() => {
  showFlash()
})

onUnmounted(() => {
  clearInterval(progressInterval.value)
  clearTimeout(hideTimeout.value)
})

// Watch for changes to restart animation
watch(() => props.message, () => {
  showFlash()
})
</script>

<style scoped>
/* Enhanced slide animations from right */
.flash-slide-enter-active {
  transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.flash-slide-leave-active {
  transition: all 0.3s cubic-bezier(0.55, 0.055, 0.675, 0.19);
}

.flash-slide-enter-from {
  transform: translateX(120%) translateY(-20px) scale(0.8) rotateY(15deg);
  opacity: 0;
  filter: blur(8px);
}

.flash-slide-leave-to {
  transform: translateX(120%) translateY(-10px) scale(0.9) rotateY(-10deg);
  opacity: 0;
  filter: blur(4px);
}

/* Pulse animations for flash effect */
@keyframes flashPulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.02);
  }
}

@keyframes glowPulse {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.6;
  }
}

/* Error shake animation */
@keyframes errorShake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-2px); }
  20%, 40%, 60%, 80% { transform: translateX(2px); }
}

/* Success bounce animation */
@keyframes successBounce {
  0%, 20%, 53%, 80%, 100% {
    transform: translate3d(0, 0, 0);
  }
  40%, 43% {
    transform: translate3d(0, -5px, 0);
  }
  70% {
    transform: translate3d(0, -3px, 0);
  }
  90% {
    transform: translate3d(0, -1px, 0);
  }
}

/* Apply type-specific animations */
.flash-slide-enter-from[data-type="error"] {
  animation: errorShake 0.5s ease-in-out;
}

.flash-slide-enter-from[data-type="success"] {
  animation: successBounce 0.6s ease-in-out;
}

/* Smooth progress bar */
.transition-all {
  transition: all 0.3s ease-in-out;
}

/* Hover effects */
.hover\:scale-105:hover {
  transform: scale(1.05) translateY(-2px);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

/* Enhanced backdrop blur */
.backdrop-blur-sm {
  backdrop-filter: blur(8px);
}
</style>