<template>
  <div class="text-center py-20">
    <div class="inline-flex items-center justify-center w-20 h-20 bg-gray-100 rounded-full mb-8">
      <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
        ></path>
      </svg>
    </div>
    <h3 class="text-2xl font-semibold text-gray-900 mb-4">{{ title }}</h3>
    <p class="text-gray-600 mb-8 max-w-md mx-auto">{{ description }}</p>

    <div class="space-x-4">
      <button
        v-if="showPrimaryAction"
        @click="$emit('primaryAction')"
        class="inline-flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl shadow-lg hover:shadow-xl transition-all duration-200"
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
          ></path>
        </svg>
        {{ primaryActionText }}
      </button>

      <button
        v-if="showSecondaryAction"
        @click="$emit('secondaryAction')"
        class="inline-flex items-center px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-medium rounded-xl shadow-lg hover:shadow-xl transition-all duration-200"
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M6 18L18 6M6 6l12 12"
          ></path>
        </svg>
        {{ secondaryActionText }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    title: string
    description: string
    showPrimaryAction?: boolean
    primaryActionText?: string
    showSecondaryAction?: boolean
    secondaryActionText?: string
  }>(),
  {
    primaryActionText: 'Load Data',
    secondaryActionText: 'Clear',
  },
)

defineEmits<{
  primaryAction: []
  secondaryAction: []
}>()
</script>
