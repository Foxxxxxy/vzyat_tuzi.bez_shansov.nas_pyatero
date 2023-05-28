<script setup>
import { computed, ref } from 'vue';
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
import { useStore } from '~/stores/stores.main';
import { CommonHamburger } from '~/components/common';

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
    name: 'Просмотр отчета',
    icon: IconSearch,
    to: '/review',
    level: 1,
    auth: false
  },
  {
    name: 'Профиль',
    icon: IconTeam,
    to: '/profile',
    level: 1,
  },
  {
    name: 'Список пользователей',
    icon: IconUsers,
    to: '/users',
    level: 3,
  },
  {
    name: 'История',
    icon: IconHistory,
    to: '/history',
    level: 1,
  },
  {
    name: 'Все запросы',
    icon: IconRequests,
    to: '/all-requests',
    level: 3,
  },
  {
    name: 'Список оборудования',
    icon: IconEquipment,
    to: '/equipments',
    level: 3,
  },
  {
    name: 'Список зданий',
    icon: IconBuilding,
    to: '/buildings',
    level: 3,
  },
  {
    name: 'Список отраслей',
    icon: IconIndustry,
    to: '/industry',
    level: 3,
  },
  {
    name: 'Разное',
    icon: IconDifferent,
    to: '/additional',
    level: 3,
  },
];

const isShowedSidebar = ref(false);
const activateBurger = ref(false);

const openSidebar = () => {
  isShowedSidebar.value = !isShowedSidebar.value;
  activateBurger.value = !activateBurger.value;
};

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
  <aside class="sidebar" :class="{ active: isShowedSidebar }">
    <div class="sidebar__wrapper">
      <div class="sidebar__header">
        <h1 class="sidebar__title">Smetaverse</h1>
        <common-hamburger
          @click="openSidebar"
          :isActive="activateBurger"
          class="sidebar__burger"
          width="20"
          height="18"
          background="#905cff"
        />
      </div>
      <nav class="nav">
        <div class="nav__item" v-for="(nav, idx) of return_navs" :key="idx">
          <router-link :to="nav.to" class="nav__link">
            <icon-wrapper class="nav__icon" width="20" height="20">
              <component :is="nav.icon" class="nav__icon" />
            </icon-wrapper>
            {{ nav.name }}
          </router-link>
        </div>
      </nav>
    </div>
  </aside>
</template>

<style lang="scss" scoped>
.bg {
  position: absolute;
  right: -100%;
  width: 100%;
  height: 100%;
  background-color: #f6f6f8;
  z-index: -1;
  opacity: 1;
  pointer-events: none;
  touch-action: none;
  transition: opacity 0.3s ease;
  &.active {
    z-index: 1000;
    opacity: 1;
  }
}
.sidebar {
  position: relative;
  height: 100%;
  width: calc(150px + 10vw);
  background-color: $primary-white;
  box-shadow: 0px 10px 50px rgba(0, 0, 0, 0.05);
  transition: width 0.3s ease;
  @include lg {
    border-right: 1px solid #f6f6f8;
  }
  @include lg {
    width: 55px;
    &.active {
      width: 300px;
    }
  }
  @include md {
    width: 0;
  }
  &__wrapper {
    overflow: hidden;
    overflow-y: scroll;
    max-height: 100vh;
  }
  &__burger {
    display: none;
    @include lg {
      display: flex;
      margin: 0 17px;
    }
  }
  &__header {
    margin-bottom: 100px;
    padding: 29px 0;
    border-bottom: 1px solid rgba(160, 160, 160, 0.4);
    min-height: 94px;
    display: flex;
    align-items: center;
    justify-content: center;
    @include lg {
      justify-content: flex-start;
    }
  }
  &__title {
    @include tg-h5-bold;
    text-align: center;
    color: $accent-purple;
    @include lg {
      display: none;
    }
  }
}

.nav {
  &__link {
    display: flex;
    align-items: center;
    height: 72px;
    white-space: nowrap;
    color: $primary-grey;
    transition: all ease 0.2s;
    padding: 0 16px;
    &.active {
      background: linear-gradient(
        89.95deg,
        #ece2ff 0.04%,
        rgba(240, 252, 247, 0) 120.25%
      );
      color: $accent-purple;
      border-left: 3px solid $accent-purple;
    }
    border-left: 3px solid transparent;
    &:hover {
      background: linear-gradient(
        89.95deg,
        #ece2ff 0.04%,
        rgba(240, 252, 247, 0) 120.25%
      );
      color: $accent-purple;
      border-left: 3px solid $accent-purple;
    }
  }
  &__icon {
    margin-right: 16px;
  }
  &__item {
    cursor: pointer;
    @include tg-h6-medium;
    text-align: center;
  }
}

.router-link-exact-active {
  background: linear-gradient(
    89.95deg,
    #ece2ff 0.04%,
    rgba(240, 252, 247, 0) 120.25%
  );
  color: $accent-purple;
  border-left: 3px solid $accent-purple;
}
</style>
