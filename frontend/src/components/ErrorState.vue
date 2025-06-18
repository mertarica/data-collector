<template>
  <div
    class="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 flex items-center justify-center p-4"
  >
    <div class="max-w-md w-full">
      <div class="bg-white rounded-2xl shadow-xl p-8 text-center">
        <div
          class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4"
        >
          <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
            ></path>
          </svg>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 mb-2">Connection Error</h2>
        <p class="text-gray-600 mb-6">
          Unable to connect to the backend service.
          <br />
          <span class="text-sm">
            Please check if the backend service is running on
            <code class="bg-blue-100 px-1 rounded">{{ apiBaseUrl }}</code>
          </span>
        </p>

        <button
          @click="$emit('retry')"
          class="w-full bg-red-600 hover:bg-red-700 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200"
        >
          Try Again
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Expose environment variable to template
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Define emits
defineEmits<{
  retry: []
}>()
</script>
