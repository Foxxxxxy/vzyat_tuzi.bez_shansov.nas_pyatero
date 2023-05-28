<script setup>
import { IconEdit, IconDelete } from '../icons';

const props = defineProps({
  titles: Array,
  idx: Number,
  item: Object,
  immediateClick: Boolean
});

const emit = defineEmits(['edit', 'remove']);

const edit = () => {
  emit('edit', props.item);
};

const remove = () => {
  emit('remove', props.item);
};

const immediate = () => {
  if (!props.immediateClick) return
  emit('edit', props.item);
}
</script>

<template>
  <div class="row" @click="immediate" :class="{ double: idx % 2 === 0, cursor: immediateClick }">
    <div class="row__content">
      <p class="row__name" v-for="(title, idx) of titles" :key="idx">
        <p class="row__title">{{ title.name }}:</p>
        <p class="row__value">{{ title.value }}</p>
      </p>
    </div>
    <div class="row__buttons">
      <icon-wrapper @click="edit" class="row__edit" width="20" height="20">
        <icon-edit />
      </icon-wrapper>
      <icon-wrapper @click="remove" class="row__delete" width="20" height="20">
        <icon-delete />
      </icon-wrapper>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.row {
  display: flex;
  padding: 18px 0;
  transition: border 0.4s ease;
  border-radius: 5px;
  border: 1px solid transparent;
  align-items: center;
  justify-content: space-between;
  &:hover {
    border: 1px solid $accent-purple;
  }
  &__buttons {
    display: flex;
    margin-right: 20px;
  }
  &__edit {
    margin-right: 15px;
  }
  &__edit,
  &__delete {
    cursor: pointer;
    color: $accent-purple;
    &:hover {
      opacity: 0.6;
    }
  }
  &__name {
    @include create-font(14px, 400, 14px);
    padding-left: 20px;
    margin-bottom: 5px;
  }
  &__title {
    @include create-font(10px, 400);
    color: $primary-grey;
    margin-bottom: 3px;
  }
  &__value {
    @include create-font(14px, 600);
  }
  &.double {
    background-color: #f5f6f8;
  }
}
</style>
