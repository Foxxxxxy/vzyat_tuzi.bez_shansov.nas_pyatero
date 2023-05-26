<script setup>
import { PageListWrapper } from '~/components/page';
import {
  get_buildings,
  delete_building,
  get_current_building,
  edit_current_building,
  add_new_building,
} from '~/api/route.building';
import { ref } from 'vue';

const editableInputs = ref([
  {
    name: 'Тип здания',
    key: 'name',
    value: '',
    mark: ''
  },
  {
    name: 'Средняя стоимость, в руб',
    key: 'average_price_rub',
    value: '',
    mark: ' руб.'
  },
]);

</script>

<template>
  <div>
    <page-list-wrapper
      :get-all-action="get_buildings"
      :get-current-action="get_current_building"
      :delete-action="delete_building"
      :edit-action="edit_current_building"
      :add-action="add_new_building"
      :config-inputs="editableInputs"
      page-title="Список зданий"
      add-title="Создать здание"
    />
  </div>
</template>

<style lang="scss" scoped></style>
