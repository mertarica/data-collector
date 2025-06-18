<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 lg:py-12">
      <!-- Page Header -->
      <PageHeader
        title="INE Datasets"
        :subtitle="`Spanish National Statistics Institute data explorer with ${store.datasetsCount} datasets available`"
      />

      <!-- Search Bar -->
      <SearchBar
        v-model="searchQuery"
        placeholder="Search datasets by name, code, or ID..."
        :result-count="filteredDatasets.length"
      />

      <!-- Loading State -->
      <LoadingState
        v-if="store.loading"
        title="Loading datasets..."
        subtitle="Fetching the latest data from INE"
      />

      <!-- Error State -->
      <ErrorState v-else-if="store.error" :message="store.error" @retry="handleRefresh" />

      <!-- Dataset Grid -->
      <DatasetGrid
        v-else-if="filteredDatasets.length > 0"
        :datasets="filteredDatasets"
        @dataset-click="viewDataset"
      />

      <!-- Empty State -->
      <EmptyState
        v-else
        :title="searchQuery ? 'No datasets found' : 'No datasets available'"
        :description="
          searchQuery
            ? 'Try adjusting your search terms or browse all available datasets.'
            : 'Load the available datasets to get started with data exploration.'
        "
        :show-primary-action="!searchQuery"
        primary-action-text="Load Datasets"
        :show-secondary-action="!!searchQuery"
        secondary-action-text="Clear Search"
        @primary-action="handleRefresh"
        @secondary-action="searchQuery = ''"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDatasetsStore } from '../stores/datasets'
import type { Dataset } from '../services/api'

// Components
import PageHeader from '../components/PageHeader.vue'
import SearchBar from '../components/SearchBar.vue'
import LoadingState from '../components/LoadingState.vue'
import ErrorState from '../components/ErrorState.vue'
import DatasetGrid from '../components/DatasetGrid.vue'
import EmptyState from '../components/EmptyState.vue'

const router = useRouter()
const store = useDatasetsStore()

const searchQuery = ref('')

// Filter datasets based on search
const filteredDatasets = computed(() => {
  if (!searchQuery.value.trim()) {
    return store.datasets
  }

  const query = searchQuery.value.toLowerCase()
  return store.datasets.filter(
    (dataset) =>
      dataset.external_id.toLowerCase().includes(query) ||
      dataset.name.toLowerCase().includes(query) ||
      dataset.dataset_name.toLowerCase().includes(query),
  )
})

const handleRefresh = () => {
  searchQuery.value = ''
  store.fetchDatasets()
}

const viewDataset = (dataset: Dataset) => {
  router.push(`/dataset/${dataset.external_id}`)
}

onMounted(() => {
  store.fetchDatasets()
})
</script>
