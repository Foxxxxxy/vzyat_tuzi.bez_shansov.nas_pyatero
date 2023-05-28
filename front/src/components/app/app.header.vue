<script setup>
import { IconLogout, IconEconomics } from '~/components/icons';
import { CommonButton } from '~/components/common';
import { useStore } from '~/stores/stores.main';
import { get_user_info } from '~/api/route.user';
import { get_token } from '~/api/route.auth';

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
  const user = localStorage.getItem('user')
    ? JSON.parse(localStorage.getItem('user'))
    : null;
  if (!user) return;
  const tokenData = await get_token(user.email, user.password);
  if (tokenData.status !== 'error' && user) {
    store.$state.user.email = user.email;
    store.$state.user.password = user.password;
    store.$state.user.level = user.level;
    store.$state.user.user_id = user.user_id;
    store.$state.user.token = user.token;
  } else {
    localStorage.removeItem('user');
  }
  const data = await get_user_info(store.$state.user.token);
  if (data.status !== 'error') {
    store.$state.user.name = data.name;
  }
});
</script>

<template>
  <header class="header">
    <h1 class="header__title">
      По заказу
      <p class="header__title-mod">
        <icon-wrapper class="header__icon">
          <icon-economics />
        </icon-wrapper>
        Экономика москвы
      </p>
    </h1>
    <h1 class="header__title header__title--md">Smetaverse</h1>
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
  height: 95px;
  @include md {
    height: 50px;
  }
  &__icon {
    margin-right: 5px;
  }
  &__title {
    margin-left: 50px;
    @include tg-18-normal;
    display: flex;
    @include md {
      display: none;
    }
    &-mod {
      color: red;
      display: flex;
      align-items: center;
      margin-left: 5px;
      font-size: 14px
    }
    &--md {
      display: none;
      @include md {
        display: block;
        @include tg-h5-bold;
        text-align: center;
        color: $accent-purple;
      }
    }
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
