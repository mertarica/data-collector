<template>
  <div
    class="group bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg hover:shadow-2xl border border-gray-200/50 hover:border-blue-300/50 cursor-pointer transition-all duration-300 hover:-translate-y-1"
    @click="$emit('click', dataset)"
  >
    <div class="flex items-start justify-between mb-4">
      <div class="flex items-center space-x-3">
        <!-- Provider Badge -->
        <div
          class="flex items-center space-x-2 px-2 py-1 rounded-lg text-xs font-medium bg-blue-100 text-blue-800"
        >
          <div class="w-2 h-2 rounded-full bg-blue-500"></div>
          <span>INE</span>
        </div>

        <span
          class="inline-flex items-center px-3 py-1.5 bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-800 text-sm font-mono font-medium rounded-lg"
        >
          {{ dataset.codigo }}
        </span>

        <span v-if="dataset.cod_ioe" class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-md">
          ID: {{ dataset.cod_ioe }}
        </span>
      </div>

      <svg
        class="w-5 h-5 text-gray-400 group-hover:text-blue-500 group-hover:translate-x-1 transition-all duration-200"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9 5l7 7-7 7"
        ></path>
      </svg>
    </div>

    <h3
      class="font-semibold text-gray-900 group-hover:text-blue-900 transition-colors duration-200 leading-relaxed mb-3"
    >
      {{ dataset.nombre }}
    </h3>

    <div class="mt-4 pt-4 border-t border-gray-100">
      <div class="flex items-center justify-between">
        <div class="flex items-center text-sm text-gray-500">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
          </svg>
          Click to view data
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Dataset } from '../services/api'

defineProps<{
  dataset: Dataset
}>()

defineEmits<{
  click: [dataset: Dataset]
}>()
</script>
