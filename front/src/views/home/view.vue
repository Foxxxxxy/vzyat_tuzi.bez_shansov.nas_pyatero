<script setup>
import { reactive, ref, onMounted, watch } from 'vue';
import { ElementMap } from '~/components/elements';
import {
  CommonButton,
  CommonInput,
  CommonHelpinput,
  CommonMultiplyInput,
} from '~/components/common';
import { get_equipment_suggestion } from '~/api/route.equipment';
import { get_building_suggestion } from '~/api/route.building';
import { get_industry_suggestion } from '~/api/route.industry';
import { get_district_suggestion } from '~/api/route.district';
import { get_additional_suggestion } from '~/api/route.additional';
import { create_calculation } from '~/api/route.calculation';
import { useStore } from '~/stores/stores.main';
import router from '~/router';

const step = ref(1);
const store = useStore();

const result = ref(null);

const form = reactive({
  industry: {
    input_type: 'suggestion',
    type: 'industry',
    value: '',
    chosen_id: null,
    route: get_industry_suggestion,
    suggestions: [],
  },

  district: {
    input_type: 'suggestion',
    type: 'district',
    value: '',
    chosen_id: null,
    route: get_district_suggestion,
    suggestions: [],
  },

  employee_amount: {
    input_type: 'simple',
    type: 'employee_amount',
    value: '',
  },

  equipment: [
    {
      input_type: 'suggestion',
      type: 'equipment',
      value: '',
      chosen_id: null,
      route: get_equipment_suggestion,
      suggestions: [],
      count: 1,
    },
  ],
  buildings: [
    {
      input_type: 'suggestion',
      type: 'buildings',
      value: '',
      chosen_id: null,
      route: get_building_suggestion,
      suggestions: [],
      count: 1,
    },
  ],

  building_area_size: {
    input_type: 'simple',
    type: 'building_area_size',
    value: '',
  },

  land_area_size: {
    input_type: 'simple',
    type: 'land_area_size',
    value: '',
  },

  predicted_income_per_year_rub: {
    input_type: 'simple',
    type: 'predicted_income_per_year_rub',
    value: '',
  },

  org_type: {
    input_type: 'org_type',
    type: 'org_type',
    value: '',
    chosen_id: null,
    route: get_equipment_suggestion,
    suggestions: [
      {
        name: 'ООО',
        id: 'OOO_AO',
      },
      {
        name: 'ИП',
        id: 'IP',
      },
    ],
    count: 1,
  },
  additional_needs: [
    {
      input_type: 'suggestion',
      type: 'additional_needs',
      value: '',
      chosen_id: null,
      route: () => [],
      suggestions: [],
      count: 1,
    },
  ],
  additional_services: [
    {
      input_type: 'suggestion',
      type: 'additional_services',
      value: '',
      chosen_id: null,
      route: get_additional_suggestion,
      suggestions: [],
      count: 1,
    },
  ],
});

const isValidStep = ref(false);

const validateMultiBlock = (block) => {
  if (block.value.length && block.chosen_id !== null) {
    return true;
  }
  return false;
};

const validateSimpleBlock = (block) => {
  if (block.value.length) {
    return true;
  }
  return false;
};

const validateMultiArrayBlock = (block) => {
  for (let i = 0; i < block.length; i++) {
    if (!block[i].value.length || block[i].value.chosen_id === null) {
      return false;
    }
  }
  return true;
};

const validate = (step) => {
  if (
    step === 1 &&
    (!validateMultiBlock(form.industry) ||
      !validateSimpleBlock(form.employee_amount) ||
      !validateSimpleBlock(form.land_area_size) ||
      !validateSimpleBlock(form.building_area_size))
  ) {
    return false;
  }
  if (
    step === 2 &&
    (!validateMultiArrayBlock(form.equipment) ||
      !validateMultiArrayBlock(form.buildings) ||
      !validateMultiBlock(form.org_type))
  ) {
    return false;
  }
  if (step === 3 && !validateSimpleBlock(form.predicted_income_per_year_rub)) {
    return false;
  }
  return true;
};

watch(form, () => {
  isValidStep.value = validate(step.value);
});

const next = () => {
  step.value += 1;
  isValidStep.value = validate(step.value);
};

const back = () => {
  step.value -= 1;
};

const getAllSuggestions = async () => {
  for (let key in form) {
    const block = form[key];
    if (Array.isArray(block)) {
      const data = [...(await block[0].route(block[0].value, 0, 100))];
      for (let i = 0; i < block.length; i++) {
        block[i].suggestions = data;
      }
      continue;
    }
    if (block.input_type === 'suggestion' && block.type !== 'org_type') {
      block.suggestions = [...(await block.route(block.value, 0, 100))];
    }
  }
};

const updateSuggestion = async (key, index) => {
  if (index >= 0) {
    const block = form[key][index];
    block.suggestions = [...(await block.route(block.value, 0, 100))];
    return;
  }
  const block = form[key];
  if (block.type !== 'org_type') {
    block.suggestions = [...(await block.route(block.value, 0, 100))];
  }
};

const setSuggestions = (suggestion, key, index) => {
  if (index >= 0) {
    return (form[key][index].chosen_id = suggestion.id);
  }
  form[key].chosen_id = suggestion.id;
};

const addMore = async (key, route) => {
  const block = form[key];
  const newItem = {
    input_type: 'suggestion',
    type: key,
    value: '',
    chosen_id: 0,
    route: route,
    suggestions: [...(await route('', 0, 100))],
    count: 1,
  };
  block.push(newItem);
  isValidStep.value = validate(step.value);
};

const deleteItem = (key, idx) => {
  if (form[key].length > 1) {
    form[key] = form[key].filter((item, itemIndex) => itemIndex !== idx);
  }
  isValidStep.value = validate(step.value);
};

const submit = async () => {
  const data = {
    industry_id: form.industry.chosen_id,
    district_id: form.district.chosen_id,
    employee_amount: +form.employee_amount.value,
    building_area_size: +form.building_area_size.value,
    land_area_size: +form.land_area_size.value,
    equipment: form.equipment.map((item) => {
      return {
        id: +item.chosen_id,
        amount: +item.count,
      };
    }),
    buildings: form.buildings.map((item) => {
      return {
        id: +item.chosen_id,
        area: +item.count,
      };
    }),
    additional_services: form.additional_services.map((item) => {
      return {
        id: +item.chosen_id,
      };
    }),

    legal_entity_type: form.org_type.chosen_id,
    accounting_services_documents_amount: +form.org_type.count,
    predicted_income_per_year_rub: +form.predicted_income_per_year_rub.value,
    additional_needs: form.additional_needs.map((item) => {
      if (item.value.length) {
        return {
          name: item.value,
          price: +item.count,
        };
      }
    }),
  };

  data.additional_needs = data.additional_needs.filter(item => item)

  const resultData = await create_calculation(
    { ...data },
    { token: store.$state.user.token }
  );
  result.value = { ...resultData };
  store.$state.result = { ...resultData };

  router.push('/review');
};

const isOpenedMap = ref(false);

const openMap = () => {
  isOpenedMap.value = true;
};

onMounted(async () => {
  await getAllSuggestions();
});
</script>

<template>
  <div class="home">
    <div v-if="isOpenedMap" class="modal">
      <div class="modal__content">
        <element-map class="map" />
      </div>
    </div>
    <div class="home-modal">
      <p class="home-modal__steps">{{ step }}/3 шаг</p>
      <h1 class="home-modal__title">
        Калькулятор для расчета возможных затрат
      </h1>
      <p class="home-modal__desc">Заполните все поля для расчета стоимости</p>
      <div class="home-modal__form">
        <div class="home-modal__step" v-show="step === 1">
          <div class="home-modal__block">
            <common-helpinput
              v-model="form.industry.value"
              class="home-modal__input"
              label="Отрасль ведения хозяйственной деятельности"
              :value="form.industry.value"
              :suggestions="form.industry.suggestions"
              @input="updateSuggestion('industry')"
              @set-item="(item) => setSuggestions(item, 'industry')"
            />
          </div>
          <div class="home-modal__block">
            <common-input
              v-model="form.employee_amount.value"
              :value="form.employee_amount.value"
              type="number"
              class="home-modal__input"
              label="Штатная численность сотрудников:"
            />
          </div>
          <div class="home-modal__block">
            <common-input
              v-model="form.land_area_size.value"
              :value="form.land_area_size.value"
              type="number"
              class="home-modal__input"
              label="Предполагаемая площадь земельного участка для расположения промышленного производства (в квадратных метрах)"
            />
          </div>
          <div class="home-modal__block">
            <common-input
              v-model="form.building_area_size.value"
              :value="form.building_area_size.value"
              type="number"
              class="home-modal__input"
              label="Планируемая площадь объектов капитального строительства"
            />
          </div>
        </div>

        <div class="home-modal__step" v-show="step === 2">
          <common-multiply-input
            label-main="Планируемый тип зданий/сооружений и их площади"
            label-count="Площадь, м2"
            suggestion-key="buildings"
            :block="form.buildings"
            @add="addMore"
            @delete="deleteItem"
            @update-suggestion="updateSuggestion"
            @set-suggestions="setSuggestions"
          />
          <common-multiply-input
            label-main="Предполагаемое к использованию оборудование (начните вводить и выберите из списка)"
            label-count="Количество, шт"
            suggestion-key="equipment"
            :block="form.equipment"
            @add="addMore"
            @delete="deleteItem"
            @update-suggestion="updateSuggestion"
            @set-suggestions="setSuggestions"
          />
          <div class="home-modal__block home-modal__block--fluid">
            <common-helpinput
              v-model="form.org_type.value"
              class="home-modal__input"
              label="Предоставление бухгалтерских услуг"
              :value="form.org_type.value"
              :suggestions="form.org_type.suggestions"
              @input="updateSuggestion('org_type')"
              @set-item="(item) => setSuggestions(item, 'org_type')"
            />
            <common-input
              v-model="form.org_type.count"
              :value="form.org_type.count"
              type="number"
              class="home-modal__input"
              label="Количество документов"
            />
          </div>
        </div>
        <div class="home-modal__step" v-show="step === 3">
          <div class="home-modal__block">
            <common-input
              v-model="form.predicted_income_per_year_rub.value"
              :value="form.predicted_income_per_year_rub.value"
              type="number"
              class="home-modal__input"
              label="Предполагаемый доход в год, руб"
            />
          </div>
          <!-- <div class="home-modal__block home-modal__block--fluid">
            <common-input
              value="Не выбран"
              class="home-modal__input"
              label="Округ"
              :view-only="true"
            />
            <common-button @click="openMap">Выбрать округ</common-button>
          </div> -->
          <div class="home-modal__block">
            <common-helpinput
              v-model="form.district.value"
              class="home-modal__input"
              label="Выбрать округ"
              :value="form.district.value"
              :suggestions="form.district.suggestions"
              @input="updateSuggestion('district')"
              @set-item="(item) => setSuggestions(item, 'district')"
            />
          </div>
          <div class="home-modal__block">
            <common-multiply-input
              :no-select="true"
              label-main="Пользовательские дополнительные услуги"
              label-count="Стоимость, руб."
              suggestion-key="additional_needs"
              :block="form.additional_needs"
              @add="addMore"
              @delete="deleteItem"
              @update-suggestion="updateSuggestion"
              @set-suggestions="setSuggestions"
            />
          </div>
          <div class="home-modal__block">
            <common-multiply-input
              label-main="Дополнительные услуги"
              label-count="Количество, шт"
              suggestion-key="additional_services"
              :block="form.additional_services"
              :input-only="true"
              @add="addMore"
              @delete="deleteItem"
              @update-suggestion="updateSuggestion"
              @set-suggestions="setSuggestions"
            />
          </div>
        </div>
      </div>
      <div class="home-modal__bottom">
        <common-button
          v-if="step !== 3"
          @click="next"
          :disabled="!isValidStep"
          class="home-modal__button"
        >
          Далее
        </common-button>
        <common-button
          v-else
          :disabled="!isValidStep"
          @click="submit"
          class="home-modal__button"
        >
          Отправить
        </common-button>
        <common-button
          variant="outlined"
          v-if="step !== 1"
          @click="back"
          class="home-modal__button"
        >
          Назад
        </common-button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.continent {
  fill: none;
  stroke: #5c443e;
  stroke-width: 3px;
  cursor: pointer;
  pointer-events: all;
}
.modal {
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.4);
  &__map {
    width: 100%;
    height: 100%;
  }
  &__content {
    background: #ffffff;
    padding: 20px;
  }
  z-index: 1000;
}
.home {
  display: flex;
  justify-content: center;
  align-items: center;
  @include md {
    padding: 0;
  }
  &-modal {
    max-width: 550px;
    width: 100%;
    margin: 0 auto;
    background-color: $primary-white;
    padding: 72px 40px;
    border-radius: 5px;
    text-align: center;
    position: relative;
    @include md {
      border-radius: 0;
    }
    &__actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }
    &__more {
      display: flex;
      align-items: center;
      @include create-font(14px, 500, 18px);
      color: $accent-purple;
      cursor: pointer;
      &-icon {
        margin-right: 8px;
        color: $accent-purple;
      }
      &:last-child {
        color: red;
        .home-modal__more-icon {
          color: red;
          transform: rotate(45deg);
        }
      }
    }
    @include md {
      padding: 50px 24px;
    }
    &__steps {
      @include create-font(20px, 600, 22px);
      color: $accent-purple;
      position: absolute;
      top: 20px;
      right: 20px;
    }
    &__button {
      width: 100%;
      &:not(:last-child) {
        margin-bottom: 24px;
      }
      @include md {
        &:hover {
          opacity: 1;
        }
      }
    }
    &__form {
      margin-bottom: 24px;
    }
    &__block {
      text-align: left;
      &--fluid {
        display: flex;
        align-items: flex-end;

        .home-modal__input:first-child {
          width: 175%;
          margin-right: 8px;
        }
        .home-modal__input:last-child {
          width: 70%;
        }
      }
      &:not(:last-child) {
        margin-bottom: 12px;
      }
      &-hint {
        @include create-font(14px, 400, 22px);
        margin-top: 6px;
      }
    }
    &__input {
      width: 100%;
    }
    &__title {
      @include create-font(26px, 600, 30px);
      margin-bottom: 30px;
      @include md {
        @include create-font(20px, 600, 30px);
        margin-bottom: 15px;
      }
    }
    &__desc {
      @include create-font(16px, 400, 22px);
      margin-bottom: 24px;
    }
    &__hint {
      @include create-font(16px, 400, 22px);
      color: $primary-grey;
      margin-bottom: 24px;
    }
  }
}
</style>
