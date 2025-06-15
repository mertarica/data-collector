<template>
  <button
    @click="handleClick"
    class="inline-flex items-center px-4 py-2 bg-white/80 backdrop-blur-sm hover:bg-white text-gray-700 hover:text-gray-900 border border-gray-200 hover:border-gray-300 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 w-fit"
  >
    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M10 19l-7-7m0 0l7-7m-7 7h18"
      ></path>
    </svg>
    {{ text }}
  </button>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

withDefaults(
  defineProps<{
    text?: string
    to?: string
  }>(),
  {
    text: 'Back',
  },
)

const router = useRouter()

const handleClick = () => {
  const props = defineProps<{
    text?: string
    to?: string
  }>()

  if (props.to) {
    router.push(props.to)
  } else {
    router.back()
  }
}
</script>
