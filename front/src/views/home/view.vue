<script setup>
import { reactive, ref } from 'vue';
import {
  CommonButton,
  CommonInput,
  CommonHelpinput,
} from '~/components/common';
import { get_equipment_suggestion } from '~/api/route.equipment';

const step = ref(1);

const next = () => {
  step.value += 1;
};

const back = () => {
  step.value -= 1;
};

const form = reactive({
  equipment: ''
})

const suggestions = ref([])

const inputEq = async () => {
  const res = await get_equipment_suggestion(form.equipment, 0, 100)
  suggestions.value = [...res]
};
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
              @input="inputEq"
              v-model="form.equipment"
              :value="form.equipment"
              :suggestions="suggestions"
              label="Предполагаемое к использованию оборудование;"
            />
          </div>
          <div class="home-modal__block">
            <common-input
              class="home-modal__input"
              label="Штатная численность сотрудников;"
            />
          </div>
          <div class="home-modal__block">
            <common-input
              class="home-modal__input"
              label="Территория расположения производства"
            />
          </div>
          <div class="home-modal__block">
            <common-input
              class="home-modal__input"
              label="Предполагаемая площадь земельного участка для расположения промышленного производства (в квадратных метрах);"
            />
          </div>
        </div>
        <div class="home-modal__step" v-show="step === 2">
          <div class="home-modal__block">
            <common-input
              class="home-modal__input"
              label="Планируемая площадь объектов капитального строительства;"
            />
          </div>
          <div class="home-modal__block">
            <common-input
              class="home-modal__input"
              label="Предполагаемое к использованию оборудование;"
            />
          </div>
          <div class="home-modal__block">
            <common-input
              class="home-modal__input"
              label="Планируемый тип зданий/сооружений и их площади;"
            />
          </div>
          <div class="home-modal__block">
            <common-input
              class="home-modal__input"
              label="Предоставление бухгалтерских услуг;"
            />
          </div>
        </div>
        <div class="home-modal__step" v-show="step === 3">
          <div class="home-modal__block">
            <common-input
              class="home-modal__input"
              label="Отрасль ведения хозяйственной деятельности;"
            />
          </div>
          <div class="home-modal__block">
            <common-input
              class="home-modal__input"
              label="Иные потребности (подключение к сетям инженерно-технического обеспечения и другие)."
            />
          </div>
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
    padding: 72px 100px;
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
