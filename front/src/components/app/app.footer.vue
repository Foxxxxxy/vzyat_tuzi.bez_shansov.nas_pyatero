<script setup>
import {
  IconHome,
  IconTeam,
  IconSearch,
  IconHistory,
  IconRequests,
  IconEquipment,
  IconBuilding,
  IconIndustry,
  IconDifferent,
  IconUsers
} from '~/components/icons';
import { computed, ref } from 'vue';
import { useStore } from '~/stores/stores.main';

const store = useStore();

const navs = [
  {
    name: 'Калькулятор',
    icon: IconHome,
    to: '/',
    level: 1,
    auth: false
  },
  {
    name: 'Отчет',
    icon: IconSearch,
    to: '/review',
    level: 1,
    auth: false
  },
  {
    name: 'История',
    icon: IconHistory,
    to: '/history',
    level: 1,
  },
  {
    name: 'Профиль',
    icon: IconTeam,
    to: '/profile',
    level: 1,
  },
  {
    name: 'Пользователи',
    icon: IconUsers,
    to: '/users',
    level: 3,
  },
  {
    name: 'Все запросы',
    icon: IconRequests,
    to: '/all-requests',
    level: 3,
  },
  {
    name: 'Оборудование',
    icon: IconEquipment,
    to: '/equipments',
    level: 3,
  },
  {
    name: 'Здания',
    icon: IconBuilding,
    to: '/buildings',
    level: 3,
  },
  {
    name: 'Отрасли',
    icon: IconIndustry,
    to: '/industry',
    level: 3,
  },
  {
    name: 'Услуги',
    icon: IconDifferent,
    to: '/additional',
    level: 3,
  },
];

const navs_admin = computed(() => {
  return navs.filter((item) => item.level <= 3);
});

const navs_user = computed(() => {
  return navs.filter((item) => item.level <= 1);
});

const user_level = computed(() => {
  return store.$state.user.level;
});

const notauth_user = computed(() => {
  return navs.filter((item) => item.auth === false);
});

const isAuth = computed(() => !!store.$state.user.token)

const return_navs = computed(() => {
  if (!isAuth.value) return notauth_user.value
  if (user_level.value === 3) {
    return navs_admin.value;
  } else {
    return navs_user.value;
  }
});

</script>

<template>
  <footer class="footer">
    <nav class="nav">
      <router-link
        :to="nav.to"
        v-for="(nav, idx) of return_navs"
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
