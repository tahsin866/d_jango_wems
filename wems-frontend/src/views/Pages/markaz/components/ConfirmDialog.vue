<template>
  <Dialog v-model:visible="visibleLocal" modal :closable="false" :style="{ width: '520px' }" class="!rounded-md">
    <template #header>
      <div
            style="font-family: 'SolaimanLipi', sans-serif;"
      class="flex items-center gap-4">
        <div class="w-14 h-14 bg-amber-50 rounded-lg flex items-center justify-center">
          <svg class="w-7 h-7 text-amber-600" viewBox="0 0 24 24" fill="none"><path d="M12 2l9 19H3L12 2z" stroke="currentColor" stroke-width="1.25"/></svg>
        </div>
        <div>
          <div class="text-lg font-bold">{{ title }}</div>
        </div>
      </div>
    </template>

    <div
          style="font-family: 'SolaimanLipi', sans-serif;"
    class="p-6 text-center">
      <p class="text-base text-slate-700 dark:text-slate-200">{{ description }}</p>
    </div>

    <template #footer>
      <div

      style="font-family: 'SolaimanLipi', sans-serif;"
      class="flex justify-end gap-3 p-3">
        <button @click="cancel" class="px-5 py-2.5 rounded-md bg-white border border-slate-200 text-slate-700 hover:bg-slate-50">{{ cancelLabel }}</button>
        <button @click="confirm" class="px-5 py-2.5 rounded-md bg-amber-500 text-white hover:bg-amber-600">{{ confirmLabel }}</button>
      </div>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import Dialog from 'primevue/dialog';
import { ref, watch } from 'vue';

/**
 * Accept both modelValue (default v-model) and visible (v-model:visible)
 * so the component works whether parent uses v-model or v-model:visible.
 */
const props = defineProps<{
  modelValue?: boolean;
  visible?: boolean;
  title?: string;
  description?: string;
  confirmLabel?: string;
  cancelLabel?: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', v: boolean): void;
  (e: 'update:visible', v: boolean): void;
  (e: 'confirm'): void;
}>();

/**
 * local visible state that syncs with either props.modelValue or props.visible
 */
const visibleLocal = ref<boolean>(!!(props.visible ?? props.modelValue));

/**
 * Keep local state in sync when parent changes either prop
 */
watch(
  () => props.visible,
  v => {
    if (v !== undefined) visibleLocal.value = !!v;
  }
);
watch(
  () => props.modelValue,
  v => {
    if (v !== undefined) visibleLocal.value = !!v;
  }
);

/**
 * When local changes (from UI actions), emit updates for both v-model variants
 * so parent receives the change whether it used v-model or v-model:visible.
 */
watch(visibleLocal, v => {
  emit('update:modelValue', v);
  emit('update:visible', v);
});

const title = props.title ?? 'Confirm';
const description = props.description ?? '';
const confirmLabel = props.confirmLabel ?? 'Confirm';
const cancelLabel = props.cancelLabel ?? 'Cancel';

function confirm() {
  // emit the confirm event to let parent handle the action
  emit('confirm');
  // close dialog
  visibleLocal.value = false;
}

function cancel() {
  // close dialog (will emit update:modelValue & update:visible via watcher)
  visibleLocal.value = false;
}
</script>

<style scoped>
/* relies on Tailwind for visuals */
</style>
