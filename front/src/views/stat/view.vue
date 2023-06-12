<script setup>
import { CommonButton } from '~/components/common';
import { ElementChartline } from '~/components/elements';
import { getOptions } from '~/core/chart'
import { reactive } from 'vue';
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const chartdata = reactive({
        labels: [ 'January', 'February', 'March'],
        datasets: [
          {
            label: 'Data One',
            backgroundColor: '#3CD0EE',
            data: [10, 3, 1]
          }
        ]
      });


const options = reactive(getOptions('price'),)
</script>

<template>
  <div class="statistics">
    <div class="block">
      <div class="block__head">
        <header class="statistics__header">
          <h1 class="statistics__title">Статистика</h1>
        </header>
      </div>
      <div class="block__content">
        <div class="date">
          <h1 class="date__h1">10 мая - 17 мая</h1>
          <div class="block__space" />
          <common-button>Неделя</common-button>
          <div class="block__divider" />
          <common-button variant="outlined"> Месяц </common-button>
          <div class="block__divider" />
          <common-button variant="outlined"> Год </common-button>
        </div>
        <div class="stats stats-mb24 stats-mt-12">
          <div class="stats__item stats__item-fullborder">
            <p class="stats__amount stats__amount-dark">
              400
            </p>
            <p class="stats__desc stats__desc-mt4">Общее число посетителей</p>
          </div>
          <div class="stats__item stats__item-fullborder">
            <p class="stats__amount stats__amount-dark">100</p>
            <p class="stats__desc stats__desc-mt4">Кол-во отправленных заявок</p>
          </div>
          <div class="stats__item stats__item-fullborder">
            <p class="stats__amount stats__amount-dark">
              15+
            </p>
            <p class="stats__desc stats__desc-mt4">Средний возраст пользователей</p>
          </div>
        </div>

        <Bar ref="chartRef"
          :chartData="chartdata"
          :options="options" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.stats {
  $border: 1px solid #eeeeee;
  display: flex;
  margin-top: 32px;
  border-top: $border;
  &-mb24 {
    margin-bottom: 24px;
  }
  &__item {
    width: 100%;
    border-right: $border;
    padding: 32px 0 32px 16px;
    &:last-child {
      border-right: none;
    }
    &-fullborder {
      border-bottom: $border;
    }
  }
  &__amount {
    font-size: 26px;
    font-weight: 600;
    line-height: 23px;
    letter-spacing: normal;
    color: $accent-purple;
    &-dark {
      color: #1d1d1b;
    }
    &-red {
      color: #fb5449;
    }
  }
  &__desc {
    font-size: 16px;
    font-weight: 500;
    line-height: 20px;
    letter-spacing: normal;
    color: $primary-grey;
    &-mt4 {
      margin-top: 4px;
    }
  }
  &__symbol {
    color: $accent-purple;
  }
}
.stats {
  &-mt-12 {
    margin-top: 12px;
  }
}
.date {
  margin-top: 22px;
  padding: 0 32px;
  color: #8c9aab;
  display: flex;
  align-items: center;
}
.statistics {
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

.block {
  background-color: #ffffff;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.03);
  border-radius: 5px;
  &__divider {
    width: 16px;
  }
  &__space {
    flex-grow: 1;
  }
  &--empty {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
  }
  &__content {
    margin-top: 30px;
    &-padding {
      padding-bottom: 1px;
      margin-bottom: 24px;
    }
  }
}
</style>
