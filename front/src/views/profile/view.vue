<script setup>
import { CommonPopup, CommonButton, CommonInput } from '~/components/common';
</script>

<template>
  <div class="profile">
    <div class="profile__content">
      <header class="profile__header">
        <h1 class="profile__title">Настройки пользователя</h1>
        <common-button class="profile__button">Сохранить</common-button>
      </header>
      <div class="profile__wrapper">
        <div class="profile__form">
          <div class="profile__block">
            <common-input label="Фамилия" class="profile__input" />
          </div>
          <div class="profile__block">
            <common-input label="Имя" class="profile__input" />
          </div>
          <div class="profile__block">
            <common-input label="Отчество" class="profile__input" />
          </div>
          <div class="profile__block">
            <common-input label="E-mail" class="profile__input" />
          </div>
          <div class="profile__block">
            <common-input
              label="Наименование организации"
              class="profile__input"
            />
          </div>
        </div>
        <div class="profile__form">
          <div class="profile__block">
            <common-input label="ИНН" class="profile__input" />
          </div>
          <div class="profile__block">
            <common-input label="Веб-сайт организации" class="profile__input" />
          </div>
          <div class="profile__block">
            <common-input
              label="Отрасль ведения хозяйственной деятельности"
              class="profile__input"
            />
          </div>

          <div class="profile__block">
            <common-input label="Страна" class="profile__input" />
          </div>
          <div class="profile__block">
            <common-input label="Город" class="profile__input" />
          </div>
          <div class="profile__block">
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
  }
  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 41px 32px 41px 0;
  }
  &__form {
    padding: 0 32px;
    max-width: 500px;
  }
  &__block {
    &:not(:last-child) {
      margin-bottom: 12px;
    }
  }
  &__title {
    position: relative;
    @include create-font(26px, 600, 23px);
    padding-left: 32px;
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
