import { xfetch } from '~/core/fetch-system';
import { SERVER_ENDPOINT } from './_global';
import { download_file, changeFiles } from './route.common';

/**
 * @param {string} username
 * @param {string} surname
 */
export function get_additional_suggestion(subtext, skip, limit) {
  return xfetch.$get(`${SERVER_ENDPOINT}/additional-service/suggestions?subtext=${subtext}&skip=${skip}&limit=${limit}`);
}

export function get_additionals() {
  return xfetch.$get(`${SERVER_ENDPOINT}/additional-service`);
}

export function get_current_additional(id) {
  return xfetch.$get(`${SERVER_ENDPOINT}/additional-service/${id}`);
}

export function edit_current_additional(
  id,
  { name, average_price_dollar } = {},
  token
) {
  return xfetch.$put(`${SERVER_ENDPOINT}/additional-service/${id}`, {
    name,
    average_price_dollar,
  }, { token });
}

export function add_new_additional({ name, average_price_dollar } = {}, token) {
  return xfetch.$post(
    `${SERVER_ENDPOINT}/additional-service`,
    {
      name,
      average_price_dollar,
    },
    { token }
  );
}

export function delete_additional(id, token) {
  return xfetch.$delete(`${SERVER_ENDPOINT}/additional-service/${id}`, null, { token });
}

export function get_xlsx_template(token) {
  return new Promise((resolve, reject) => {
    const url = `${SERVER_ENDPOINT}/additional-service/excel-template`
    download_file(url, token, (status) => resolve(status))
  })
}

export async function send_glsx_template(e, token) {
  const url = `${SERVER_ENDPOINT}/additional-service/excel`
  return changeFiles(url, e, token)
}
