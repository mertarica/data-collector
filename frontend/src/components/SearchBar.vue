<template>
  <div class="max-w-2xl mx-auto mb-12">
    <div class="relative group">
      <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
        <svg
          class="w-5 h-5 text-gray-400 group-focus-within:text-blue-500 transition-colors"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          ></path>
        </svg>
      </div>
      <input
        :value="modelValue"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        type="text"
        :placeholder="placeholder"
        class="w-full pl-12 pr-4 py-4 text-lg bg-white/80 backdrop-blur-sm border-2 border-gray-200 rounded-2xl shadow-lg focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition-all duration-300 placeholder-gray-500"
      />
      <div class="absolute inset-y-0 right-0 pr-4 flex items-center">
        <div
          v-if="modelValue && resultCount !== undefined"
          class="text-sm text-gray-400 bg-gray-100 px-2 py-1 rounded-lg"
        >
          {{ resultCount }} found
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: string
  placeholder?: string
  resultCount?: number
}>()

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>
