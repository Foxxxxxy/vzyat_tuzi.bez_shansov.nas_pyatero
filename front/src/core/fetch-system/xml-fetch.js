/**
 * Старая версия fetch ( используется для отображения прогресса загрузки )
 * @param {string} token
 * @param {string} link
 * @param {FormData} form
 * @param {object} callbacks
 * @param {Function} callbacks.onReady - при выполненной загрузке на сервер
 * @param {Function} callbacks.onProgressTick - прогресс загрузки на сервер
 * @param {Function} callbacks.onStart - начало загрузки на сервер
 * @returns {FetchResponse<any>}
 */
export function XMLUpload(link, form, token = null, { onReady, onProgressTick, onStart } = {}) {
  const xml = new XMLHttpRequest()
  if (!onReady || !onStart) throw new Error('On Ready & On Start | callbacks is required!')

  xml.onreadystatechange = () => onReady(xml)
  xml.onloadstart = () => onStart(xml)
  xml.upload.addEventListener('progress', onProgressTick ?? (() => {}))
  xml.open('POST', link, true)

  xml.responseType = 'json'

  if (token) xml.setRequestHeader('Authorization', `Token ${token}`)

  xml.send(form)
}
