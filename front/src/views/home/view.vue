<script setup>
import { reactive, ref, onMounted } from 'vue';
import {
  CommonButton,
  CommonInput,
  CommonHelpinput,
} from '~/components/common';
import { get_equipment_suggestion } from '~/api/route.equipment';

const step = ref(2);

const next = () => {
  step.value += 1;
};

const back = () => {
  step.value -= 1;
};

const form = reactive({
  industry: {
    input_type: 'suggestion',
    type: 'industry',
    value: '',
    chosen_id: 0,
    route: get_equipment_suggestion,
    suggestions: [],
  },

  employee_amount: {
    input_type: 'simple',
    type: 'employee_amount',
    value: '',
  },

  equipment: {
    input_type: 'suggestion',
    type: 'equipment',
    value: '',
    chosen_id: 0,
    route: get_equipment_suggestion,
    suggestions: [],
    count: 1
  },

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

  buildings: {
    input_type: 'suggestion',
    type: 'buildings',
    value: '',
    chosen_id: 0,
    route: get_equipment_suggestion,
    suggestions: [],
  },

  org_type: {
    input_type: 'org_type',
    type: 'org_type',
    value: '',
    chosen_id: 0,
    route: get_equipment_suggestion,
    suggestions: [],
    count: 1
  },
});

const suggestions = ref([]);

const getAllSuggestions = async () => {
  for (let key in form) {
    const block = form[key];
    if (block.input_type === 'suggestion') {
      block.suggestions = [...(await block.route(block.value, 0, 100))];
    }
  }
};

const updateSuggestion = async (key) => {
  const block = form[key]
  block.suggestions = [...(await block.route(block.value, 0, 100))]
};

const setSuggestions = (suggestion, key) => {
  form[key].chosen_id = suggestion.id
}

onMounted(async () => {
  await getAllSuggestions();
});
</script>

<template>
  <div class="home">
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
              class="home-modal__input"
              label="Штатная численность сотрудников:"
            />
          </div>
          <div class="home-modal__block">
            <common-input
              v-model="form.building_area_size.value"
              :value="form.building_area_size.value"
              class="home-modal__input"
              label="Предполагаемая площадь земельного участка для расположения промышленного производства (в квадратных метрах)"
            />
          </div>
          <div class="home-modal__block">
            <common-input
              v-model="form.land_area_size.value"
              :value="form.land_area_size.value"
              class="home-modal__input"
              label="Планируемая площадь объектов капитального строительства"
            />
          </div>
        </div>

        <div class="home-modal__step" v-show="step === 2">
          <div class="home-modal__block home-modal__block--fluid">
            <common-helpinput
              v-model="form.equipment.value"
              class="home-modal__input"
              label="Предполагаемое к использованию оборудование (начните вводить и выберите из списка)"
              :value="form.equipment.value"
              :suggestions="form.equipment.suggestions"
              @input="updateSuggestion('equipment')"
              @set-item="(item) => setSuggestions(item, 'equipment')"
            />
            <common-input
              v-model="form.equipment.count"
              :value="form.equipment.count"
              class="home-modal__input"
              label="Количество, шт (введите число)"
            />
          </div>
          <div class="home-modal__block">
            <common-helpinput
              v-model="form.buildings.value"
              class="home-modal__input"
              label="Планируемый тип зданий/сооружений и их площади;"
              :value="form.buildings.value"
              :suggestions="form.buildings.suggestions"
              @input="updateSuggestion('buildings')"
              @set-item="(item) => setSuggestions(item, 'buildings')"
            />
          </div>
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
              class="home-modal__input"
              label="Количество документов"
            />
          </div>
        </div>
        <div class="home-modal__step" v-show="step === 3">
        </div>
      </div>
      <div class="home-modal__bottom">
        <common-button @click="next" class="home-modal__button">
          Далее
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
