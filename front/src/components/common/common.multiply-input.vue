<script setup>
import {
  CommonInput,
  CommonHelpinput,
} from '~/components/common';
import { IconPlus } from '~/components/icons';

const props = defineProps({
  suggestionKey: String,
  block: Array,
  labelMain: String,
  labelCount: String
})

const emit = defineEmits(['add', 'delete', 'updateSuggestion', 'setSuggestions'])

const addMore = () => {
  emit('add', props.suggestionKey, props.block[0].route)
}

const deleteItem = () => {
  emit('delete', props.suggestionKey, props.block.length - 1)
}

const updateSuggestion = (type, index) => {
  emit('add', type, index)
}

const setSuggestions = (item, type, index) => {
  emit('setSuggestions', item, type, index)
}

</script>

<template>
  <div>
    <div
      v-for="(item, index) of block"
      :key="index"
      class="home-modal__block home-modal__block--fluid"
    >
      <common-helpinput
        v-model="item.value"
        class="home-modal__input"
        :label="index > 0 ? '' : labelMain"
        :value="item.value"
        :suggestions="item.suggestions"
        @input="updateSuggestion(suggestionKey, index)"
        @set-item="(item) => setSuggestions(item, suggestionKey, index)"
      />
      <common-input
        v-model.number="item.count"
        :value="item.count"
        class="home-modal__input"
        :label="index > 0 ? '' : labelCount"
      />
    </div>
    <div class="home-modal__actions">
      <span @click="addMore" class="home-modal__more">
        <icon-wrapper class="home-modal__more-icon" width="13" height="13">
          <icon-plus />
        </icon-wrapper>
        Добавить еще поле
      </span>
      <span
        v-show="block.length > 1"
        @click="deleteItem"
        class="home-modal__more"
      >
        <icon-wrapper class="home-modal__more-icon" width="13" height="13">
          <icon-plus />
        </icon-wrapper>
        Удалить поле
      </span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.home {
  &-modal {
    &__actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }
    &__more {
      display: flex;
      align-items: center;
      @include create-font(14px, 500, 18px);
      color: $accent-purple;
      cursor: pointer;
      &-icon {
        margin-right: 8px;
        color: $accent-purple;
      }
      &:last-child {
        color: red;
        .home-modal__more-icon {
          color: red;
          transform: rotate(45deg);
        }
      }
    }
    &__block {
      &--fluid {
        display: flex;
        align-items: flex-end;

        .home-modal__input:first-child {
          width: 175%;
          margin-right: 8px;
        }
        .home-modal__input:last-child {
          width: 70%;
        }
      }
      &:not(:last-child) {
        margin-bottom: 12px;
      }
      &-hint {
        @include create-font(14px, 400, 22px);
        margin-top: 6px;
      }
    }
    &__input {
      width: 100%;
    }
  }
}
</style>
