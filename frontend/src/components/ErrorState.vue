<template>
  <div class="max-w-2xl mx-auto text-center py-16">
    <div class="inline-flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mb-6">
      <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
        ></path>
      </svg>
    </div>

    <h3 class="text-xl font-semibold text-gray-900 mb-4">{{ title }}</h3>

    <!-- Enhanced error message display -->
    <div class="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
      <p class="text-red-800 text-sm leading-relaxed">{{ message }}</p>

      <!-- Additional help for specific errors -->
      <div
        v-if="isDatasetNotFound"
        class="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg"
      >
        <div class="flex items-start space-x-2">
          <svg
            class="w-5 h-5 text-yellow-600 mt-0.5 flex-shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
          </svg>
          <div class="text-yellow-800 text-sm">
            <p class="font-medium mb-1">Dataset might not be available</p>
            <p>
              This dataset code might not exist in INE's database or might have been moved. Try
              browsing available datasets instead.
            </p>
          </div>
        </div>
      </div>

      <div v-if="isConnectionError" class="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <div class="flex items-start space-x-2">
          <svg
            class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"
            ></path>
          </svg>
          <div class="text-blue-800 text-sm">
            <p class="font-medium mb-1">Connection Issue</p>
            <p>
              Please check if the backend service is running on
              <code class="bg-blue-100 px-1 rounded">{{ import.meta.env.VITE_API_BASE_URL }}</code>
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="space-x-4">
      <button
        @click="$emit('retry')"
        class="inline-flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl shadow-lg hover:shadow-xl transition-all duration-200"
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
          ></path>
        </svg>
        {{ retryText }}
      </button>

      <button
        @click="$emit('goHome')"
        class="inline-flex items-center px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-medium rounded-xl shadow-lg hover:shadow-xl transition-all duration-200"
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
          ></path>
        </svg>
        Go to Datasets
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    title?: string
    message: string
    retryText?: string
  }>(),
  {
    title: 'Something went wrong',
    retryText: 'Try Again',
  },
)

defineEmits<{
  retry: []
  goHome: []
}>()

const isDatasetNotFound = computed(
  () =>
    props.message.includes('404') ||
    props.message.includes('not exist') ||
    props.message.includes('HTML error page'),
)

const isConnectionError = computed(
  () =>
    props.message.includes('connect') ||
    props.message.includes('fetch') ||
    props.message.includes('backend service'),
)
</script>
