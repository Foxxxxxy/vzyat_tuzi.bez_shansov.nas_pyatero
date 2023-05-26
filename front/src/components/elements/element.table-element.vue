<script setup>
import { IconEdit, IconDelete } from '../icons';

const props = defineProps({
  titles: Array,
  idx: Number,
  item: Object,
});

const emit = defineEmits(['edit', 'remove']);

const edit = () => {
  emit('edit', props.item);
};

const remove = () => {
  emit('remove', props.item);
};
</script>

<template>
  <div
    class="row"
    :class="{ double: idx % 2 === 0 }"
    :style="{ gridTemplateColumns: `repeat(${titles.length}, 1fr) 40px 40px` }"
  >
    <p class="row__name" v-for="(title, idx) of titles" :key="idx">
      {{ title }}
    </p>
    <icon-wrapper @click="edit" class="row__edit" width="20" height="20">
      <icon-edit />
    </icon-wrapper>
    <icon-wrapper @click="remove" class="row__delete" width="20" height="20">
      <icon-delete />
    </icon-wrapper>
  </div>
</template>

<style lang="scss" scoped>
.row {
  display: grid;
  padding: 18px 0;
  transition: border 0.4s ease;
  border-radius: 5px;
  border: 1px solid transparent;
  align-items: center;
  cursor: pointer;
  &:hover {
    border: 1px solid $accent-purple;
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
  }
  &.double {
    background-color: #f5f6f8;
  }
}
</style>
