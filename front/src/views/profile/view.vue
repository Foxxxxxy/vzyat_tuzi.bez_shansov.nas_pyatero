<script setup>
import { CommonButton, CommonInput } from '~/components/common';
import { get_user_info, edit_current_user } from '~/api/route.user';
import { computed, onMounted, ref } from 'vue';
import { useStore } from '~/stores/stores.main';

const form = ref(null);
const store = useStore();

const token = computed(() => store.$state.user.token);

const save = async () => {
  const { email, name, last_name, organisation_name, inn, web_site } =
    form.value;
  await edit_current_user(
    form.value.id,
    {
      email,
      name,
      last_name,
      organisation_name,
      inn,
      web_site,
    },
    token.value
  );
};

onMounted(async () => {
  const data = await get_user_info(token.value);
  form.value = { ...data };
});
</script>

<template>
  <div class="profile" v-if="form">
    <div class="profile__content">
      <header class="profile__header">
        <h1 class="profile__title">Настройки пользователя</h1>
        <common-button @click="save" class="profile__button"
          >Сохранить</common-button
        >
      </header>
      <div class="profile__wrapper">
        <div class="profile__form">
          <div class="profile__block" v-if="form.last_name">
            <common-input
              v-model="form.last_name"
              :value="form.last_name"
              label="Фамилия"
              class="profile__input"
            />
          </div>
          <div class="profile__block" v-if="form.name">
            <common-input
              v-model="form.name"
              :value="form.name"
              label="Имя"
              class="profile__input"
            />
          </div>
          <div class="profile__block" v-if="form.p">
            <common-input label="Отчество" class="profile__input" />
          </div>
          <div class="profile__block" v-if="form.email">
            <common-input
              v-model="form.email"
              :value="form.email"
              label="E-mail"
              class="profile__input"
            />
          </div>
          <div class="profile__block" v-if="form.organisation_name">
            <common-input
              v-model="form.organisation_name"
              :value="form.organisation_name"
              label="Наименование организации"
              class="profile__input"
            />
          </div>
        </div>
        <div class="profile__form">
          <div class="profile__block" v-if="form.inn">
            <common-input
              v-model="form.inn"
              :value="form.inn"
              label="ИНН"
              class="profile__input"
            />
          </div>
          <div class="profile__block" v-if="form.web_site">
            <common-input
              v-model="form.web_site"
              :value="form.web_site"
              label="Веб-сайт организации"
              class="profile__input"
            />
          </div>
          <div class="profile__block" v-if="form.industry">
            <common-input
              v-model="form.industry"
              :value="form.industry"
              label="Отрасль ведения хозяйственной деятельности"
              class="profile__input"
            />
          </div>

          <div class="profile__block" v-if="form.country">
            <common-input label="Страна" class="profile__input" />
          </div>
          <div class="profile__block" v-if="form.city">
            <common-input label="Город" class="profile__input" />
          </div>
          <div class="profile__block" v-if="form.work">
            <common-input label="Должность" class="profile__input" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.profile {
  width: 100%;
  height: 100%;
  background-color: #ffffff;
  &__content {
    background-color: #ffffff;
  }
  &__wrapper {
    display: grid;
    grid-template-columns: 1fr 1fr;
    @include lg {
      grid-template-columns: 1fr;
    }
  }
  &__button {
    @include md {
      margin-left: 10px;
    }
  }
  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 41px 32px 41px 0;
    @include md {
      flex-direction: column;
      align-items: flex-start;
    }
  }
  &__form {
    padding: 0 32px;
    max-width: 500px;
    @include md {
      padding: 0 10px;
      margin-bottom: 20px;
    }
  }
  &__block {
    &:not(:last-child) {
      margin-bottom: 12px;
    }
  }
  &__title {
    position: relative;
    @include create-font(26px, 600, 26px);
    padding-left: 32px;
    @include md {
      margin-bottom: 30px;
    }
    &::before {
      content: '';
      height: calc(100% + 10px);
      position: absolute;
      top: -5px;
      width: 4px;
      border-radius: 4px;
      background-color: $accent-purple;
      left: 0;
    }
  }
}
</style>
