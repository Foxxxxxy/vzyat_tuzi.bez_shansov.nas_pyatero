<script setup>
import { CommonPopup, CommonButton } from '~/components/common';
import { ElementTableTitle, ElementTableElement } from '~/components/elements';
import {
  get_buildings,
  delete_building,
  get_current_building,
  edit_current_building,
  add_new_building,
} from '~/api/route.building';
import { ref, onMounted, computed, watch } from 'vue';
import { useStore } from '~/stores/stores.main';
import { useRouter, useRoute } from 'vue-router';
import { PageEdit } from '~/components/page';

const buildings = ref(null);
const router = useRouter();
const route = useRoute();

const store = useStore();

const token = computed(() => store.$state.user.token);

const isShowDeletePopup = ref(false);
const currentItem = ref({});

const currentRouteId = computed(() => route.query.id);
const isCreateAction = computed(() => !!route.query.create)

const currentAction = ref('edit');

const currentActionUrl = computed(() => {
  if (currentAction.value === 'edit') {
    return edit_current_building;
  }
  return add_new_building;
});

const editableInputs = ref([
  {
    name: 'Тип здания',
    key: 'name',
    value: '',
    mark: ''
  },
  {
    name: 'Средняя стоимость, в руб',
    key: 'average_price_rub',
    value: '',
    mark: ' руб.'
  },
]);

const titles = editableInputs.value.map(el => el.name);

const createTitle = (item) => {
  return editableInputs.value.map(el => item[el.key])
};

const createPopupDesc = () => {
  let str = ''
  editableInputs.value.forEach(el => {
    str += `${el.name}: ${el.value} ${el.mark}`
  })
  return str
}

const edit = (item) => {
  router.push(`${route.path}?id=${item.id}`);
  currentItem.value = { ...item };
  currentAction.value = 'edit';
};

const remove = async () => {
  await delete_building(currentItem.value.id, token.value);
  buildings.value = buildings.value.filter(
    (item) => item.id !== currentItem.value.id
  );
  isShowDeletePopup.value = false;
  currentItem.value = {};
};

const handleRemove = (item) => {
  currentItem.value = item;
  isShowDeletePopup.value = true;
};

const closePopup = () => {
  isShowDeletePopup.value = false;
  currentItem.value = {};
};

watch(currentItem, () => {
  editableInputs.value.forEach((element) => {
    element.value = currentItem.value[element.key];
  });
});

const updateCurrentItem = async () => {
  if (currentRouteId.value && currentRouteId.value.length) {
    const data = await get_current_building(currentRouteId.value);
    currentItem.value = { ...data };
  }
};

const createNew = () => {
  currentAction.value = 'create'
  router.push(`${route.path}?create=true`)
  editableInputs.value.forEach(item => {
    item.value = ''
  })
}

watch(() => route.query, async () => {
  if (Object.keys(route.query).length === 0) {
    buildings.value = await get_buildings();
  }
})

watch(currentRouteId, async () => {
  await updateCurrentItem();
});

onMounted(async () => {
  buildings.value = await get_buildings();
  await updateCurrentItem();
  if (isCreateAction.value) {
    currentAction.value = 'create'
  }
});
</script>

<template>
    <div v-if="!isCreateAction && !currentRouteId" class="buildings">
      <common-popup
        :is-active="isShowDeletePopup"
        class="popup"
        title="Вы действительно хотите удалить данное оборудование?"
        :desc="createPopupDesc()"
      >
        <common-button
          @click="closePopup"
          class="popup__button"
          variant="outlined"
        >
          Нет
        </common-button>
        <common-button @click="remove" class="popup__button">
          Да
        </common-button>
      </common-popup>
      <div class="buildings__header">
        <h1 class="buildings__title">Список зданий</h1>
        <div class="buildings__buttons">
          <common-button @click="createNew" class="buildings__button">
            Создать здание
          </common-button>
        </div>
      </div>
      <div class="buildings__content">
        <element-table-title :titles="titles" />
        <element-table-element
          v-for="(item, idx) of buildings"
          :idx="idx"
          :titles="createTitle(item)"
          :item="item"
          @edit="edit(item)"
          @remove="handleRemove"
        />
      </div>
    </div>
    <page-edit
      v-else
      :blocks="editableInputs"
      :item="currentItem"
      :backUrl="route.path"
      :action="currentAction"
      :action-url="currentActionUrl"
    />
</template>

<style scoped lang="scss">
.wrapper {
  height: 100%;
}
.popup {
  z-index: 100;
  &__button {
    width: 100%;
    &:not(:last-child) {
      margin-right: 8px;
    }
  }
}
.buildings {
  background-color: $primary-white;
  min-height: 100%;
  &__content {
    padding: 32px;
  }
  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    align-items: center;
    padding: 41px 32px 41px 0;
    border-bottom: 1px dashed $accent-purple;
  }
  &__title {
    position: relative;
    @include create-font(26px, 600, 23px);
    padding-left: 32px;
    &::before {
      content: '';
      height: calc(100% + 10px);
      position: absolute;
      top: -5px;
      width: 4px;
      border-radius: 4px;
      background-color: $accent-purple;
      left: 0;
    }
  }
}
</style>
