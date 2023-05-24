<script setup>
import { CommonPopup, CommonButton, CommonInput } from '~/components/common';

defineProps({
  result: [Object, null],
});
</script>

<template>
  <div class="result">
    <div class="result__content">
      <header class="result__header">
        <h1 class="result__title">Предпросмотр отчета</h1>
      </header>
      <div class="result__wrapper">
          <div class="result__block">
            <common-input
              label="Количество бухгалтерских документов"
              class="result__input"
              :value="result.accounting_services_documents_amount"
              :view-only="true"
            />
          </div>
          <!-- <div class="result__block">
            <common-input
              label="Расходы на бухгалтерские документы"
              class="result__input"
              :value="result.accounting_services_expenses"
              :view-only="true"
            />
          </div> -->
          <div class="result__block">
            <common-input
              label="Планируемая площадь объектов капитального строительства"
              class="result__input"
              :value="result.building_area_size"
              :view-only="true"
            />
          </div>
          <div class="result__block">
            <common-input
              label="Московский округ"
              class="result__input"
              :value="result.district"
              :view-only="true"
            />
          </div>
          <div class="result__block">
            <common-input
              label="Штатная численность сотрудников"
              class="result__input"
              :value="result.employee_amount"
              :view-only="true"
            />
          </div>
          <div class="result__block">
            <common-input
              label="Отрасль ведения хозяйственной деятельности"
              class="result__input"
              :value="result.industry_name"
              :view-only="true"
            />
          </div>
          <div class="result__block">
            <common-input
              label="Предполагаемая площадь земельного участка для расположения промышленного производства"
              class="result__input"
              :value="result.land_area_size"
              :view-only="true"
            />
          </div>
          <!-- <div class="result__block">
            <common-input
              label="Предполагаемый доход в год, руб"
              class="result__input"
              :value="result.total_rent_expenses"
              :view-only="true"
            />
          </div> -->
          <!-- <div class="result__block">
            <common-input
              label="Расходы на персонал"
              class="result__input"
              :value="result.total_employee_expenses"
              :view-only="true"
            />
          </div> -->
          <!-- <div class="result__block">
            <common-input
              label="Расходы на оборудование"
              class="result__input"
              :value="result.total_equipments_expenses"
              :view-only="true"
            />
          </div> -->
          <!-- <div class="result__block">
            <common-input
              label="Итого"
              class="result__input"
              :value="result.total_expenses"
              :view-only="true"
            />
          </div> -->
          <!-- <div class="result__block">
            <common-input
              label="Общие расходы на аренду"
              class="result__input"
              :value="result.total_rent_expenses"
              :view-only="true"
            />
          </div> -->
          <!-- <div class="result__block">
            <common-input
              label="Общие расходы по налогам"
              class="result__input"
              :value="result.total_taxes_expenses"
              :view-only="true"
            />
          </div> -->
      </div>
      <div class="result__main">
        <div class="result__main-block">
          <p class="result__main-title">Расходы на бухгалтерские документы:</p>
          <p class="result__main-value">{{ result.accounting_services_expenses }} руб.</p>
        </div>
        <div class="result__main-block">
          <p class="result__main-title">Предполагаемый доход в год, руб:</p>
          <p class="result__main-value">{{ result.predicted_income_per_year_rub }} руб.</p>
        </div>
        <div class="result__main-block">
          <p class="result__main-title">Расходы на персонал</p>
          <p class="result__main-value">{{ result.total_employee_expenses }} руб.</p>
        </div>
        <div class="result__main-block">
          <p class="result__main-title">Расходы на оборудование:</p>
          <p class="result__main-value">{{ result.total_equipments_expenses }} руб.</p>
        </div>
        <div class="result__main-block">
          <p class="result__main-title">Общие расходы на аренду:</p>
          <p class="result__main-value">{{ result.total_rent_expenses }} руб.</p>
        </div>
        <div class="result__main-block">
          <p class="result__main-title">Общие расходы по налогам:</p>
          <p class="result__main-value">{{ result.total_taxes_expenses }} руб.</p>
        </div>
        <div class="result__main-block result__main-block--multiply" v-if="result.equipments && result.equipments.length">
          <p class="result__main-title">Оборудование:</p>
          <div class="result__main-block">
            <p class="result__main-subtitle">Количество:</p>
            <p class="result__main-value">{{ result.equipments[0].amount }} шт.</p>
          </div>
          <div class="result__main-block">
            <p class="result__main-subtitle">Общие расходы на оборудование:</p>
            <p class="result__main-value">{{ result.equipments[0].total_expenses }} руб.</p>
          </div>
          <div class="result__main-list" v-for="(item, idx) of result.equipments" :key="idx">
            <div class="result__main-item">
              <p class="result__main-subtitle result__main-subtitle--gray">Наименование:</p>
              <p class="result__main-value">{{ item.equipment.name }}</p>
            </div>
            <div class="result__main-item">
              <p class="result__main-subtitle result__main-subtitle--gray">Средняя стоимость доллара:</p>
              <p class="result__main-value">{{ item.equipment.average_price_dollar }} $</p>
            </div>
          </div>
        </div>
        <div class="result__main-block">
          <p class="result__main-title result__main-title--big">Итого:</p>
          <p class="result__main-value result__main-value--big">{{ result.total_expenses }} руб.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.result {
  width: 100%;
  height: 100%;
  background-color: #ffffff;
  margin-bottom: 200px;
  &__main {
    padding: 20px;
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
          margin-bottom: 10px;
        }
      }
    }
  }
  &__content {
    background-color: #ffffff;
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
    padding: 41px 32px 41px 0;
  }
  &__form {
    padding: 0 32px;
    max-width: 500px;
  }
  &__block {
    border-bottom: 1px solid #d8d8d8;
    padding: 0 0 15px 10px;
    &:not(:last-child) {
      // margin-bottom: 12px;
    }
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
