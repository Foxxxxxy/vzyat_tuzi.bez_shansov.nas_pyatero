<script setup>
import { PageListWrapper } from '~/components/page';
import {
  get_calculations,
} from '~/api/route.calculation';
import { ref } from 'vue';

const editableInputs = ref([
  {
    name: 'Отрасль',
    key: 'industry',
    value: '',
    mark: '',
  },
  {
    name: 'Средняя стоимость, в долл',
    key: 'average_price_dollar',
    value: '',
    mark: ' $',
  },
]);
</script>

<template>
  <div>
    <page-list-wrapper
      :get-all-action="get_calculations"
      :config-inputs="editableInputs"
      :view-only="true"
      page-title="Список оборудования"
      add-title="Создать оборудования"
    />
  </div>
</template>

<style lang="scss" scoped></style>
