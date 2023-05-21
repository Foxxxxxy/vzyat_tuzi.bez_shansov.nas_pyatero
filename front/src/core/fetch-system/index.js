/**
 * @typedef xfetchOptions
 * @property {string} path - путь до рута
 * @property {any} body - тело запроса ( автоматически сериализуется в JSON )
 * @property {('POST'|'GET')} method - метод запроса
 * @property {HeadersInit} headers - заголовки
 * @property {...any} args
 */

async function $fetch({ path, body, method, headers, type, is_file }, ...args) {
  try {
    const f = await fetch(path, {
      body:
        type === 'application/json;charset=utf-8' ? JSON.stringify(body) : body,
      method,
      headers: {
        'Content-Type': type,
        ...headers,
      },
      ...args,
    })
    if (!f.ok) return null
    if (!is_file) {
      const parsed = await f.json()
      parsed.status = f.status
      return parsed
    }
    return f
  } catch (e) {
    console.log('[FETCH ERROR]', e)
    return {
      status: 400,
    }
  }
}

export class xfetch {
  /**
   * Базовая функция
   * @param {xfetchOptions} options
   * @static
   */
  static #setHeader(headers, key, value, toSet) {
    if (value) headers[key] = toSet
  }

  static #with_body(
    path,
    body,
    { token, type = 'application/json;charset=utf-8', is_file = false } = {},
    method = 'POST'
  ) {
    const headers = {}
    xfetch.#setHeader(headers, 'Authorization', token, `Bearer ${token}`)
    return $fetch({
      path,
      method,
      body,
      headers,
      type,
      is_file,
    })
  }

  static $get(path, { token } = {}) {
    const headers = {}
    xfetch.#setHeader(headers, 'Authorization', token, `Bearer ${token}`)
    return $fetch({ path, method: 'GET', headers })
  }

  static $post(path, body, { token, type, is_file } = {}) {
    return this.#with_body(path, body, { token, type, is_file }, 'POST')
  }

  static $put(path, body, { token } = {}) {
    return this.#with_body(path, body, { token }, 'PUT')
  }

  static $delete(path, body, { token } = {}) {
    return this.#with_body(path, body, { token }, 'DELETE')
  }

  static $patch(path, body, { token } = {}) {
    return this.#with_body(path, body, { token }, 'PATCH')
  }
}
