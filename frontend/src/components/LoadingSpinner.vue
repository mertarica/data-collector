<template>
  <div class="flex items-center justify-center p-4">
    <div class="flex items-center space-x-2">
      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
      <span class="text-gray-600">{{ message }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  message?: string
}>()
</script>
