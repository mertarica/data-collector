<template>
  <div id="app" class="min-h-screen">
    <!-- Modern Header -->
    <header
      class="bg-white/80 backdrop-blur-md shadow-sm border-b border-gray-200/50 sticky top-0 z-50"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <RouterLink to="/" class="flex items-center space-x-3 group">
            <div
              class="w-10 h-10 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center group-hover:scale-105 transition-transform duration-200"
            >
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                ></path>
              </svg>
            </div>
            <div class="hidden sm:block">
              <span
                class="font-bold text-xl bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent"
                >Data Collector</span
              >
              <div class="text-xs text-gray-500 font-medium">INE Data Explorer</div>
            </div>
          </RouterLink>

          <!-- Navigation Menu (for future expansion) -->
          <nav class="hidden md:flex items-center space-x-8">
            <RouterLink
              to="/"
              class="text-gray-600 hover:text-gray-900 font-medium transition-colors duration-200"
            >
              Datasets
            </RouterLink>
          </nav>

          <!-- Mobile menu button (for future) -->
          <div class="md:hidden">
            <button class="text-gray-600 hover:text-gray-900 transition-colors duration-200">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 6h16M4 12h16M4 18h16"
                ></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main>
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="bg-gray-50 border-t border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="text-center text-gray-600">
          <p class="text-sm">
            Data provided by
            <a
              href="https://www.ine.es"
              target="_blank"
              class="text-blue-600 hover:text-blue-700 font-medium"
            >
              Spanish National Statistics Institute (INE)
            </a>
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>
