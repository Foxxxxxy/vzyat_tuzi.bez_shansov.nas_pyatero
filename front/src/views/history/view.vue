<script setup>
import { PageListWrapper } from '~/components/page';
import { get_calculation_preview } from '~/api/route.calculation';
import { get_user_review } from '~/api/route.user';
import { ref, computed } from 'vue';
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

const user_id = computed(() => store.$state.user.user_id)

const revert = async (item) => {
  const data = await get_calculation_preview(item.id, store.$state.user.token)
  store.result = {...data}
  router.push('/review')
};

const functionWrapper = async (token) => {
  const res = await get_user_review(user_id.value, token)
  if (res.status !== 'error') {
    const data = res[0]
    data.forEach(item => {
      item['name'] = res[1].name
      return item
    })
    return data
  }
}
</script>

<template>
  <page-list-wrapper
    page-title="История запросов"
    variant="calculation"
    :get-all-action="functionWrapper"
    :config-inputs="editableInputs"
    :view-only="true"
    :immediate-click="true"
    @revert-calculation="revert"
  />
</template>

<style lang="scss" scoped></style>
