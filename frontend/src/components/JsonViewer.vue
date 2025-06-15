<template>
  <div
    class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-200/50 overflow-hidden"
  >
    <div class="p-6 border-b border-gray-200/50 bg-gray-50/50">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2 text-sm text-gray-500">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"
              ></path>
            </svg>
            <span>JSON Format</span>
          </div>
          <button
            @click="copyToClipboard"
            class="inline-flex items-center px-3 py-1.5 bg-blue-100 hover:bg-blue-200 text-blue-700 text-sm font-medium rounded-lg transition-colors duration-200"
            :class="{ 'bg-green-100 text-green-700': copied }"
          >
            <svg
              v-if="!copied"
              class="w-4 h-4 mr-1.5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
              ></path>
            </svg>
            <svg
              v-else
              class="w-4 h-4 mr-1.5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 13l4 4L19 7"
              ></path>
            </svg>
            {{ copied ? 'Copied!' : 'Copy All' }}
          </button>
        </div>
      </div>
    </div>
    <div class="p-6">
      <div class="bg-gray-900 rounded-xl overflow-hidden">
        <div class="bg-gray-800 px-4 py-2 flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <div class="w-3 h-3 bg-red-500 rounded-full"></div>
            <div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
            <div class="w-3 h-3 bg-green-500 rounded-full"></div>
          </div>
          <span class="text-gray-400 text-xs font-mono">{{ filename }}</span>
        </div>
        <pre
          class="text-sm text-gray-300 p-4 overflow-auto max-h-96 leading-relaxed font-mono custom-scrollbar"
          >{{ formattedData }}</pre
        >
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

const props = withDefaults(
  defineProps<{
    data: any
    title?: string
    filename?: string
  }>(),
  {
    title: 'JSON Data',
    filename: 'data.json',
  },
)

const copied = ref(false)

const formattedData = computed(() => {
  return JSON.stringify(props.data, null, 2)
})

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(formattedData.value)
    copied.value = true

    // Reset copied state after 2 seconds
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy to clipboard:', err)

    // Fallback for older browsers
    const textArea = document.createElement('textarea')
    textArea.value = formattedData.value
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)

    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  }
}
</script>
