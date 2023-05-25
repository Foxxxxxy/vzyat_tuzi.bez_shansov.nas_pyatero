<script setup>
import { IconLogout } from '~/components/icons';
import { CommonButton } from '~/components/common';
import { useStore } from '~/stores/stores.main';
import { get_user_info } from '~/api/route.user';

import { useRouter } from 'vue-router';
import { computed, onMounted } from 'vue';

const store = useStore();
const router = useRouter();

const logout = () => {
  store.$state.user.token = null;
  store.$state.user.email = null;
  store.$state.user.level = null;
  store.$state.user.user_id = null;
  store.$state.user.password = null;
  store.$state.user.name = null;

  localStorage.removeItem('user');
};

const name = computed(() => store.$state.user.name);

onMounted(async () => {
  if (store.$state.user.token) {
    const { name } = await get_user_info(store.$state.user.token)
    store.$state.user.name = name;
  }
})
</script>

<template>
  <header class="header">
    <h1 class="header__title">Сервис для обработки смет</h1>
    <div class="user" v-if="name">
      <h3 class="user__name">{{ name }}</h3>
      <div @click="logout" class="user__logout">
        <icon-wrapper width="30" height="30">
          <icon-logout />
        </icon-wrapper>
      </div>
    </div>
    <router-link to="/auth" v-else>
      <common-button class="header__button">Войти</common-button>
    </router-link>
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
  &__button {
    padding: 37px 50px;
    border-radius: 0;
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
