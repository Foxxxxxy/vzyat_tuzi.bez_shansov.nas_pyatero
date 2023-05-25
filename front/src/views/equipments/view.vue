<script setup>
import { CommonButton } from '~/components/common';
import { ElementTableTitle, ElementTableElement } from '~/components/elements';
import { get_equipments } from '~/api/route.equipment';
import { ref, onMounted } from 'vue';

const equipments = ref(null);

const titles = ['Тип', 'Средняя стоимость, долл'];

const createTitle = (item) => {
  return [item.name, item.average_price_dollar + " $"];
};

const edit = () => {
  console.log('edit');
}

const remove = () => {
  console.log('remove');
}

onMounted(async () => {
  equipments.value = await get_equipments();
});
</script>

<template>
  <div class="equipments">
    <div class="equipments__header">
      <h1 class="equipments__title">Список оборудования</h1>
      <div class="equipments__buttons">
        <common-button class="equipments__button">
          Создать оборудование
        </common-button>
      </div>
    </div>
    <div class="equipments__content">
      <element-table-title :titles="titles" />
      <element-table-element
        v-for="(item, idx) of equipments"
        :idx="idx"
        :titles="createTitle(item)"
        :item="item"
        @edit="edit"
        @remove="remove"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.equipments {
  background-color: $primary-white;
  min-height: 100%;
  &__content {
    padding: 32px;
  }
  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    align-items: center;
    padding: 41px 32px 41px 0;
  }
  &__title {
    position: relative;
    @include create-font(26px, 600, 23px);
    padding-left: 32px;
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
