<script setup>
import { PageListWrapper } from '~/components/page';
import {
  get_users,
  get_current_user
} from '~/api/route.user';
import { ref } from 'vue';

const editableInputs = ref([
  {
    name: 'Фамилия',
    key: 'last_name',
    value: '',
    mark: ''
  },
  {
    name: 'Имя',
    key: 'name',
    value: '',
    mark: ''
  },
  {
    name: 'ИНН',
    key: 'inn',
    value: '',
    mark: ' руб.'
  },
  {
    name: 'Наименование организации',
    key: 'organisation_name',
    value: '',
    mark: ''
  },
  {
    name: 'Веб-сайт организации',
    key: 'web_site',
    value: '',
    mark: ''
  },
]);
</script>

<template>
  <div>
    <page-list-wrapper
      :get-all-action="get_users"
      :get-current-action="get_current_user"
      :config-inputs="editableInputs"
      :view-only="true"
      page-title="Список пользователей"
    />
  </div>
</template>

<style lang="scss" scoped></style>


<!-- <script setup>
import { ElementTableTitle, ElementTableElement } from '~/components/elements';
import {
  get_users,
  get_current_user
} from '~/api/route.user';
import { ref, onMounted, computed, watch } from 'vue';
import { useStore } from '~/stores/stores.main';
import { useRouter, useRoute } from 'vue-router';
import { PageEdit } from '~/components/page';

const users = ref(null);
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
    return () => {};
  }
  return () => {};
});

const editableInputs = ref([
  {
    name: 'Фамилия',
    key: 'last_name',
    value: '',
    mark: ''
  },
  {
    name: 'Имя',
    key: 'name',
    value: '',
    mark: ''
  },
  {
    name: 'ИНН',
    key: 'inn',
    value: '',
    mark: ' руб.'
  },
  {
    name: 'Наименование организации',
    key: 'organisation_name',
    value: '',
    mark: ''
  },
  {
    name: 'Веб-сайт организации',
    key: 'web_site',
    value: '',
    mark: ''
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
  await delete_user(currentItem.value.id, token.value);
  users.value = users.value.filter(
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
    const data = await get_current_user(currentRouteId.value);
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
    users.value = await get_users();
  }
})

watch(currentRouteId, async () => {
  await updateCurrentItem();
});

onMounted(async () => {
  users.value = await get_users();
  await updateCurrentItem();
  if (isCreateAction.value) {
    currentAction.value = 'create'
  }
});
</script>

<template>
    <div v-if="!isCreateAction && !currentRouteId" class="users">
      <div class="users__header">
        <h1 class="users__title">Список пользователей</h1>
      </div>
      <div class="users__content">
        <element-table-title :titles="titles" />
        <element-table-element
          class="users__row"
          v-for="(item, idx) of users"
          :idx="idx"
          :titles="createTitle(item)"
          :item="item"
          @edit="edit(item)"
        />
      </div>
    </div>
    <page-edit
      v-else
      :view-only="true"
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
.users {
  background-color: $primary-white;
  min-height: 100%;
  &__row {
    &::v-deep(.row__delete) {
      display: none;
    }
  }
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
</style> -->
