import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '~/views/home';
import AuthView from '~/views/auth';
import ProfileView from '~/views/profile';
import ReviewView from '~/views/review';
import EquipmentsView from '~/views/equipments';
import BuildingsView from '~/views/buildings';
import IndustryView from '~/views/industry';
import AdditionalView from '~/views/additional';
import UsersView from '~/views/users';

export default createRouter({
  history: createWebHistory(),
  routes: [
    ...HomeView,
    ...AuthView,
    ...ProfileView,
    ...ReviewView,
    ...EquipmentsView,
    ...BuildingsView,
    ...IndustryView,
    ...AdditionalView,
    ...UsersView
  ],
});
