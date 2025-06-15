<template>
  <div class="text-center py-16">
    <div class="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-6">
      <div
        class="w-8 h-8 border-3 border-blue-200 border-t-blue-600 rounded-full animate-spin"
      ></div>
    </div>
    <h3 class="text-xl font-semibold text-gray-700 mb-2">{{ title }}</h3>
    <p class="text-gray-500">{{ subtitle }}</p>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    title?: string
    subtitle?: string
  }>(),
  {
    title: 'Loading...',
    subtitle: 'Please wait',
  },
)
</script>
