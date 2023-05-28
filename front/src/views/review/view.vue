<script setup>
import { computed, onMounted, ref } from 'vue';
import { CommonPopup, CommonButton, CommonInput } from '~/components/common';
import { useStore } from '~/stores/stores.main';
import { download_pdf, download_detailed_pdf } from '~/api/route.calculation';

const store = useStore();
const isLoggedIn = computed(() => !!store.$state.user.token);

const windowInner = ref(window.innerWidth);

const result = computed(() => store.$state.result);

const download = () => {
  download_pdf(result.value.request_id, store.$state.user.token);
};

const downloadDetailed = () => {
  download_detailed_pdf(result.value.request_id, store.$state.user.token);
};

const returnLegal = (legal) => {
  if (legal === 'OOO_AO') {
    return 'ООО';
  }
  return 'ИП';
};

onMounted(() => {
  window.addEventListener('resize', (e) => {
    windowInner.value = window.innerWidth;
  });
});
</script>

<template>
  <div class="result">
    <div class="result__content" v-if="result">
      <header class="result__header">
        <h1 class="result__title">Предпросмотр отчета</h1>
        <div class="result__buttons">
          <common-button
            v-if="isLoggedIn"
            @click="download"
            variant="outlined"
            class="result__button"
            >СКАЧАТЬ ОТЧЕТ</common-button
          >
          <router-link to="/auth?back=review" v-else>
            <common-button variant="outlined" class="result__button"
              >Войдите, чтобы скачать отчет</common-button
            >
          </router-link>
          <common-button
            v-if="isLoggedIn"
            @click="downloadDetailed"
            variant="outlined"
            class="result__button"
            >СКАЧАТЬ ПОДРОБНЫЙ ОТЧЕТ</common-button
          >
        </div>
      </header>
      <main class="result__main">
        <div class="result__section">
          <div class="result__subtitle">Бухгалтерский учет</div>
          <div class="result__grid">
            <div class="result__grid-wrapper">
              <div class="result__row">
                <div class="result__column">
                  <p class="result__grid-title">Количество документов</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Расходы</p>
                </div>
              </div>
              <div class="result__row">
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ result.accounting_services_documents_amount }} шт.
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ result.accounting_services_expenses }} руб.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <p class="result__section-sum">
            Итого расходы:
            <span class="result__section-sumval"
              >{{ result.accounting_services_expenses }} руб.</span
            >
          </p>
        </div>
        <div class="result__section">
          <div class="result__subtitle">Налогообложение</div>
          <div class="result__grid">
            <div class="result__grid-wrapper">
              <div class="result__row result__row--4">
                <div class="result__column">
                  <p class="result__grid-title">Предполагаемый доход в год</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Налог</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">
                    Предоставление бухгалтерских услуг
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Отрасль</p>
                </div>
              </div>
              <div class="result__row result__row--4">
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ result.predicted_income_per_year_rub }} руб.
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ result.total_taxes_expenses }} руб.
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ returnLegal(result.legal_entity_type) }}
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ result.industry_name }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          <p class="result__section-sum">
            Итого расходы:
            <span class="result__section-sumval"
              >{{ result.total_taxes_expenses }} руб.</span
            >
          </p>
        </div>
        <div class="result__section">
          <div class="result__subtitle">Персонал</div>
          <div class="result__grid">
            <div class="result__grid-wrapper">
              <div class="result__row">
                <div class="result__column">
                  <p class="result__grid-title">Количество работников</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Расходы</p>
                </div>
              </div>
              <div class="result__row">
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ result.employee_amount }} чел.
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ result.total_employee_expenses }} руб.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <p class="result__section-sum">
            Итого расходы:
            <span class="result__section-sumval"
              >{{ result.total_employee_expenses }} руб.</span
            >
          </p>
        </div>
        <div class="result__section">
          <div class="result__subtitle">Территория</div>
          <div class="result__grid">
            <div class="result__grid-wrapper">
              <div class="result__row result__row--4">
                <div class="result__column">
                  <p class="result__grid-title">Округ</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Площадь земельного участка</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">
                    Площадь объектов капитального строительства
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Стоимость</p>
                </div>
              </div>
              <div class="result__row result__row--4">
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ result.district }}
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ result.land_area_size }} м2.
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ result.building_area_size }} м2.
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ result.total_rent_expenses }} руб.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <p class="result__section-sum">
            Итого расходы:
            <span class="result__section-sumval"
              >{{ result.total_rent_expenses }} руб.</span
            >
          </p>
        </div>
        <div class="result__section">
          <div class="result__subtitle">Здания</div>
          <div class="result__grid" v-if="windowInner > 768">
            <div class="result__grid-wrapper">
              <div class="result__row result__row--4">
                <div class="result__column">
                  <p class="result__grid-title">Тип</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Средняя стоимость</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Площадь</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Стоимость</p>
                </div>
              </div>
              <div
                v-for="(item, index) of result.buildings"
                :key="index"
                class="result__row result__row--4"
              >
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.building.name }}
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.building.average_price_rub }} руб.
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">{{ item.area }} м2</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.total_expenses }} руб.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="result__grid" v-else>
            <div
              class="result__grid-wrapper"
              v-for="(item, index) of result.buildings"
              :key="index"
            >
              <div class="result__row result__row--4">
                <div class="result__column">
                  <p class="result__grid-title">Тип</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Средняя стоимость</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Площадь</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Стоимость</p>
                </div>
              </div>
              <div class="result__row result__row--4">
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.building.name }}
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.building.average_price_rub }} руб.
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">{{ item.area }} м2</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.total_expenses }} руб.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <p class="result__section-sum">
            Итого расходы:
            <span class="result__section-sumval"
              >{{ result.total_buildings_expenses }} руб.</span
            >
          </p>
        </div>
        <div class="result__section">
          <div class="result__subtitle">Оборудование</div>
          <div class="result__grid" v-if="windowInner > 768">
            <div class="result__grid-wrapper">
              <div class="result__row result__row--4">
                <div class="result__column">
                  <p class="result__grid-title">Тип</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Средняя стоимость</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Количество</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Стоимость</p>
                </div>
              </div>
              <div
                v-for="(item, index) of result.equipments"
                :key="index"
                class="result__row result__row--4"
              >
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.equipment.name }}
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.equipment.average_price_dollar }} $
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">{{ item.amount }} шт.</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.total_expenses }} руб.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="result__grid">
            <div
              class="result__grid-wrapper"
              v-for="(item, index) of result.equipments"
              :key="index"
            >
              <div class="result__row result__row--4">
                <div class="result__column">
                  <p class="result__grid-title">Тип</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Средняя стоимость</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Количество</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Стоимость</p>
                </div>
              </div>
              <div class="result__row result__row--4">
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.equipment.name }}
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.equipment.average_price_dollar }} $
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">{{ item.amount }} шт.</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.total_expenses }} руб.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <p class="result__section-sum">
            Итого расходы:
            <span class="result__section-sumval"
              >{{ result.total_equipments_expenses }} руб.</span
            >
          </p>
        </div>
        <div class="result__section">
          <div class="result__subtitle">Дополнительные услуги</div>
          <div class="result__grid" v-if="windowInner > 768">
            <div class="result__grid-wrapper">
              <div class="result__row">
                <div class="result__column">
                  <p class="result__grid-title">Тип</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Стоимость</p>
                </div>
              </div>
              <div
                class="result__row"
                v-for="(item, index) of result.additional_services"
                :key="index"
              >
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.additional_service.name }}
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.total_expenses }} руб.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="result__grid" v-else>
            <div
              class="result__grid-wrapper"
              v-for="(item, index) of result.additional_services"
              :key="index"
            >
              <div class="result__row">
                <div class="result__column">
                  <p class="result__grid-title">Тип</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Стоимость</p>
                </div>
              </div>
              <div class="result__row">
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.additional_service.name }}
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.total_expenses }} руб.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <p class="result__section-sum">
            Итого расходы:
            <span class="result__section-sumval"
              >{{ result.total_additional_services_expenses }} руб.</span
            >
          </p>
        </div>
        <div class="result__section">
          <div class="result__subtitle">Дополнительные пользовательские услуги</div>
          <div class="result__grid" v-if="windowInner > 768">
            <div class="result__grid-wrapper">
              <div class="result__row">
                <div class="result__column">
                  <p class="result__grid-title">Тип</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Стоимость</p>
                </div>
              </div>
              <div
                class="result__row"
                v-for="(item, index) of result.additional_needs"
                :key="index"
              >
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.name }}
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.price }} руб.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="result__grid" v-else>
            <div
              class="result__grid-wrapper"
              v-for="(item, index) of result.additional_needs"
              :key="index"
            >
              <div class="result__row">
                <div class="result__column">
                  <p class="result__grid-title">Тип</p>
                </div>
                <div class="result__column">
                  <p class="result__grid-title">Стоимость</p>
                </div>
              </div>
              <div class="result__row">
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.name }}
                  </p>
                </div>
                <div class="result__column">
                  <p class="result__grid-value">
                    {{ item.price }} руб.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <p class="result__section-sum">
            Итого расходы:
            <span class="result__section-sumval"
              >{{ result.total_additional_needs_expenses }} руб.</span
            >
          </p>
        </div>
        <div class="result__bottom">
          <div class="result__main-block">
            <p class="result__main-title">Бухгалтерский учет:</p>
            <p class="result__main-value">
              {{ result.accounting_services_expenses }} руб.
            </p>
          </div>
          <div class="result__main-block">
            <p class="result__main-title">Налогообложение:</p>
            <p class="result__main-value">
              {{ result.total_taxes_expenses }} руб.
            </p>
          </div>
          <div class="result__main-block">
            <p class="result__main-title">Оборудование:</p>
            <p class="result__main-value">
              {{ result.total_equipments_expenses }} руб.
            </p>
          </div>
          <div class="result__main-block">
            <p class="result__main-title">Здания:</p>
            <p class="result__main-value">
              {{ result.total_buildings_expenses }} руб.
            </p>
          </div>
          <div class="result__main-block">
            <p class="result__main-title">Персонал:</p>
            <p class="result__main-value">
              {{ result.total_employee_expenses }} руб.
            </p>
          </div>
          <div class="result__main-block">
            <p class="result__main-title">Дополнительные услуги:</p>
            <p class="result__main-value">
              {{ result.total_additional_services_expenses }} руб.
            </p>
          </div>
          <div class="result__main-block">
            <p class="result__main-title">Территория:</p>
            <p class="result__main-value">
              {{ result.total_rent_expenses }} руб.
            </p>
          </div>
          <div class="result__main-block">
            <p class="result__main-title result__main-title--big">
              ОБЩИЙ ИТОГ:
            </p>
            <p class="result__main-value result__main-value--big">
              {{ result.total_expenses }} руб.
            </p>
          </div>
        </div>
      </main>
    </div>
    <div class="result__content result__content--empty" v-else>
      <router-link to="/">
        <common-button>Создать новый отчет</common-button>
      </router-link>
    </div>
  </div>
</template>

<style scoped lang="scss">
.result {
  width: 100%;
  height: 100%;
  background-color: #ffffff;
  margin-bottom: 10000px;
  &__bottom {
    padding: 20px;
  }
  &__section {
    border-bottom: 1px dashed $accent-purple;
    padding-bottom: 11px;
    &-sum {
      @include create-font(22px, 600, normal);
      padding-left: 20px;
      padding-top: 10px;
    }
    &-sumval {
      margin-left: 10px;
      @include create-font(16px, 600, normal);
      color: $accent-purple;
    }
  }
  &__grid {
    display: grid;
    &-wrapper {
      display: grid;
      grid-template-rows: 1fr 1fr;
      gap: 8px;
      border-bottom: 1px dashed #d8d8d8;
      padding-bottom: 10px;
      @include md {
        grid-template-columns: 1fr 1fr;
        grid-template-rows: none;
      }
    }
    &-title {
      @include create-font(18px, 500, normal);
      color: #8c9aab;
    }
    &-value {
      @include create-font(16px, 600, normal);
    }
  }
  &__row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    padding-left: 20px;
    &--4 {
      grid-template-columns: repeat(4, 1fr);
    }
    @include md {
      grid-template-columns: none;
      align-items: flex-end;
      gap: 10px;
    }
  }
  &__subtitle {
    @include create-font(20px, 600, normal);
    padding: 20px 0 20px 20px;
    border-bottom: 1px dashed #d8d8d8;
    margin-bottom: 10px;
  }
  &__main {
    // padding: 20px;
    &-list {
      position: relative;
      padding-left: 50px;
      &:not(:last-child) {
        margin-bottom: 20px;
      }
    }
    &-subtitle {
      margin-right: 18px;
      font-weight: 700;
      &--gray {
        color: #a8a8a8;
      }
    }
    &-item {
      display: flex;
      &:not(:last-child) {
        margin-bottom: 10px;
      }
      &::before {
        content: '';
        width: 5px;
        height: 5px;
        background-color: #454545;
        border-radius: 50%;
        position: absolute;
        left: 33px;
        // top: 5px;
      }
    }
    &-title {
      font-weight: bold;
      font-size: 18px;
      margin-right: 20px;
      color: #454545;
      &--big {
        font-size: 30px;
      }
    }
    &-value {
      &--big {
        font-size: 20px;
      }
    }
    &-block {
      display: flex;
      align-items: baseline;
      margin-bottom: 20px;
      &--multiply {
        flex-direction: column;
        .result__main-block {
          margin-bottom: 10px;
          padding-left: 20px;
        }
        .result__main-title {
          margin-bottom: 20px;
        }
      }
    }
  }
  &__content {
    background-color: #ffffff;
    &--empty {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
    }
  }
  &__wrapper {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px 0;
    padding: 20px;
  }
  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    align-items: center;
    padding: 41px 32px 41px 0;
    @include md {
      flex-direction: column;
      align-items: flex-start;
    }
  }
  &__form {
    padding: 0 32px;
    max-width: 500px;
  }
  &__block {
    border-bottom: 1px solid #d8d8d8;
    padding: 0 0 15px 10px;
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
  &__buttons {
    flex-direction: column;
  }
  &__button {
    width: 100%;
    &:not(:last-child) {
      margin-bottom: 10px;
    }
    @include md {
      margin-left: 10px;
    }
  }
}
</style>
