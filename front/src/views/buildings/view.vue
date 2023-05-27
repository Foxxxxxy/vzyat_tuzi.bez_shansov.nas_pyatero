<script setup>
import { PageListWrapper } from '~/components/page';
import {
  get_buildings,
  delete_building,
  get_current_building,
  edit_current_building,
  add_new_building,
  get_xlsx_template,
  send_glsx_template
} from '~/api/route.building';
import { ref } from 'vue';
import { useStore } from '~/stores/stores.main';

const editableInputs = ref([
  {
    name: 'Тип здания',
    key: 'name',
    value: '',
    mark: '',
  },
  {
    name: 'Средняя стоимость, в руб',
    key: 'average_price_rub',
    value: '',
    mark: ' руб.',
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
    :get-xlsx-action="get_xlsx_template"
    :send-file-action="changeFiles"
    :get-all-action="get_buildings"
    :get-current-action="get_current_building"
    :delete-action="delete_building"
    :edit-action="edit_current_building"
    :add-action="add_new_building"
    :config-inputs="editableInputs"
    page-title="Список зданий"
    add-title="Создать здание"
  />
</template>

<style lang="scss" scoped></style>
