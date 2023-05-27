<script setup>
import { PageListWrapper } from '~/components/page';
import {
  get_equipments,
  delete_equipment,
  get_current_equipment,
  edit_current_equipment,
  add_new_equipment,
  get_xlsx_template,
  send_glsx_template
} from '~/api/route.equipment';
import { ref } from 'vue';
import { useStore } from '~/stores/stores.main';

const editableInputs = ref([
  {
    name: 'Тип оборудования',
    key: 'name',
    value: '',
    mark: '',
  },
  {
    name: 'Средняя стоимость, в долл.',
    key: 'average_price_dollar',
    value: '',
    mark: ' $',
  },
]);

const store = useStore()
const refresh = ref(true)

const changeFiles = async (e) => {
  await send_glsx_template(e, store.$state.user.token)
  refresh.value = !refresh.value
}
</script>

<template>
  <page-list-wrapper
    :refresh="refresh"
    :get-all-action="get_equipments"
    :get-current-action="get_current_equipment"
    :delete-action="delete_equipment"
    :edit-action="edit_current_equipment"
    :add-action="add_new_equipment"
    :get-xlsx-action="get_xlsx_template"
    :config-inputs="editableInputs"
    :send-file-action="changeFiles"
    page-title="Список оборудования"
    add-title="Создать оборудования"
  />
</template>

<style lang="scss" scoped></style>
