<script setup>
import { PageListWrapper } from '~/components/page';
import {
  get_industrys,
  delete_industry,
  get_current_industry,
  edit_current_industry,
  add_new_industry,
} from '~/api/route.industry';
import { ref } from 'vue';

const editableInputs = ref([
  {
    name: 'Тип отрасли',
    key: 'name',
    value: '',
    mark: ''
  },
]);


</script>

<template>
  <div>
    <page-list-wrapper
      :get-all-action="get_industrys"
      :get-current-action="get_current_industry"
      :delete-action="delete_industry"
      :edit-action="edit_current_industry"
      :add-action="add_new_industry"
      :config-inputs="editableInputs"
      page-title="Список отраслей"
      add-title="Создать отрасль"
    />
  </div>
</template>

<style lang="scss" scoped></style>
