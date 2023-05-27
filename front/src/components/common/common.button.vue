<script setup>
import { computed } from 'vue';

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: function (value) {
      return ['outlined', 'grey', 'primary', 'red'].indexOf(value) !== -1;
    },
  },
  btnType: {
    type: String,
    default: () => '',
  },
  wrap: {
    type: String,
    default: 'no-wrap',
  },
});

const emit = defineEmits(['add-file']);

const isFile = computed(() => props.btnType === 'file');

const changeFile = (e) => {
  emit('add-file', e);
};
</script>

<template>
  <button
    v-if="!isFile"
    class="el"
    type="button"
    :class="[`el-${variant}`, `el-${wrap}`]"
  >
    <slot />
  </button>
  <label
    class="el"
    type="button"
    :class="[`el-${variant}`, `el-${wrap}`]"
    v-else
  >
    <input v-if="isFile" type="file" class="el__file" @change="changeFile" />
    <slot />
  </label>
</template>

<style scoped lang="scss">
.el {
  $btn-transition: 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 22px;
  border-radius: 4px;
  border: 1px solid $accent-purple;
  @include create-font(16px, 600, 20px);
  cursor: pointer;
  &__file {
    position: absolute;
    left: -9999px;
  }
  &-no-wrap {
    white-space: nowrap;
  }

  transition: opacity $btn-transition, color $btn-transition,
    box-shadow $btn-transition, border-color $btn-transition;
  &-primary {
    background-color: $accent-purple;
    color: $primary-white;
    box-shadow: none;
    &:hover {
      opacity: 0.5;
    }
    &:active {
      box-shadow: 0px 2px 6px rgba(0, 220, 129, 0.3);
    }
    &:disabled {
      opacity: 0.3;
      pointer-events: none;
      touch-action: none;
    }
  }
  &-outlined {
    background-color: $primary-white;
    border: 1px solid $accent-purple;
    color: $accent-purple;
    box-shadow: none;
    &:hover {
      opacity: 0.5;
    }
    &:active {
      box-shadow: 0px 2px 6px rgba(0, 220, 129, 0.3);
    }
    &:disabled {
      opacity: 0.3;
      pointer-events: none;
      touch-action: none;
    }
  }
}
</style>
