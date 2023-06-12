function range(start, end, rangeArray = []) {
  if (start >= end) return rangeArray
  rangeArray.push(++start)
  return range(start, end, rangeArray)
}

export const getHours = () => {
  const rangeArray = range(-1, 23),
    r = {}
  rangeArray.forEach(
    (n) => (r[n] = timeToString('', (n + '').padStart(2, '0')))
  )
  return r
}

export const getMinutes = () => {
  const rangeArray = [],
    r = {}
  for (let i = 0; i < 60; i += 5) {
    rangeArray.push(i)
  }
  rangeArray.forEach(
    (n) => (r[n] = timeToString('', (n + '').padStart(2, '0')))
  )
  return r
}

/**
 * Удаляет время у даты
 * @param {Date} date
 * @returns {Date}
 */
export const normalizeDate = (date) => {
  const normalizedDate = new Date(
    date.getFullYear(),
    date.getMonth(),
    date.getDate()
  )
  return normalizedDate
}

/**
 * 8 -> 8:00
 * @param {number} time
 * @param {number} minute
 * @returns
 */
export const timeToString = (time, minute) => {
  return minute ? `${minute}` : `${time}:00`
}

/**
 * 26.02.2021 \ 8:00 -> 2021-02-26T08:00:00.0Z
 * @param {Date} date
 * @param {number} time - from HOURS
 */
export const isoConcat = (date, time, minutes) => {
  const d = new Date(date)
  d.setUTCHours(time)
  if (minutes) d.setUTCMinutes(minutes)
  d.setDate(d.getDate() + 1) // wtf?
  return d.toISOString()
}

/**
 * Форматирование даты ( Intl )
 * @param {Date} date
 * @param {Intl.DateTimeFormatOptions} options
 * @returns {string}
 */
export function formatDate(date, options = { year: 'numeric', month: 'long' }) {
  // Todo : change lang
  const formatter = Intl.DateTimeFormat('ru', options)
  return formatter.format(date)
}

/**
 * 2021-02-26T08:00:00.0Z -> { hour: 8, Date(26.02.2021) }
 * @param {string} iso
 * @returns {object}
 */
export const isoParse = (iso) => {
  const prepareDate = new Date(Date.parse(iso))
  const hour = prepareDate.getUTCHours()
  const minutes = prepareDate.getUTCMinutes()
  const date = new Date(
    prepareDate.getUTCFullYear(),
    prepareDate.getUTCMonth(),
    prepareDate.getUTCDate()
  )
  return {
    hour,
    minutes,
    date,
  }
}

/**
 *
 * @param {Date} date
 * @returns {string}
 */
export const toTitleDate = (date) => {
  if (date instanceof Date) {
    return formatDate(date, {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    })
  }
  return date
}

/**
 * 19.02.2006 -> 19 Февраля
 * @param {Date} date
 * @returns {string}
 */
export const monthLocaleDate = (date) => {
  if (date instanceof Date) {
    return formatDate(date, {
      day: '2-digit',
      month: 'long',
    })
  }
  return date
}

/**
 * Получить текущую неделю
 * @returns {{currentDate: Date, nextDate: Date}}
 */
export const getCurrentWeek = () => {
  const currentDate = normalizeDate(new Date())
  const nextDate = normalizeDate(new Date())
  nextDate.setDate(nextDate.getDate() + 5)
  return { currentDate, nextDate }
}

/**
 * Получить текущую неделю
 * @returns {{currentMonth: Date, nextMonth: Date}}
 */
export const getCurrentMonth = () => {
  const currentDate = normalizeDate(new Date())
  return {
    currentMonth: new Date(
      currentDate.getFullYear(),
      currentDate.getMonth(),
      1
    ),
    nextMonth: new Date(
      currentDate.getFullYear(),
      currentDate.getMonth() + 1,
      0
    ),
  }
}

// import moment from 'moment'
// export const getEveryWeekDay = (weekDay) => {
//   const startMonth = moment().startOf('month')
//   // if (startMonth.date() > 7) startMonth.add(7, 'd')
//   const month = startMonth.month()
//   const days = []
//   while (month === startMonth.month()) {
//     days.push(startMonth.day(weekDay).toISOString())
//     startMonth.add(1, 'week')
//   }
//   return days
// }
