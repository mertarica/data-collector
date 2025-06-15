import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        title: 'Datasets',
      },
    },
    {
      path: '/dataset/:code',
      name: 'dataset-detail',
      component: () => import('../views/DatasetDetailView.vue'),
      meta: {
        title: 'Dataset Detail',
      },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
      meta: {
        title: '404 - Page Not Found',
      },
    },
  ],
})

// Update page title
router.beforeEach((to) => {
  document.title = `${to.meta.title} - Augusta Data Collector`
})

export default router
