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

const revert = async (item) => {
  const data = await get_calculation_preview(item.id, store.$state.user.token)
  store.result = {...data}
  router.push('/review')
};
</script>

<template>
  <page-list-wrapper
    page-title="История всех запросов"
    variant="calculation"
    :get-all-action="get_calculations"
    :config-inputs="editableInputs"
    :view-only="true"
    @revert-calculation="revert"
  />
</template>

<style lang="scss" scoped></style>
