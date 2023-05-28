<script setup>
import {
  CommonButton,
  CommonInput,
  CommonHelpinput,
  CommonPopup
} from '~/components/common';
import { get_user_info, edit_current_user } from '~/api/route.user';
import { computed, onMounted, ref } from 'vue';
import { useStore } from '~/stores/stores.main';
import { get_industry_suggestion, get_current_industry } from '~/api/route.industry';

const form = ref(null);
const store = useStore();

const isShowPopup = ref(false)

const token = computed(() => store.$state.user.token);

const save = async () => {
  const {
    email,
    name,
    last_name,
    organisation_name,
    fathers_name,
    inn,
    web_site,
    country,
    city,
    position,
  } = form.value;
  const res = await edit_current_user(
    form.value.id,
    {
      email,
      name,
      last_name,
      organisation_name,
      fathers_name,
      inn,
      web_site,
      country,
      city,
      position,
      industry_id: form.value.industry.chosen_id,
    },
    token.value
  );
  if (res.statue !== 'error') {
    isShowPopup.value = true
  }
};

const setSuggestions = (suggestion, key, index) => {
  if (index >= 0) {
    return (form.value[key][index].chosen_id = suggestion.id);
  }
  form.value[key].chosen_id = suggestion.id;
};

const getAllSuggestions = async () => {
  for (let key in form.value) {
    const block = form.value[key];
    if (block.input_type === 'suggestion' && block.type !== 'org_type') {
      block.suggestions = [...(await block.route(block.value, 0, 100))];
    }
  }
};

onMounted(async () => {
  const data = await get_user_info(token.value);
  form.value = {
    ...data,
    industry: {
      input_type: 'suggestion',
      type: 'industry',
      value: '',
      chosen_id: null,
      route: get_industry_suggestion,
      suggestions: [],
    },
  };

  await getAllSuggestions();
  const industry = await get_current_industry(form.value.industry_id)
  form.value.industry.value = industry.name
});
</script>

<template>
  <div class="profile" v-if="form">
    <common-popup
      :is-active="isShowPopup"
      class="popup"
      title="Вы успешно изменили информацию о себе!"
    >
      <common-button @click="isShowPopup = false" class="popup__button"> Закрыть </common-button>
    </common-popup>
    <div class="profile__content">
      <header class="profile__header">
        <h1 class="profile__title">Настройки пользователя</h1>
        <common-button @click="save" class="profile__button"
          >Сохранить</common-button
        >
      </header>
      <div class="profile__wrapper">
        <div class="profile__form">
          <div class="profile__block">
            <common-input
              v-model="form.last_name"
              :value="form.last_name"
              label="Фамилия"
              class="profile__input"
            />
          </div>
          <div class="profile__block">
            <common-input
              v-model="form.name"
              :value="form.name"
              label="Имя"
              class="profile__input"
            />
          </div>
          <div class="profile__block">
            <common-input
              v-model="form.fathers_name"
              :value="form.fathers_name"
              label="Отчество"
              class="profile__input"
            />
          </div>
          <div class="profile__block">
            <common-input
              v-model="form.email"
              :value="form.email"
              label="E-mail"
              class="profile__input"
            />
          </div>
          <div class="profile__block">
            <common-input
              v-model="form.organisation_name"
              :value="form.organisation_name"
              label="Наименование организации"
              class="profile__input"
            />
          </div>
        </div>
        <div class="profile__form">
          <div class="profile__block">
            <common-input
              v-model="form.inn"
              :value="form.inn"
              label="ИНН"
              class="profile__input"
            />
          </div>
          <div class="profile__block">
            <common-input
              v-model="form.web_site"
              :value="form.web_site"
              label="Веб-сайт организации"
              class="profile__input"
            />
          </div>
          <div class="profile__block">
            <common-helpinput
              v-model="form.industry.value"
              class="profile__input"
              label="Отрасль ведения хозяйственной деятельности"
              :value="form.industry.value"
              :suggestions="form.industry.suggestions"
              @input="updateSuggestion('industry')"
              @set-item="(item) => setSuggestions(item, 'industry')"
            />
          </div>

          <div class="profile__block">
            <common-input
              v-model="form.country"
              :value="form.country"
              label="Страна"
              class="profile__input"
            />
          </div>
          <div class="profile__block">
            <common-input
              v-model="form.city"
              :value="form.city"
              label="Город"
              class="profile__input"
            />
          </div>
          <div class="profile__block">
            <common-input
              v-model="form.position"
              :value="form.position"
              label="Должность"
              class="profile__input"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">

.popup {
  z-index: 1000;
  &__button {
    width: 100%;
  }
}
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
      padding-bottom: 100px;
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
    @include lg {
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
