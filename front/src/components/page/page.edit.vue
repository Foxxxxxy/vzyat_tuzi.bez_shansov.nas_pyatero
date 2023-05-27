<script setup>
import { computed } from 'vue';
import { CommonInput, CommonButton } from '../common';
import { useStore } from '~/stores/stores.main';
import { useRouter } from 'vue-router';

const store = useStore()
const router = useRouter()

const props = defineProps({
  blocks: Array,
  item: Object,
  actionUrl: Function,
  viewOnly: {
    type: Boolean,
    default: () => false
  },
  backUrl: {
    type: String,
    default: () => ''
  },
  action: {
    type: String,
    default: () => 'edit'
  }
});

const token = computed(() => store.$state.user.token)

const computedButtonTitle = computed(() => {
  if (props.action === 'edit') {
    return 'Сохранить'
  }
  return 'Создать'
})

const computedTitle = computed(() => {
  if (props.viewOnly) {
    return "Просмотр"
  }
  if (props.action === 'edit') {
    return 'Редактирование'
  }
  return 'Создание'
})

const action = async () => {
  const formattedObject = {}
    props.blocks.forEach(item => {
      formattedObject[item.key] = item.value
    })
  if (props.action === 'edit') {
    await props.actionUrl(props.item.id, {...formattedObject}, token.value)
    router.push(props.backUrl)
    return
  }
  await props.actionUrl({...formattedObject}, token.value)
  router.push(props.backUrl)
}

</script>

<template>
  <div class="edit">
    <div class="edit__header">
      <h1 class="edit__title">{{ computedTitle }}</h1>
      <div class="edit__buttons">
        <common-button v-if="!viewOnly" @click="action" class="edit__button"> {{ computedButtonTitle }} </common-button>
        <router-link :to="backUrl">
          <common-button variant="outlined" class="edit__button">
            Назад
          </common-button>
        </router-link>
      </div>
    </div>
    <div class="edit__content">
      <div class="edit__form">
        <div class="edit__block" v-for="(block, index) of blocks" :key="index">
          <common-input
            :view-only="viewOnly"
            :label="block.name"
            :value="block.value"
            v-model="block.value"
            class="edit__input"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.edit {
  background-color: $primary-white;
  min-height: 100%;
  &__buttons {
    display: flex;
    @include md {
      margin-left: 10px;
    }
  }
  &__button {
    &:not(:last-child) {
      margin-right: 8px;
    }
  }
  &__content {
    padding: 32px;
  }
  &__form {
    max-width: 500px;
  }
  &__block {
    &:not(:last-child) {
      margin-bottom: 12px;
    }
  }
  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    align-items: center;
    padding: 41px 32px 41px 0;
    @include md {
      flex-direction: column;
      align-items: flex-start;
    }
  }
  &__title {
    position: relative;
    @include create-font(26px, 600, 23px);
    padding-left: 32px;
    @include md {
      margin-bottom: 30px;
    }
    &::before {
      content: '';
      height: calc(100% + 10px);
      position: absolute;
      top: -5px;
      width: 4px;
      border-radius: 4px;
      background-color: $accent-purple;
      left: 0;
    }
  }
}
</style>
