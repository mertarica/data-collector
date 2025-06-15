<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">INE Datasets</h1>
        <p class="mt-2 text-sm text-gray-600">
          Explore and access Spanish National Statistics Institute datasets
        </p>
      </div>
      <div class="flex items-center space-x-2 text-sm text-gray-500">
        <span>Total: {{ store.datasetsCount }}</span>
        <span v-if="store.loading" class="text-blue-600">Loading...</span>
      </div>
    </div>

    <!-- Search Bar -->
    <div class="card">
      <div class="flex space-x-4">
        <div class="flex-1">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search datasets by name or code..."
            class="input-field"
            @input="handleSearch"
          />
        </div>
        <button
          @click="handleRefresh"
          class="btn-secondary"
          :disabled="store.loading"
        >
          🔄 Refresh
        </button>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="store.error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <div class="flex">
        <div class="text-red-600">❌</div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">Error</h3>
          <div class="mt-2 text-sm text-red-700">{{ store.error }}</div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="store.loading && store.datasets.length === 0" class="card">
      <div class="flex items-center justify-center py-12">
        <div class="text-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p class="mt-2 text-sm text-gray-600">Loading datasets...</p>
        </div>
      </div>
    </div>

    <!-- Datasets Grid -->
    <div v-else-if="store.datasets.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="dataset in store.datasets"
        :key="dataset.codigo"
        class="card hover:shadow-lg transition-shadow duration-200 cursor-pointer"
        @click="viewDataset(dataset)"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <h3 class="font-semibold text-gray-900 mb-2">
              {{ dataset.codigo }}
            </h3>
            <p class="text-sm text-gray-600 mb-3 line-clamp-3">
              {{ dataset.nombre }}
            </p>
            <div class="flex items-center space-x-2 text-xs text-gray-500">
              <span v-if="dataset.cod_ioe" class="bg-blue-100 text-blue-800 px-2 py-1 rounded">
                IOE: {{ dataset.cod_ioe }}
              </span>
            </div>
          </div>
          <div class="ml-4">
            <button class="text-blue-600 hover:text-blue-800">
              →
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!store.loading" class="card">
      <div class="text-center py-12">
        <div class="text-6xl mb-4">📊</div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No datasets found</h3>
        <p class="text-gray-600 mb-4">
          {{ searchQuery ? 'Try adjusting your search terms' : 'Click refresh to load datasets' }}
        </p>
        <button @click="handleRefresh" class="btn-primary">
          Load Datasets
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDatasetsStore } from '../stores/datasets'
import type { Dataset } from '../services/api'

const router = useRouter()
const store = useDatasetsStore()

// Local state
const searchQuery = ref('')
const searchTimeout = ref<number | null>(null)

// Methods
const handleSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
  
  searchTimeout.value = setTimeout(() => {
    if (searchQuery.value.trim()) {
      store.searchDatasets(searchQuery.value.trim())
    } else {
      store.fetchDatasets()
    }
  }, 300)
}

const handleRefresh = () => {
  searchQuery.value = ''
  store.fetchDatasets()
}

const viewDataset = (dataset: Dataset) => {
  router.push(`/dataset/${dataset.codigo}`)
}

// Lifecycle
onMounted(async () => {
  console.log('HomeView mounted, fetching datasets...') // Debug log
  await store.fetchDatasets()
})
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>