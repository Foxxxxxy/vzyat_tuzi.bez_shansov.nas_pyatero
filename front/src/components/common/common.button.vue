<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: function (value) {
      return ['outlined', 'grey', 'primary', 'red'].indexOf(value) !== -1
    },
  },
  wrap: {
    type: String,
    default: 'no-wrap',
  },
})
</script>

<template>
  <button class="el" type="button" :class="[`el-${variant}`, `el-${wrap}`]">
    <slot />
  </button>
</template>

<style scoped lang="scss">
.el {
  $btn-transition: 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 22px;
  border-radius: 4px;
  @include create-font(16px, 600, 20px);
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
