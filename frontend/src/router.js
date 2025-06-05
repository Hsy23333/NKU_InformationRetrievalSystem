
import { createRouter, createWebHistory } from 'vue-router'
import Home from './components/HomePage.vue'
import SearchPage from './components/SearchPage.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/search', name: 'Search', component: SearchPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
