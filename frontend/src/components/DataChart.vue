<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick, type ComputedRef } from 'vue'
import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  LineController,
  Title,
  Tooltip,
  Legend,
  TimeScale,
  type ChartConfiguration,
} from 'chart.js'
import 'chartjs-adapter-date-fns'

// Register Chart.js components
Chart.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  LineController,
  Title,
  Tooltip,
  Legend,
  TimeScale,
)

interface Props {
  data: any
  dataType: 'raw' | 'processed'
}

const props = defineProps<Props>()

// Reactive variables
const chartRef = ref<HTMLCanvasElement>()
const viewMode = ref<'chart' | 'table'>(props.dataType === 'raw' ? 'chart' : 'table')
const currentPage = ref(1)
const pageSize = ref(25)
const selectedSeries = ref<string>('')
const hiddenDatasets = ref<Set<number>>(new Set())
let chartInstance: Chart | null = null

// Computed properties
const sourceData = computed(() => {
  if (!props.data) return []
  return props.dataType === 'raw' ? props.data.data || [] : props.data.summary || []
})

const chartData = computed(() => {
  if (!sourceData.value.length || props.dataType !== 'raw') return []

  return sourceData.value
    .map((series: any, index: number) => {
      if (!series.data_points?.length) return null

      const seriesData = series.data_points
        .filter((point: any) => point.timestamp_ms && point.value !== null && !point.is_secret)
        .map((point: any) => ({
          x: new Date(point.timestamp_ms),
          y: parseFloat(point.value),
        }))
        .filter((point: any) => !isNaN(point.x.getTime()) && !isNaN(point.y))
        .sort((a: any, b: any) => a.x.getTime() - b.x.getTime())

      if (!seriesData.length) return null

      return {
        label: series.name || series.code || `Series ${index + 1}`,
        data: seriesData,
        borderColor: getColor(index),
        backgroundColor: getColor(index, 0.1),
        borderWidth: 2,
        fill: false,
        tension: 0.1,
        pointRadius: 2,
        pointHoverRadius: 4,
      }
    })
    .filter(Boolean)
})

const tableData = computed(() => {
  if (props.dataType === 'raw') {
    const rows: any[] = []
    sourceData.value.forEach((series: any) => {
      if (!series.data_points?.length) return

      series.data_points.forEach((point: any) => {
        if (point.timestamp_ms && point.value !== null && !point.is_secret) {
          rows.push({
            date: point.timestamp_ms,
            dateFormatted: formatDate(point.timestamp_ms),
            series: series.code || 'Unknown',
            seriesName: series.name || series.code || 'Unknown Series',
            value: point.value,
            year: point.year,
            period: point.period_id,
            confidentiality: 'Public',
          })
        }
      })
    })
    return rows.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
  } else {
    return sourceData.value.map((item: any, index: number) => ({
      index: index + 1,
      code: item.code || 'N/A',
      indicator_name: item.indicator_name || 'N/A',
      unit_description: item.unit_description || 'N/A',
      frequency_name: item.frequency_name || 'N/A',
      year: item.year || 'N/A',
      value: item.value || 'N/A',
      data_confidentiality: item.data_confidentiality || 'N/A',
    }))
  }
})

const filteredTableData = computed(() => {
  if (!selectedSeries.value) return tableData.value

  const filterKey = props.dataType === 'raw' ? 'series' : 'code'
  return tableData.value.filter(
    (row: { [x: string]: string }) => row[filterKey] === selectedSeries.value,
  )
})

const paginatedTableData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredTableData.value.slice(start, start + pageSize.value)
})

const totalPages = computed(() => Math.ceil(filteredTableData.value.length / pageSize.value))

const uniqueSeries = computed(() => {
  if (props.dataType === 'raw') {
    return [...new Set(tableData.value.map((row: { series: string }) => row.series))]
  } else {
    const seriesMap = new Map()
    tableData.value.forEach((row: { code: string; indicator_name: string }) => {
      if (row.code !== 'N/A' && row.indicator_name !== 'N/A') {
        seriesMap.set(row.code, `${row.code} - ${row.indicator_name}`)
      }
    })
    return Array.from(seriesMap.entries()).map(([code, display]) => ({ code, display }))
  }
}) as ComputedRef<string[] | { code: string; display: string }[]>

const hasData = computed(() => chartData.value.length > 0)
const seriesCount = computed(() =>
  props.dataType === 'raw' ? chartData.value.length : sourceData.value.length,
)

// Helper functions
function formatDate(timestamp: number): string {
  return new Date(timestamp).toLocaleDateString('tr-TR')
}

function getColor(index: number, alpha: number = 1): string {
  const colors = [
    `rgba(59, 130, 246, ${alpha})`,
    `rgba(16, 185, 129, ${alpha})`,
    `rgba(245, 101, 101, ${alpha})`,
    `rgba(139, 92, 246, ${alpha})`,
    `rgba(245, 158, 11, ${alpha})`,
    `rgba(236, 72, 153, ${alpha})`,
    `rgba(20, 184, 166, ${alpha})`,
    `rgba(251, 113, 133, ${alpha})`,
  ]
  return colors[index % colors.length]
}

function viewButtonClass(mode: string): string {
  const base = 'px-3 py-1 text-sm font-medium rounded-md transition-all duration-200'
  return `${base} ${viewMode.value === mode ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-600 hover:text-gray-900'}`
}

function goToPage(page: number) {
  currentPage.value = page
}

function resetFilters() {
  selectedSeries.value = ''
  currentPage.value = 1
}

// Chart functions
function toggleDataset(datasetIndex: number) {
  if (!chartInstance) return
  const meta = chartInstance.getDatasetMeta(datasetIndex)
  meta.hidden = !meta.hidden
  chartInstance.update()

  if (meta.hidden) {
    hiddenDatasets.value.add(datasetIndex)
  } else {
    hiddenDatasets.value.delete(datasetIndex)
  }
}

function selectAllDatasets() {
  if (!chartInstance) return
  chartInstance.data.datasets.forEach((_, index) => {
    chartInstance!.getDatasetMeta(index).hidden = false
  })
  chartInstance.update()
  hiddenDatasets.value.clear()
}

function unselectAllDatasets() {
  if (!chartInstance) return
  chartInstance.data.datasets.forEach((_, index) => {
    const meta = chartInstance!.getDatasetMeta(index)
    meta.hidden = true
    hiddenDatasets.value.add(index)
  })
  chartInstance.update()
}

const createChart = async () => {
  if (!chartRef.value || !hasData.value) return

  await nextTick()
  const ctx = chartRef.value.getContext('2d')
  if (!ctx) return

  if (chartInstance) chartInstance.destroy()

  const config: ChartConfiguration = {
    type: 'line',
    data: { datasets: chartData.value },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        title: {
          display: true,
          text: 'Raw Data Time Series',
          font: { size: 16, weight: 'bold' },
          padding: 20,
        },
        legend: { display: false },
        tooltip: {
          callbacks: {
            title: (context) =>
              context[0].parsed.x ? new Date(context[0].parsed.x).toLocaleDateString('tr-TR') : '',
            label: (context) => `${context.dataset.label}: ${context.parsed.y}`,
          },
        },
      },
      scales: {
        x: {
          type: 'time',
          time: { unit: 'quarter', displayFormats: { quarter: 'MMM yyyy' } },
          title: { display: true, text: 'Date', font: { size: 12, weight: 'bold' } },
          ticks: { maxRotation: 45, font: { size: 10 } },
        },
        y: {
          title: { display: true, text: 'Value', font: { size: 12, weight: 'bold' } },
          ticks: { font: { size: 10 } },
        },
      },
      layout: { padding: 10 },
    },
  }

  try {
    chartInstance = new Chart(ctx, config)
    // Restore hidden state
    hiddenDatasets.value.forEach((index) => {
      if (chartInstance?.getDatasetMeta(index)) {
        chartInstance.getDatasetMeta(index).hidden = true
      }
    })
    if (hiddenDatasets.value.size > 0) chartInstance.update()
  } catch (error) {
    console.error('Error creating chart:', error)
  }
}

// Watchers
watch(
  [() => props.data, () => props.dataType],
  () => {
    if (viewMode.value === 'chart') createChart()
  },
  { deep: true },
)

watch(viewMode, (newMode) => {
  if (newMode === 'chart') nextTick(() => createChart())
})

watch(selectedSeries, () => {
  currentPage.value = 1
})

watch(
  () => props.dataType,
  (newDataType) => {
    viewMode.value = newDataType === 'raw' ? 'chart' : 'table'
    resetFilters()
  },
  { immediate: true },
)

// Lifecycle
onMounted(() => {
  if (hasData.value && viewMode.value === 'chart') createChart()
})

onUnmounted(() => {
  if (chartInstance) chartInstance.destroy()
})
</script>

<template>
  <div class="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-gray-200/50">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h3 class="text-lg font-semibold text-gray-900">Data Visualization</h3>
        <p class="text-sm text-gray-600">
          {{
            dataType === 'raw'
              ? `Time series chart showing ${seriesCount} data series`
              : `Processed data table showing ${seriesCount} data points`
          }}
        </p>
      </div>

      <!-- View Toggle - Only for raw data -->
      <div v-if="dataType === 'raw'" class="flex items-center space-x-2">
        <span class="text-sm font-medium text-gray-700">View:</span>
        <div class="relative inline-flex bg-gray-100 rounded-lg p-1">
          <button @click="viewMode = 'chart'" :class="viewButtonClass('chart')">Chart</button>
          <button @click="viewMode = 'table'" :class="viewButtonClass('table')">Table</button>
        </div>
      </div>
    </div>

    <!-- Raw Data: Chart or Table -->
    <template v-if="dataType === 'raw'">
      <!-- Chart View -->
      <div v-if="viewMode === 'chart'" class="relative">
        <div v-if="!hasData" class="flex flex-col items-center justify-center h-64 text-gray-500">
          <svg class="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
          </svg>
          <p class="text-lg font-medium">No chart data available</p>
          <p class="text-sm">
            This dataset doesn't contain time series data suitable for visualization.
          </p>
        </div>

        <div v-else class="space-y-4">
          <!-- Chart Legend Controls -->
          <div v-if="chartData.length > 1" class="bg-gray-50 rounded-lg p-4">
            <div class="flex items-center justify-between mb-3">
              <h4 class="text-sm font-medium text-gray-700">Chart Series</h4>
              <div class="flex space-x-2">
                <button
                  @click="selectAllDatasets"
                  class="px-2 py-1 text-xs font-medium text-blue-600 bg-blue-50 rounded hover:bg-blue-100 transition-colors"
                >
                  Select All
                </button>
                <button
                  @click="unselectAllDatasets"
                  class="px-2 py-1 text-xs font-medium text-gray-600 bg-gray-100 rounded hover:bg-gray-200 transition-colors"
                >
                  Unselect All
                </button>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
              <button
                v-for="(dataset, index) in chartData"
                :key="index"
                @click="toggleDataset(index)"
                :class="[
                  'flex items-center space-x-2 p-2 rounded text-left text-sm transition-all',
                  hiddenDatasets.has(index)
                    ? 'bg-gray-100 text-gray-400'
                    : 'bg-white text-gray-700 hover:bg-gray-50',
                ]"
              >
                <div
                  :style="{ backgroundColor: dataset.borderColor }"
                  class="w-3 h-3 rounded-full"
                ></div>
                <span class="truncate" :title="dataset.label">
                  {{
                    dataset.label.length > 30
                      ? dataset.label.substring(0, 27) + '...'
                      : dataset.label
                  }}
                </span>
              </button>
            </div>
          </div>

          <!-- Chart Canvas -->
          <div class="h-[500px] bg-white rounded-lg border">
            <canvas ref="chartRef" class="w-full h-full"></canvas>
          </div>
        </div>
      </div>

      <!-- Table View -->
      <div v-else>
        <!-- Filters -->
        <div class="flex flex-col sm:flex-row gap-4 p-4 bg-gray-50 rounded-lg mb-4">
          <div class="flex-1">
            <label class="block text-sm font-medium text-gray-700 mb-1">Filter by Series:</label>
            <select
              v-model="selectedSeries"
              class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Series</option>
              <option
                v-for="series in uniqueSeries"
                :key="typeof series === 'string' ? series : series.code"
                :value="typeof series === 'string' ? series : series.code"
              >
                {{ typeof series === 'string' ? series : series.display }}
              </option>
            </select>
          </div>
          <div class="flex items-end">
            <button
              @click="resetFilters"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Reset Filters
            </button>
          </div>
        </div>

        <!-- Table -->
        <div class="overflow-x-auto mb-4">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="table-header">Date</th>
                <th class="table-header">Series</th>
                <th class="table-header">Value</th>
                <th class="table-header">Year</th>
                <th class="table-header">Period</th>
                <th class="table-header">Confidentiality</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="row in paginatedTableData" :key="`${row.series}-${row.date}`">
                <td class="table-cell text-gray-900">{{ row.dateFormatted }}</td>
                <td class="table-cell text-gray-900">{{ row.seriesName }}</td>
                <td class="table-cell font-medium text-blue-600">{{ row.value }}</td>
                <td class="table-cell text-gray-500">{{ row.year }}</td>
                <td class="table-cell text-gray-500">{{ row.period }}</td>
                <td class="table-cell text-gray-500">{{ row.confidentiality }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <!-- Processed Data: Table Only -->
    <template v-else>
      <!-- Filters -->
      <div class="flex flex-col sm:flex-row gap-4 p-4 bg-gray-50 rounded-lg mb-4">
        <div class="flex-1">
          <label class="block text-sm font-medium text-gray-700 mb-1">Filter by Series:</label>
          <select
            v-model="selectedSeries"
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Series</option>
            <option
              v-for="item in uniqueSeries"
              :key="(item as any).code"
              :value="(item as any).code"
            >
              {{ (item as any).display }}
            </option>
          </select>
        </div>
        <div class="flex items-end">
          <button
            @click="resetFilters"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Reset Filters
          </button>
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto mb-4">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="table-header">#</th>
              <th class="table-header">Code</th>
              <th class="table-header">Indicator</th>
              <th class="table-header">Value</th>
              <th class="table-header">Year</th>
              <th class="table-header">Unit</th>
              <th class="table-header">Frequency</th>
              <th class="table-header">Confidentiality</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="row in paginatedTableData" :key="row.index">
              <td class="table-cell text-gray-500">{{ row.index }}</td>
              <td class="table-cell font-mono text-blue-600">{{ row.code }}</td>
              <td class="table-cell text-gray-900">{{ row.indicator_name }}</td>
              <td class="table-cell font-medium text-green-600">{{ row.value }}</td>
              <td class="table-cell text-gray-500">{{ row.year }}</td>
              <td class="table-cell text-gray-500">{{ row.unit_description }}</td>
              <td class="table-cell text-gray-500">{{ row.frequency_name }}</td>
              <td class="table-cell text-xs">
                <span
                  :class="
                    row.data_confidentiality === 'Public data — freely available'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  "
                  class="px-2 py-1 rounded-full"
                >
                  {{ row.data_confidentiality }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
      <div class="text-sm text-gray-700">
        Showing {{ (currentPage - 1) * pageSize + 1 }} to
        {{ Math.min(currentPage * pageSize, filteredTableData.length) }} of
        {{ filteredTableData.length }} results
      </div>

      <div class="flex items-center space-x-2">
        <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-3 py-1 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
        >
          Previous
        </button>

        <div class="flex space-x-1">
          <button
            v-for="page in Math.min(totalPages, 5)"
            :key="page"
            @click="goToPage(page)"
            :class="[
              'px-3 py-1 text-sm font-medium rounded-md',
              currentPage === page
                ? 'bg-blue-600 text-white'
                : 'text-gray-700 bg-white border border-gray-300 hover:bg-gray-50',
            ]"
          >
            {{ page }}
          </button>
        </div>

        <button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.table-header {
  @apply px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider;
}

.table-cell {
  @apply px-6 py-4 whitespace-nowrap text-sm;
}
</style>
