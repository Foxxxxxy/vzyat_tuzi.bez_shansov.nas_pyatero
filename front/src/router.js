import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '~/views/home'
import AuthView from '~/views/auth'

export default createRouter({
  history: createWebHistory(),
  routes: [...HomeView, ...AuthView],
})
