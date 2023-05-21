<script setup>
import { computed, onMounted, ref } from 'vue'
import { IconHome, IconTeam, IconSetup } from '~/components/icons'
import { useStore } from '~/stores/stores.main'

const store = useStore()

const navs = [
  {
    name: 'Калькулятор',
    icon: IconHome,
    to: '/',
    level: 1,
  },
  {
    name: 'Профиль',
    icon: IconTeam,
    to: '/profile',
    level: 1,
  },
  // {
  //   name: 'Редактирование справочников',
  //   icon: IconSetup,
  //   to: '/setup',
  //   level: 2,
  // },
  // {
  //   name: 'Список пользователей',
  //   icon: IconTeam,
  //   to: '/team',
  //   level: 3,
  // },
]

const navs_moderator = computed(() => {
  return navs.filter((item) => item.level <= 2)
})

const navs_user = computed(() => {
  return navs.filter((item) => item.level <= 1)
})

const user_level = computed(() => {
  return store.$state.level
})

const return_navs = computed(() => {
  if (user_level.value == 3) {
    return navs
  } else if (user_level.value == 2) {
    return navs_moderator.value
  } else {
    return navs_user.value
  }
})
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar__header">
      <h1 class="sidebar__title">Smetaverse</h1>
    </div>
    <nav class="nav">
      <div class="nav__item" v-for="(nav, idx) of return_navs" :key="idx">
        <router-link :to="nav.to" class="nav__link" router-link-active="active">
          <icon-wrapper class="nav__icon" width="20" height="20">
            <component :is="nav.icon" class="nav__icon" />
          </icon-wrapper>
          {{ nav.name }}
        </router-link>
      </div>
    </nav>
  </aside>
</template>

<style lang="scss" scoped>
.sidebar {
  height: 100%;
  width: 100%;
  background-color: $primary-white;
  box-shadow: 0px 10px 50px rgba(0, 0, 0, 0.05);
  &__header {
    margin-bottom: 100px;
    padding: 29px 0;
    border-bottom: 1px solid rgba(160, 160, 160, 0.4);
  }
  &__title {
    @include tg-h5-bold;
    text-align: center;
    color: $accent-purple;
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
</style>
