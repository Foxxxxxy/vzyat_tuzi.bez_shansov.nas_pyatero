<script setup>
defineProps({
  title: String,
  desc: String,
  isActive: Boolean
})
</script>

<template>
  <div class="popup" :class="{ hidden: !isActive }">
    <div class="popup__content">
      <h2 class="popup__title">{{ title }}</h2>
      <p class="popup__desc">{{ desc }}</p>
      <div class="popup__bottom">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.popup {
  opacity: 1;
  transition: opacity 0.3s ease;
  position: fixed;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  &.hidden {
    opacity: 0;
    pointer-events: none;
    touch-action: none;
  }
  &__content {
    text-align: center;
    padding: 24px;
    background-color: $primary-white;
    border-radius: 5px;
    max-width: 328px;
    margin: 0 auto;
  }
  &__title {
    @include create-font(20px, 600, 28px);
    margin-bottom: 20px;
  }
  &__desc {
    @include create-font(16px, 400, 25px);
    color: #8C9AAB;
    margin-bottom: 8px;
  }
  &__bottom {
    padding: 16px 0;
    display: flex;
    justify-content: center;
  }
  &__button {
    width: 100%;
    &:not(:last-child) {
      margin-right: 8px;
    }
  }
}
</style>
