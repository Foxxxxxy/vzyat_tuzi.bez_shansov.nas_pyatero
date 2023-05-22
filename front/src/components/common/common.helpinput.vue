<script setup>
import { ref, reactive } from 'vue';

const props = defineProps({
  value: {
    type: String,
    required: true,
  },
  required: Boolean,
  label: {
    type: String,
  },
  type: {
    type: String,
    default: () => 'text',
  },
  suggestions: {
    type: Array,
    default: () => [],
  },
  isErrored: Boolean,
});

const emit = defineEmits(['update:modelValue', 'set-item']);

const updateInput = (ev) => {
  emit('update:modelValue', ev.target.value);
  isActiveLabel.value = true;
};

const isActiveLabel = ref(false);

const currentSuggestion = ref({});

const focus = () => {
  isActiveLabel.value = true;
};

const blur = () => {
  setTimeout(() => {
    isActiveLabel.value = false;
  }, 200);
};

const setItem = (item) => {
  currentSuggestion.value = item;
  emit('update:modelValue', item.name);
  emit('set-item', item);
};
</script>

<template>
  <div class="label">
    <p class="label__title">
      {{ label }}
      <span v-if="required" class="label__required">*</span>
    </p>
    <input
      :value="value"
      :type="type"
      :class="{ error: isErrored }"
      class="input"
      @input="updateInput"
      @blur="blur"
      @focus="focus"
    />
    <div class="suggestions" v-show="isActiveLabel">
      <div class="suggestions__item">
        <p class="suggestions__text">Выберите из списка:</p>
      </div>
      <div
        class="suggestions__item"
        @click="setItem(item)"
        v-for="item of suggestions"
        :key="item.id"
      >
        <p class="suggestions__text">{{ item.name }}</p>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.suggestions {
  background-color: $primary-white;
  border-radius: 5px;
  position: absolute;
  z-index: 100;
  width: 100%;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-top: transparent;
  padding: 0 10px;
  max-height: 150px;
  overflow: auto;
  &__item {
    cursor: pointer;
    padding: 10px 0;
    color: $primary-grey;
    &:first-child {
      color: $accent-purple;
      pointer-events: none;
    }
    &:not(:last-child) {
      border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    }
    &:hover {
      opacity: 0.7;
      color: $accent-purple;
    }
  }
  &__text {
    @include create-font(16px, 400, 22px);
  }
}

.label {
  position: relative;
  display: block;
  &__required {
    color: red;
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
