<script setup>
import { CommonPopup, CommonButton, CommonInput } from '~/components/common';
import { reactive, ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { get_token, register } from '~/api/route.auth.js';
import { useStore } from '~/stores/stores.main';

const router = useRouter();
const route = useRoute();
const store = useStore();

const form = reactive({
  email: '',
  password: '',
});

const registrationForm = reactive({
  name: '',
  surname: '',
  last_name: '',
  email: '',
  organisation_name: '',
  inn: '',
  web_site: '',
  type_of_work: '',
  country: '',
  city: '',
  work_position: '',
  level: 1,
  password: '',
});

const isShowPopup = ref(false);

const step = ref('login');

const registrationStep = ref(1);

const isValidStep = ref(false);

const createCache = (user) => {
  localStorage.setItem('user', JSON.stringify(user));
};

const setUserStore = (email, password, level, user_id, token) => {
  store.$state.user.email = email;
  store.$state.user.password = password;
  store.$state.user.level = level;
  store.$state.user.user_id = user_id;
  store.$state.user.token = token;
};

const login = async () => {
  const { access_token, level, user_id } = await get_token(
    form.email,
    form.password
  );

  setUserStore(form.email, form.password, level, user_id, access_token);
  createCache(store.$state.user);
  if (route.query.back) {
      router.push('/' + route.query.back);
    } else {
      router.push('/');
    }
};

const signup = async () => {
  //TODO ДОБАВИТЬ ПРОВЕРКУ ПО СТАТУСУ ЗАПРОСА
  const res = await register({ ...registrationForm });

  if (!res.detail) {
    const { access_token, level, user_id } = await get_token(
      res.email,
      registrationForm.password
    );

    setUserStore(form.email, form.password, level, user_id, access_token);
    createCache(store.$state.user);
    if (route.query.back) {
      router.push('/' + route.query.back);
    } else {
      router.push('/');
    }
  }
};

const validateEmail = (email) => {
  return String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
};

const next = () => {
  registrationStep.value += 1;
  isValidStep.value = validate(registrationStep.value);
};

const back = () => {
  registrationStep.value -= 1;
  isValidStep.value = validate(registrationStep.value);
};

const validate = (step) => {
  if (step === 1 && !registrationForm.name.length) {
    return false;
  }
  if (step === 2 && !registrationForm.inn.length) {
    return false;
  }
  if (
    step === 4 &&
    (!registrationForm.email.length ||
      registrationForm.password.length < 8 ||
      !validateEmail(registrationForm.email))
  ) {
    return false;
  }
  return true;
};

watch(registrationForm, () => {
  isValidStep.value = validate(registrationStep.value);
});

const updateCache = () => {
  localStorage.setItem('popup_shown', 'true');
};

const handlePopup = (isAgree) => {
  if (!isAgree) {
    router.push('/');
  } else {
    isShowPopup.value = false;
    step.value = 'registration';
    router.push({ path: 'auth', query: { step: 'registration' } });
  }
  updateCache();
};

onMounted(() => {
  const isShownPopup = localStorage.getItem('popup_shown');
  if (!isShownPopup) {
    isShowPopup.value = true;
  }
  if (route.query.step === 'registration') {
    step.value = 'registration';
  }
});
</script>

<template>
  <div class="auth">
    <common-popup
      :is-active="isShowPopup"
      class="popup"
      title="Здравствуйте!"
      desc="Вы впервые пользуетесь нашим сервисом, хотите пройти регистрацию?"
    >
      <common-button
        @click="() => handlePopup(false)"
        class="popup__button"
        variant="outlined"
      >
        Нет
      </common-button>
      <common-button @click="() => handlePopup(true)" class="popup__button">
        Да
      </common-button>
    </common-popup>
    <div class="auth-modal" v-if="step === 'login'">
      <h1 class="auth-modal__title">Добро пожаловать в систему!</h1>
      <p class="auth-modal__desc">Авторизуйтесь, чтобы начать</p>
      <div class="auth-modal__form">
        <div class="auth-modal__block">
          <common-input
            v-model="form.email"
            :value="form.email"
            class="auth-modal__input"
            label="E-mail"
          />
        </div>
        <div class="auth-modal__block">
          <common-input
            v-model="form.password"
            :value="form.password"
            class="auth-modal__input"
            label="Пароль"
          />
        </div>
      </div>
      <div class="auth-modal__bottom">
        <common-button @click="login" class="auth-modal__button">
          Войти
        </common-button>
        <p class="auth-modal__hint">
          Если вы еще не зарегистрированы в нашем сервисе нажмите на кнопку
          "Регистрация" ниже
        </p>
        <common-button
          @click="() => (step = 'registration')"
          class="auth-modal__button"
          variant="outlined"
        >
          Регистрация
        </common-button>
        <common-button
          @click="router.push('/')"
          class="auth-modal__button"
          variant="outlined"
        >
          Вернуться на главную
        </common-button>
      </div>
    </div>
    <div class="auth-modal" v-else>
      <p class="auth-modal__steps">{{ registrationStep }}/4 шаг</p>
      <h1 class="auth-modal__title">Добро пожаловать в систему!</h1>
      <p class="auth-modal__desc">Пройдите регистрацию, чтобы начать</p>
      <div class="auth-modal__form">
        <div class="auth-modal__step" v-show="registrationStep === 1">
          <div class="auth-modal__block">
            <common-input
              v-model="registrationForm.surname"
              :value="registrationForm.surname"
              class="auth-modal__input"
              label="Фамилия"
            />
          </div>
          <div class="auth-modal__block">
            <common-input
              v-model="registrationForm.name"
              :value="registrationForm.name"
              :required="true"
              class="auth-modal__input"
              label="Имя"
            />
          </div>
          <div class="auth-modal__block">
            <common-input
              v-model="registrationForm.last_name"
              :value="registrationForm.last_name"
              class="auth-modal__input"
              label="Отчество"
            />
          </div>
        </div>
        <div class="auth-modal__step" v-show="registrationStep === 2">
          <div class="auth-modal__block">
            <common-input
              v-model="registrationForm.organisation_name"
              :value="registrationForm.organisation_name"
              class="auth-modal__input"
              label="Наименование организации"
            />
          </div>
          <div class="auth-modal__block">
            <common-input
              v-model="registrationForm.inn"
              :value="registrationForm.inn"
              class="auth-modal__input"
              :required="true"
              label="ИНН"
            />
          </div>
          <div class="auth-modal__block">
            <common-input
              v-model="registrationForm.web_site"
              :value="registrationForm.web_site"
              class="auth-modal__input"
              label="Веб-сайт организации"
            />
          </div>
          <div class="auth-modal__block">
            <common-input
              v-model="registrationForm.type_of_work"
              :value="registrationForm.type_of_work"
              class="auth-modal__input"
              label="Отрасль ведения хозяйственной деятельности"
            />
          </div>
        </div>
        <div class="auth-modal__step" v-show="registrationStep === 3">
          <div class="auth-modal__block">
            <common-input
              v-model="registrationForm.country"
              :value="registrationForm.country"
              class="auth-modal__input"
              label="Страна"
            />
          </div>
          <div class="auth-modal__block">
            <common-input
              v-model="registrationForm.city"
              :value="registrationForm.city"
              class="auth-modal__input"
              label="Город"
            />
          </div>
          <div class="auth-modal__block">
            <common-input
              v-model="registrationForm.work_position"
              :value="registrationForm.work_position"
              class="auth-modal__input"
              label="Должность"
            />
          </div>
        </div>
        <div class="auth-modal__step" v-show="registrationStep === 4">
          <div class="auth-modal__block">
            <common-input
              v-model="registrationForm.email"
              :value="registrationForm.email"
              :required="true"
              class="auth-modal__input"
              label="E-mail"
            />
          </div>
          <div class="auth-modal__block">
            <common-input
              v-model="registrationForm.password"
              :value="registrationForm.password"
              :required="true"
              class="auth-modal__input"
              label="Пароль"
            />
            <p class="auth-modal__block-hint">Минимально 8 символов</p>
          </div>
        </div>
      </div>
      <div class="auth-modal__bottom">
        <common-button
          v-if="registrationStep !== 4"
          @click="next"
          :disabled="!isValidStep"
          class="auth-modal__button"
        >
          Далее
        </common-button>
        <common-button
          v-if="registrationStep === 4"
          @click="signup"
          :disabled="!isValidStep"
          class="auth-modal__button"
        >
          Зарегистрироваться
        </common-button>
        <common-button
          variant="outlined"
          v-if="registrationStep !== 1"
          @click="back"
          class="auth-modal__button"
        >
          Назад
        </common-button>
        <p class="auth-modal__hint">
          Если вы уже зарегистрированы в нашем сервисе нажмите на кнопку "Войти"
          ниже
        </p>
        <common-button
          @click="step = 'login'"
          class="auth-modal__button"
          variant="outlined"
        >
          Войти
        </common-button>

        <common-button
          @click="router.push('/')"
          class="auth-modal__button"
          variant="outlined"
        >
          Вернуться на главную
        </common-button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.popup {
  z-index: 100;
  &__button {
    width: 100%;
    &:not(:last-child) {
      margin-right: 8px;
    }
  }
}

.auth {
  background-color: $primary-grey;
  min-height: 100vh;
  background-color: #f5f6f8;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  @include md {
    padding: 0;
  }
  &-modal {
    max-width: 550px;
    width: 100%;
    margin: 0 auto;
    background-color: $primary-white;
    padding: 72px 100px;
    border-radius: 5px;
    text-align: center;
    position: relative;
    @include md {
      padding: 50px 24px;
    }
    &__steps {
      @include create-font(20px, 600, 22px);
      color: $accent-purple;
      position: absolute;
      top: 20px;
      right: 20px;
    }
    &__button {
      width: 100%;
      &:not(:last-child) {
        margin-bottom: 24px;
      }
      @include md {
        &:hover {
          opacity: 1;
        }
      }
    }
    &__form {
      margin-bottom: 24px;
    }
    &__block {
      &:not(:last-child) {
        margin-bottom: 12px;
      }
      &-hint {
        @include create-font(14px, 400, 22px);
        margin-top: 6px;
      }
    }
    &__input {
      width: 100%;
    }
    &__title {
      @include create-font(26px, 600, 30px);
      margin-bottom: 30px;
    }
    &__desc {
      @include create-font(16px, 400, 22px);
      margin-bottom: 24px;
    }
    &__hint {
      @include create-font(16px, 400, 22px);
      color: $primary-grey;
      margin-bottom: 24px;
    }
  }
}
</style>
