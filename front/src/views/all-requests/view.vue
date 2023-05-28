<script setup>
import { PageListWrapper } from '~/components/page';
import { get_calculations, get_calculation_preview } from '~/api/route.calculation';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from '~/stores/stores.main';

const store = useStore()
const router = useRouter()

const editableInputs = ref([
  {
    name: 'Имя',
    key: 'name',
    value: '',
    mark: '',
  },
  {
    name: 'Дата',
    key: 'timestamp',
    value: '',
    mark: ' $',
  },
]);

const revert = async (item) => {
  const data = await get_calculation_preview(item.id, store.$state.user.token)
  store.result = {...data}
  router.push('/review')
};

const functionWrapper = async (token) => {
  const res = await get_calculations(token)
  if (res.status !== 'error') {
    const res_data = []
    res.forEach(item => {
      item[0]['name'] = item[1].name
      res_data.push(item[0])
      return item
    })
    return res_data
  }
}
</script>

<template>
  <page-list-wrapper
    page-title="История всех запросов"
    variant="calculation"
    :get-all-action="functionWrapper"
    :config-inputs="editableInputs"
    :view-only="true"
    :immediate-click="true"
    @revert-calculation="revert"
  />
</template>

<style lang="scss" scoped></style>
