<script setup>
import { ref } from 'vue';

const props = defineProps({
  value: {
    type: [String, Number],
    required: true
  },
  required: Boolean,
  label: {
    type: String,
  },
  type: {
    type: String,
    default: () => 'text',
  },
  viewOnly: Boolean,
  isErrored: Boolean,
});

const emit = defineEmits(['update:modelValue']);

const updateInput = (ev) => {
  emit('update:modelValue', ev.target.value);
};

const isActiveLabel = ref(false)

const focus = () => {
  isActiveLabel.value = true
}

const blur = () => {
  if (!props.value) {
    isActiveLabel.value = false
  }
}

</script>

<template>
  <label class="label">
    <p class="label__title">
      {{ label }}
      <span v-if="required" class="label__required">*</span>
    </p>
    <input
      v-if="!viewOnly"
      :type="type"
      :class="{ error: isErrored }"
      class="input"
      @input="updateInput"
      @focus="focus"
      @blur="blur"
      :value="value"
    />
    <p v-else class="label__view">{{ value }}</p>
  </label>
</template>

<style lang="scss" scoped>

.label {
  position: relative;
  display: block;
  &__required {
    color: red;
  }
  &__view {
    font-weight: bold
  }
  &__title {
    @include create-font(16px, 400, 22px);
    color: $primary-grey;
    transition: 0.3s ease all;
    background-color: #ffffff;
    text-align: left;
    padding-bottom: 12px;
    &.active {
      @include create-font(14px, 400, 22px);
      top: -27px;
      left: 2px;
    }
  }
}
.input {
  border: 1px solid $accent-purple;
  padding: 10px 20px 10px 10px;
  border-radius: 5px;
  transition: border 0.3s ease;
  color: #000000;
  width: 100%;
  &:hover {
    border: 1px solid $accent-purple;
  }
  &.error {
    border: 1px solid red;
  }
}
</style>
