<script setup>
defineProps({
  titles: Array,
});
</script>

<template>
  <div class="row" :style="{ gridTemplateColumns: `repeat(${titles.length}, 1fr)  40px 40px` }">
    <p
      class="row__name"
      v-for="(title, idx) of titles"
      :key="idx"
    >
      {{ title }}
    </p>
  </div>
</template>

<style lang="scss" scoped>
.row {
  display: grid;
  padding: 8px 0;
  margin-bottom: 10px;
  &__name {
    @include create-font(12px, 500, 16px);
    color: $primary-grey;
    padding-left: 20px;
  }
}
</style>
