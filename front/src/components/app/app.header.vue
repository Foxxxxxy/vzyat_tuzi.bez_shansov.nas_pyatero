<script setup></script>

<template>
  <header class="header">
    <h1 class="header__title">ООО Название</h1>
  </header>
</template>

<style lang="scss" scoped>
.header {
  padding: 32px 0;
  width: 100%;
  background-color: $primary-white;
  &__title {
    margin-left: 50px;
    @include tg-18-normal;
  }
}
</style>
