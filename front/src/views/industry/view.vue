<script setup>
import { PageListWrapper } from '~/components/page';
import {
  get_industrys,
  delete_industry,
  get_current_industry,
  edit_current_industry,
  add_new_industry,
  get_xlsx_template,
  send_glsx_template,
} from '~/api/route.industry';
import { ref } from 'vue';
import { useStore } from '~/stores/stores.main';

const editableInputs = ref([
  {
    name: 'Тип отрасли',
    key: 'name',
    value: '',
    mark: '',
  },
]);

const store = useStore();
const refresh = ref(true);

const changeFiles = async (e) => {
  await send_glsx_template(e, store.$state.user.token);
  refresh.value = !refresh.value;
};
</script>

<template>
  <page-list-wrapper
    :refresh="refresh"
    :get-xlsx-action="get_xlsx_template"
    :send-file-action="changeFiles"
    :get-all-action="get_industrys"
    :get-current-action="get_current_industry"
    :delete-action="delete_industry"
    :edit-action="edit_current_industry"
    :add-action="add_new_industry"
    :config-inputs="editableInputs"
    page-title="Список отраслей"
    add-title="Создать отрасль"
  />
</template>

<style lang="scss" scoped></style>
