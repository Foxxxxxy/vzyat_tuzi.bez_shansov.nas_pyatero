<script setup>
import { IconLogout } from '~/components/icons'

import { useStore } from '~/stores/stores.main'

import { useRouter } from 'vue-router'
import { computed } from 'vue'

const store = useStore()
const router = useRouter()

const logout = () => {
  store.$state.user.token = null
  store.$state.user.email = null
  store.$state.user.level = null
  store.$state.user.user_id = null
  store.$state.user.password = null

  localStorage.removeItem('user')

  router.push('/auth')
}

const name = computed(() => store.$state.user.email)
</script>

<template>
  <header class="header">
    <h1 class="header__title">Сервис для обработки смет</h1>
    <div class="user">
      <h3 class="user__name">{{ name }}</h3>
      <div @click="logout" class="user__logout">
        <icon-wrapper width="30" height="30">
          <icon-logout />
        </icon-wrapper>
      </div>
    </div>
  </header>
</template>

<style lang="scss" scoped>
.header {
  width: 100%;
  background-color: $primary-white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  &__title {
    margin-left: 50px;
    @include tg-18-normal;
  }
}
.user {
  display: flex;
  align-items: center;
  &__name {
    @include tg-14-medium;
    margin-right: 32px;
  }
  &__logout {
    cursor: pointer;
    padding: 32px 20px;
    background-color: $accent-purple;
  }
}
</style>
