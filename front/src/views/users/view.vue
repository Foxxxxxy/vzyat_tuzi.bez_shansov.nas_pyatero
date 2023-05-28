<script setup>
import { PageListWrapper } from '~/components/page';
import { get_users, get_current_user } from '~/api/route.user';
import { ref } from 'vue';

const editableInputs = ref([
  {
    name: 'Фамилия',
    key: 'last_name',
    value: '',
    mark: '',
  },
  {
    name: 'Имя',
    key: 'name',
    value: '',
    mark: '',
  },
  {
    name: 'ИНН',
    key: 'inn',
    value: '',
    mark: ' руб.',
  },
  {
    name: 'Наименование организации',
    key: 'organisation_name',
    value: '',
    mark: '',
  },
  {
    name: 'Уровень доступа',
    key: 'level',
    value: '',
    mark: '',
  },
]);
</script>

<template>
  <page-list-wrapper
    :get-all-action="get_users"
    :get-current-action="get_current_user"
    :config-inputs="editableInputs"
    :view-only="true"
    page-title="Список пользователей"
  />
</template>

<style lang="scss" scoped></style>
