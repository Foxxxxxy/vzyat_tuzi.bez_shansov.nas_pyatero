<script setup>
import { IconHome, IconTeam, IconSetup } from '~/components/icons';

const navs = [
  {
    name: 'Калькулятор',
    icon: IconHome,
    to: '/',
    level: 1,
  },
  {
    name: 'Отчет',
    icon: IconHome,
    to: '/review',
    level: 1,
  },
  {
    name: 'Профиль',
    icon: IconTeam,
    to: '/profile',
    level: 1,
  },
  {
    name: 'Оборудование',
    icon: IconTeam,
    to: '/equipments',
    level: 1,
  },
  {
    name: 'Здания',
    icon: IconTeam,
    to: '/buildings',
    level: 1,
  },
  {
    name: 'Отрасли',
    icon: IconTeam,
    to: '/industry',
    level: 1,
  },
  {
    name: 'Разное',
    icon: IconTeam,
    to: '/additional',
    level: 1,
  },
  {
    name: 'Пользователи',
    icon: IconTeam,
    to: '/users',
    level: 1,
  },
];
</script>

<template>
  <footer class="footer">
    <nav class="nav">
      <router-link
        :to="nav.to"
        v-for="(nav, idx) of navs"
        :key="idx"
        class="nav__link"
      >
        <icon-wrapper class="nav__icon" width="20" height="20">
          <component :is="nav.icon" class="nav__icon" />
        </icon-wrapper>
        {{ nav.name }}
      </router-link>
    </nav>
  </footer>
</template>

<style lang="scss" scoped>
.footer {
  width: 100%;
  background-color: $primary-white;
  border-radius: 5px;
  padding-bottom: 8px;
}

.nav {
  display: flex;
  justify-content: space-between;
  &__icon {
    margin-bottom: 5px;
  }
  &__link {
    @include create-font(12px, 600, 14px);
    display: flex;
    justify-content: baseline;
    color: #c1c7d2;
    flex-direction: column;
    align-items: center;
    width: 100px;
    padding: 10px 30px;
    text-align: center;
    border-radius: 15px 15px 0 0;
  }
}

.router-link-exact-active {
  background: linear-gradient(
    177.1deg,
    #bebcfe -18.09%,
    rgba(240, 252, 247, 0) 97.59%
  );
  color: $accent-purple;
}
</style>
