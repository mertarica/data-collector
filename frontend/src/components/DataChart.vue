<template>
  <div class="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-gray-200/50">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h3 class="text-lg font-semibold text-gray-900">Data Visualization</h3>
        <p class="text-sm text-gray-600">Time series chart showing {{ seriesCount }} data series</p>
      </div>

      <!-- View Toggle -->
      <div class="flex items-center space-x-2">
        <span class="text-sm font-medium text-gray-700">View:</span>
        <div class="relative inline-flex bg-gray-100 rounded-lg p-1">
          <button @click="viewMode = 'chart'" :class="viewButtonClass('chart')">Chart</button>
          <button @click="viewMode = 'table'" :class="viewButtonClass('table')">Table</button>
        </div>
      </div>
    </div>

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

      <div v-else class="h-96 bg-white rounded-lg border">
        <canvas ref="chartRef" class="w-full h-full"></canvas>
      </div>
    </div>

    <!-- Table View -->
    <div v-else class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="table-header">Date</th>
            <th class="table-header">Series</th>
            <th class="table-header">Value</th>
            <th class="table-header">Year</th>
            <th class="table-header">Period</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="row in displayTableData" :key="`${row.series}-${row.date}`">
            <td class="table-cell text-gray-900">{{ row.dateFormatted }}</td>
            <td class="table-cell text-gray-900">{{ row.seriesName }}</td>
            <td class="table-cell font-medium text-blue-600">{{ row.value }}</td>
            <td class="table-cell text-gray-500">{{ row.year }}</td>
            <td class="table-cell text-gray-500">{{ row.period }}</td>
          </tr>
        </tbody>
      </table>
      <div v-if="tableData.length > 100" class="p-4 text-center text-gray-500">
        Showing first 100 rows of {{ tableData.length }} total rows
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
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
const viewMode = ref<'chart' | 'table'>('chart')
let chartInstance: Chart | null = null
console.log(props.data);
// Computed properties
const sourceData = computed(() => {
  if (!props.data) return []

  if (props.dataType === 'raw' && props.data.raw_data) {
    return props.data.raw_data
  } else if (props.dataType === 'processed' && props.data.processed_data) {
    return props.data.processed_data
  }

  return []
})

const chartData = computed(() => {
  if (!sourceData.value.length) return []

  return sourceData.value
    .map((series: any, index: number) => {
      if (!series.Data?.length) return null

      const seriesData = series.Data.filter((point: any) => isValidDataPoint(point))
        .map((point: any) => ({
          x: parseDate(point.Fecha),
          y: parseFloat(point.Valor),
        }))
        .filter((point: any) => !isNaN(point.x.getTime()) && !isNaN(point.y))
        .sort((a: any, b: any) => a.x.getTime() - b.x.getTime())

      if (!seriesData.length) return null

      return {
        label: series.Nombre || series.COD || `Series ${index + 1}`,
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
  const rows: any[] = []
  sourceData.value.forEach((series: any) => {
    if (!series.Data?.length) return

    series.Data.forEach((point: any) => {
      if (isValidDataPoint(point)) {
        rows.push({
          date: point.Fecha,
          dateFormatted: formatDate(point.Fecha),
          series: series.COD || 'Unknown',
          seriesName: series.Nombre || series.COD || 'Unknown Series',
          value: point.Valor,
          year: point.Anyo,
          period: point.FK_Periodo,
        })
      }
    })
  })

  return rows.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
})

const hasData = computed(() => chartData.value.length > 0)
const seriesCount = computed(() => chartData.value.length)
const displayTableData = computed(() => tableData.value.slice(0, 100))

// Helper functions
function isValidDataPoint(point: any): boolean {
  return point.Fecha && point.Valor !== null && point.Valor !== undefined && !point.Secreto
}

function parseDate(dateStr: string): Date {
  if (typeof dateStr === 'string' && dateStr.startsWith('/Date(')) {
    const dateMatch = dateStr.match(/\/Date\((\d+)\)/)
    if (dateMatch) {
      const timestamp = parseInt(dateMatch[1])
      return new Date(timestamp)
    }
  }
  return new Date(dateStr)
}

function formatDate(dateStr: string): string {
  return parseDate(dateStr).toLocaleDateString('tr-TR')
}

function getColor(index: number, alpha: number = 1): string {
  const colors = [
    `rgba(59, 130, 246, ${alpha})`, // blue
    `rgba(16, 185, 129, ${alpha})`, // green
    `rgba(245, 101, 101, ${alpha})`, // red
    `rgba(139, 92, 246, ${alpha})`, // purple
    `rgba(245, 158, 11, ${alpha})`, // yellow
    `rgba(236, 72, 153, ${alpha})`, // pink
    `rgba(20, 184, 166, ${alpha})`, // teal
    `rgba(251, 113, 133, ${alpha})`, // rose
  ]
  return colors[index % colors.length]
}

function viewButtonClass(mode: string): string {
  const baseClass = 'px-3 py-1 text-sm font-medium rounded-md transition-all duration-200'
  const activeClass = 'bg-white text-blue-600 shadow-sm'
  const inactiveClass = 'text-gray-600 hover:text-gray-900'

  return `${baseClass} ${viewMode.value === mode ? activeClass : inactiveClass}`
}

// Chart creation
const createChart = async () => {
  if (!chartRef.value || !hasData.value) return

  await nextTick()

  const ctx = chartRef.value.getContext('2d')
  if (!ctx) return

  // Destroy existing chart
  if (chartInstance) {
    chartInstance.destroy()
  }

  const config: ChartConfiguration = {
    type: 'line',
    data: { datasets: chartData.value },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        title: {
          display: true,
          text: `${props.dataType === 'raw' ? 'Raw' : 'Processed'} Data Time Series`,
        },
        legend: {
          display: chartData.value.length > 1,
          position: 'top',
        },
        tooltip: {
          callbacks: {
            title: (context) => {
              return context[0].parsed.x
                ? new Date(context[0].parsed.x).toLocaleDateString('tr-TR')
                : ''
            },
            label: (context) => `${context.dataset.label}: ${context.parsed.y}`,
          },
        },
      },
      scales: {
        x: {
          type: 'time',
          time: {
            unit: 'quarter',
            displayFormats: { quarter: 'MMM yyyy' },
          },
          title: { display: true, text: 'Date' },
        },
        y: {
          title: { display: true, text: 'Value' },
        },
      },
    },
  }

  try {
    chartInstance = new Chart(ctx, config)
  } catch (error) {
    console.error('Error creating chart:', error)
  }
}

// Watchers
watch(
  [() => props.data, () => props.dataType],
  () => {
    if (viewMode.value === 'chart') {
      createChart()
    }
  },
  { deep: true },
)

watch(viewMode, (newMode) => {
  if (newMode === 'chart') {
    nextTick(() => createChart())
  }
})

// Lifecycle
onMounted(() => {
  if (hasData.value && viewMode.value === 'chart') {
    createChart()
  }
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
})
</script>

<style scoped>
.table-header {
  @apply px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider;
}

.table-cell {
  @apply px-6 py-4 whitespace-nowrap text-sm;
}
</style>
