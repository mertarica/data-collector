<template>
  <div class="mb-8">
    <div class="flex flex-wrap gap-3 justify-center">
      <!-- All Providers -->
      <button
        @click="selectProvider('all')"
        class="provider-chip"
        :class="{ active: selectedProvider === 'all' }"
      >
        <div
          class="w-8 h-8 bg-gradient-to-r from-gray-500 to-gray-600 rounded-lg flex items-center justify-center mr-3"
        >
          <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 00-2 2v0a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2"
            ></path>
          </svg>
        </div>
        <div class="flex-1">
          <div class="font-medium">All Providers</div>
          <div class="text-sm opacity-75">{{ totalDatasets }} datasets</div>
        </div>
      </button>

      <!-- Individual Providers -->
      <button
        v-for="provider in enabledProviders"
        :key="provider.id"
        @click="selectProvider(provider.id)"
        class="provider-chip"
        :class="{ active: selectedProvider === provider.id }"
      >
        <div
          class="w-8 h-8 rounded-lg flex items-center justify-center mr-3"
          :class="`bg-gradient-to-r from-${provider.color}-500 to-${provider.color}-600`"
        >
          <span class="text-white font-bold text-sm">{{ provider.name.substring(0, 2) }}</span>
        </div>
        <div class="flex-1">
          <div class="font-medium">{{ provider.name }}</div>
          <div class="text-sm opacity-75">
            {{ datasetCountByProvider[provider.id] || 0 }} datasets
          </div>
        </div>
        <div
          v-if="!provider.enabled"
          class="ml-2 text-xs bg-amber-100 text-amber-800 px-2 py-1 rounded-full"
        >
          Soon
        </div>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useProvidersStore } from '../stores/providers'

const providersStore = useProvidersStore()
const { enabledProviders, selectedProvider, totalDatasets, datasetCountByProvider } =
  storeToRefs(providersStore)

const selectProvider = (providerId: string) => {
  providersStore.setSelectedProvider(providerId)
}
</script>

<style scoped>
.provider-chip {
  @apply flex items-center p-4 bg-white/70 backdrop-blur-sm border-2 border-gray-200/50 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 min-w-[200px];
}

.provider-chip.active {
  @apply border-blue-300 bg-blue-50/70 ring-2 ring-blue-500/20;
}

.provider-chip:hover {
  @apply border-gray-300/70 transform scale-105;
}

.provider-chip.active:hover {
  @apply border-blue-400;
}
</style>
