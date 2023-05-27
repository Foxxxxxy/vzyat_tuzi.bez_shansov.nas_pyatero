<script setup>
import { PageListWrapper } from '~/components/page';
import {
  get_additionals,
  delete_additional,
  get_current_additional,
  edit_current_additional,
  add_new_additional,
  get_xlsx_template,
  send_glsx_template,
} from '~/api/route.additional';
import { ref } from 'vue';
import { useStore } from '~/stores/stores.main';

const editableInputs = ref([
  {
    name: 'Тип',
    key: 'name',
    value: '',
    mark: '',
  },
  {
    name: 'Стоимость, долл.',
    key: 'average_price_dollar',
    value: '',
    mark: ' $',
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
    :get-all-action="get_additionals"
    :get-current-action="get_current_additional"
    :delete-action="delete_additional"
    :edit-action="edit_current_additional"
    :add-action="add_new_additional"
    :config-inputs="editableInputs"
    page-title="Разное"
    add-title="Создать"
  />
</template>

<style lang="scss" scoped></style>
