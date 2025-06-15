<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="text-center">
      <div class="text-9xl mb-8">🔍</div>
      <h1 class="text-6xl font-bold text-gray-900 mb-4">404</h1>
      <p class="text-xl text-gray-600 mb-8">Oops! The page you're looking for doesn't exist.</p>
      <div class="space-x-4">
        <router-link to="/" class="btn-primary"> 🏠 Go Home </router-link>
        <button @click="router.back()" class="btn-secondary">← Go Back</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>
