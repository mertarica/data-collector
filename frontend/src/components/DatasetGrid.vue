<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <DatasetCard
      v-for="dataset in datasets"
      :key="dataset.id"
      :dataset="dataset"
      @click="$emit('datasetClick', $event)"
    />
  </div>
</template>

<script setup lang="ts">
import DatasetCard from './DatasetCard.vue'
import type { Dataset } from '../services/api'

defineProps<{
  datasets: Dataset[]
}>()

defineEmits<{
  datasetClick: [dataset: Dataset]
}>()
</script>
