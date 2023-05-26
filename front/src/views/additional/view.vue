<script setup>
import { PageListWrapper } from '~/components/page';
import {
  get_additionals,
  delete_additional,
  get_current_additional,
  edit_current_additional,
  add_new_additional,
} from '~/api/route.additional';
import { ref } from 'vue';

const editableInputs = ref([
  {
    name: 'Тип',
    key: 'name',
    value: '',
    mark: ''
  },
  {
    name: 'Стоимость, долл.',
    key: 'average_price_dollar',
    value: '',
    mark: ' $'
  },
]);
</script>

<template>
  <div>
    <page-list-wrapper
      :get-all-action="get_additionals"
      :get-current-action="get_current_additional"
      :delete-action="delete_additional"
      :edit-action="edit_current_additional"
      :add-action="add_new_additional"
      :config-inputs="editableInputs"
      page-title="Разное"
      add-title="Создать"
    />
  </div>
</template>

<style lang="scss" scoped></style>
