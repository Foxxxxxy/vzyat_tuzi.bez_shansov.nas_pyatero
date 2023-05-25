import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '~/views/home';
import AuthView from '~/views/auth';
import ProfileView from '~/views/profile';
import ReviewView from '~/views/review';
import EquipmentsView from '~/views/equipments';

export default createRouter({
  history: createWebHistory(),
  routes: [
    ...HomeView,
    ...AuthView,
    ...ProfileView,
    ...ReviewView,
    ...EquipmentsView,
  ],
});
