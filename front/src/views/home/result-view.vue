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
        <div class="result__form">
          <div class="result__block">
            <common-input
              label="Количество бухгалтерских документов"
              class="result__input"
              :value="result.accounting_services_documents_amount"
              :view-only="true"
            />
          </div>
          <div class="result__block">
            <common-input
              label="Расходы на бухгалтерские документы"
              class="result__input"
              :value="result.accounting_services_expenses"
              :view-only="true"
            />
          </div>
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
        </div>
        <div class="result__form">
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
          <div class="result__block">
            <common-input
              label="Предполагаемый доход в год, руб"
              class="result__input"
              :value="result.predicted_income_per_year_rub"
              :view-only="true"
            />
          </div>

          <div class="result__block">
            <common-input
              label="Расходы на персонал"
              class="result__input"
              :value="result.total_employee_expenses"
              :view-only="true"
            />
          </div>
          <div class="result__block">
            <common-input
              label="Расходы на оборудование"
              class="result__input"
              :value="result.total_equipments_expenses"
              :view-only="true"
            />
          </div>
          <div class="result__block">
            <common-input
              label="Итого"
              class="result__input"
              :value="result.total_expenses"
              :view-only="true"
            />
          </div>
          <div class="result__block">
            <common-input
              label="Общие расходы на аренду"
              class="result__input"
              :value="result.total_rent_expenses"
              :view-only="true"
            />
          </div>
          <div class="result__block">
            <common-input
              label="Общие расходы по налогам"
              class="result__input"
              :value="result.total_taxes_expenses"
              :view-only="true"
            />
          </div>
          <div class="result__block">
            <common-input
              label="Фамилия"
              class="result__input"
              :view-only="true"
            />
          </div>
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
  &__content {
    background-color: #ffffff;
  }
  &__wrapper {
    display: grid;
    grid-template-columns: 1fr 1fr;
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
    &:not(:last-child) {
      margin-bottom: 12px;
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
