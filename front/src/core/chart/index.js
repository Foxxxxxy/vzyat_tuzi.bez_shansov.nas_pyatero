import moment from 'moment'
import {
  formatDate
} from '~/core/time'

export const normalizePrice = (num) => num.toLocaleString('ru-RU')
/**
 * Генерация настроек для графиков
 * @param {('price'|'order'|'order-count')} tooltipType
 */
export function normalizeWords(n, texts) {
  n = Math.abs(n) % 100
  const n1 = n % 10
  if (n > 10 && n < 20) return texts[2]
  else if (n1 > 1 && n1 < 5) return texts[1]
  else if (n1 == 1) return texts[0]
  return texts[2]
}

export const getOptions = (tooltipType) => {
  const options = {
    scales: {
      xAxes: [
        {
          gridLines: {
            zeroLineColor: 'transparent',
            color: '#DFDFDF',
            borderDash: [10, 10],
          },
          ticks: {
            stepSize: 1,
            fontColor: '#8C9AAB',
            fontFamily: 'Inter',
          },
        },
      ],
      yAxes: [
        {
          gridLines: {
            zeroLineColor: 'transparent',
            color: '#DFDFDF',
            borderDash: [10, 10],
          },
          ticks: {
            fontColor: '#8C9AAB',
            fontFamily: 'Inter',
          },
        },
      ],
    },
    legend: {
      display: false,
    },
    elements: {
      point: {
        radius: 5,
        backgroundColor: '#ffffff',
        borderWidth: 4,
        hitRadius: 5,
        hoverRadius: 6,
        hoverBorderWidth: 5,
      },
      line: {
        tension: 0.4, // изгиб линии
        fill: false,
      },
    },
    animation: {
      easing: 'easeOutCubic',
    },
    responsive: true,
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: '#ffffff',
      displayColors: false,
      titleFontColor: '#8C9AAB',
      titleFontFamily: 'Inter',
      titleFontSize: 13,
      bodyFontColor: '#000',
      bodyFontStyle: 'bold',
      bodyFontFamily: 'Inter',
      bodyFontSize: 16,
      xPadding: 16,
      yPadding: 8,
    },
  }
  if (tooltipType === 'price') {
    options.tooltips.callbacks = {
      label: (tooltipItem) => {
        return `${normalizePrice(Math.round(tooltipItem.yLabel * 100) / 100)} ₽`
      },
    }
  } else if (tooltipType === 'order') {
    options.tooltips.callbacks = {
      label: (tooltipItem) => {
        const name =
          tooltipItem.datasetIndex === 0
            ? 'успешных заказов'
            : 'провалено заказов'
        return `${normalizePrice(
          Math.round(tooltipItem.yLabel * 100) / 100
        )} ${name}`
      },
    }
  } else if (tooltipType === 'order-count') {
    options.tooltips.callbacks = {
      label: (tooltipItem) => {
        const value = Math.round(tooltipItem.yLabel * 100) / 100
        return `${normalizePrice(value)} ${normalizeWords(value, [
          'заказ',
          'заказа',
          'заказов',
        ])}`
      },
    }
  }
  return options
}

const normalizeISO = (iso) => {
  return `${iso.split('T')[0]}T00:00:00.000Z`
}

export const getStats = async (token, type, byCount, divided_stats = false) => {
  let from, to
  const currentDate = moment()
  // На неделю
  if (type === 0) {
    // День - 1
    from = currentDate.clone().subtract(1, 'days')
    to = currentDate.add(20, 'hours')
  } else if (type === 1) {
    // 3 Дня
    from = currentDate.clone().subtract(1, 'days')
    to = currentDate.add(1, 'days')
  } else if (type === 2) {
    // Текущая неделя
    const startOfWeek = currentDate.clone().startOf('isoWeek')
    from = startOfWeek.clone().add(1, 'days')
    to = startOfWeek.add(7, 'days')
  } else if (type === 3) {
    // Текущий месяц
    const startOfMonth = currentDate.clone().startOf('month')
    from = startOfMonth.clone().add(1, 'days')
    to = startOfMonth.endOf('month')
  } else if (type === 4) {
    // Текущий год
    const startOfYear = currentDate.clone().startOf('year')
    from = startOfYear.clone().add(1, 'days')
    to = startOfYear.endOf('year')
    // ачё куда течёт?
  }

  const ok = false
  const data = []

  const formatToMonth = (date) =>
    formatDate(date, { day: '2-digit', month: 'short' })
  const formatToYear = (date) => formatDate(date, { month: 'long' })

  if (ok) {
    const labels = data.times.map((date) => {
      const parsed = new Date(Date.parse(date))
      return type === 4 ? formatToYear(parsed) : formatToMonth(parsed)
    })
    const defaultBody = {
      labels,
      average_check: data.average_check,
      total_amount: data.total_amount,
      total_count: data.total_count,
    }
    if (divided_stats) {
      return {
        realized: data.res_realized,
        not_realized: data.res_not_realized,
        ...defaultBody,
      }
    }
    return {
      data: data.res,
      ...defaultBody,
    }
  }
  return {
    data: [],
    labels: [],
    average_check: 0,
    total_amount: 0,
    total_count: 0,
  }
}
