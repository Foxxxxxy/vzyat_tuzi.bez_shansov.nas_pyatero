<script setup>
import { CommonPopup, CommonButton } from '~/components/common';
import {
  ElementTableTitle,
  ElementTableElement,
  ElementTableElementAdaptive,
} from '~/components/elements';
import { ref, onMounted, computed, watch } from 'vue';
import { useStore } from '~/stores/stores.main';
import { useRouter, useRoute } from 'vue-router';
import { PageEdit } from '~/components/page';

const props = defineProps({
  listData: Array,
  getAllAction: Function,
  getCurrentAction: Function,
  deleteAction: Function,
  editAction: Function,
  addAction: Function,
  configInputs: Array,
  pageTitle: String,
  addTitle: String,
  viewOnly: Boolean,
});

const listData = ref(null);
const router = useRouter();
const route = useRoute();

const store = useStore();

const token = computed(() => store.$state.user.token);

const isShowDeletePopup = ref(false);
const currentItem = ref({});

const currentRouteId = computed(() => route.query.id);
const isCreateAction = computed(() => !!route.query.create);

const currentAction = ref('edit');

const titles = props.configInputs.map((el) => el.name);

const currentActionUrl = computed(() => {
  if (currentAction.value === 'edit') {
    return props.editAction;
  }
  return props.addAction;
});

const createTitle = (item) => {
  return props.configInputs.map((el) => item[el.key]);
};

const createAdaptiveTitle = (item) => {
  return props.configInputs.map((el) => {
    return { name: el.name, value: item[el.key] };
  });
};

const edit = (item) => {
  router.push(`${route.path}?id=${item.id}`);
  currentItem.value = { ...item };
  currentAction.value = 'edit';
};

const remove = async () => {
  await props.deleteAction(currentItem.value.id, token.value);
  isShowDeletePopup.value = false;
  listData.value = listData.value.filter(
    (item) => item.id !== currentItem.value.id
  );
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
  props.configInputs.forEach((element) => {
    element.value = currentItem.value[element.key];
  });
});

const updateCurrentItem = async () => {
  if (currentRouteId.value && currentRouteId.value.length) {
    const data = await props.getCurrentAction(currentRouteId.value, {
      token: token.value,
    });
    currentItem.value = { ...data };
  }
};

const createNew = () => {
  currentAction.value = 'create';
  router.push(`${route.path}?create=true`);
  props.configInputs.forEach((item) => {
    item.value = '';
  });
};

const createPopupDesc = () => {
  let str = '';
  props.configInputs.forEach((el) => {
    str += `${el.name}: ${el.value} ${el.mark}`;
  });
  return str;
};

watch(
  () => route.query,
  async () => {
    if (Object.keys(route.query).length === 0) {
      listData.value = await props.getAllAction({ token: token.value });
    }
  }
);

watch(currentRouteId, async () => {
  await updateCurrentItem();
});

const windowSize = ref(window.innerWidth);

onMounted(async () => {
  listData.value = await props.getAllAction({ token: token.value });
  await updateCurrentItem();
  if (isCreateAction.value) {
    currentAction.value = 'create';
  }
  window.addEventListener('resize', () => {
    windowSize.value = window.innerWidth;
  });
});
</script>

<template>
  <div v-if="!isCreateAction && !currentRouteId" class="pages">
    <common-popup
      v-if="!viewOnly"
      :is-active="isShowDeletePopup"
      class="popup"
      title="Вы действительно хотите удалить?"
      :desc="createPopupDesc()"
    >
      <common-button
        @click="closePopup"
        class="popup__button"
        variant="outlined"
      >
        Нет
      </common-button>
      <common-button @click="remove" class="popup__button"> Да </common-button>
    </common-popup>
    <div class="pages__header" :class="{ view: viewOnly }">
      <h1 class="pages__title">{{ pageTitle }}</h1>
      <div class="pages__buttons" v-if="!viewOnly">
        <common-button @click="createNew" class="pages__button">
          {{ addTitle }}
        </common-button>
      </div>
    </div>
    <div class="pages__content" v-if="windowSize > 576">
      <element-table-title :titles="titles" />
      <element-table-element
        class="pages__row"
        :class="{ view: viewOnly }"
        v-for="(item, idx) of listData"
        :idx="idx"
        :titles="createTitle(item)"
        :item="item"
        @edit="edit(item)"
        @remove="handleRemove"
      />
    </div>
    <div class="pages__content" v-else>
      <element-table-element-adaptive
        class="pages__row"
        :class="{ view: viewOnly }"
        v-for="(item, idx) of listData"
        :idx="idx"
        :titles="createAdaptiveTitle(item)"
        :item="item"
        @edit="edit(item)"
        @remove="handleRemove"
      />
    </div>
  </div>
  <page-edit
    v-else
    :view-only="viewOnly"
    :blocks="configInputs"
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
.pages {
  background-color: $primary-white;
  min-height: 100%;
  &__row {
    &.view {
      &::v-deep(.row__delete) {
        display: none;
      }
    }
  }
  &__content {
    padding: 32px;
    @include sm {
      padding: 0 0 32px 0;
    }
  }
  &__buttons {
    @include md {
      margin-left: 10px;
    }
  }
  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    align-items: center;
    padding: 41px 32px 41px 0;
    border-bottom: 1px dashed $accent-purple;
    &.view {
      .pages__title {
        margin: 0;
      }
    }
    @include md {
      flex-direction: column;
      align-items: flex-start;
    }
  }
  &__title {
    position: relative;
    @include create-font(26px, 600, 23px);
    padding-left: 32px;
    @include md {
      margin-bottom: 30px;
    }
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
