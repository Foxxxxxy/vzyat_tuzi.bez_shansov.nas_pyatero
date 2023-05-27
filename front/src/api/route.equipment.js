import { xfetch } from '~/core/fetch-system';
import { SERVER_ENDPOINT } from './_global';
import { download_file, changeFiles } from './route.common';

/**
 * @param {string} username
 * @param {string} surname
 */
export function get_equipment_suggestion(subtext, skip, limit) {
  return xfetch.$get(
    `${SERVER_ENDPOINT}/equipment/suggestions?subtext=${subtext}&skip=${skip}&limit=${limit}`
  );
}

export function get_equipments() {
  return xfetch.$get(`${SERVER_ENDPOINT}/equipment`);
}

export function get_current_equipment(id) {
  return xfetch.$get(`${SERVER_ENDPOINT}/equipment/${id}`);
}

export function edit_current_equipment(
  id,
  { name, average_price_dollar } = {},
  token
) {
  return xfetch.$put(`${SERVER_ENDPOINT}/equipment/${id}`, {
    name,
    average_price_dollar,
  }, { token });
}

export function add_new_equipment({ name, average_price_dollar } = {}, token) {
  return xfetch.$post(
    `${SERVER_ENDPOINT}/equipment`,
    {
      name,
      average_price_dollar,
    },
    { token }
  );
}

export function delete_equipment(id, token) {
  return xfetch.$delete(`${SERVER_ENDPOINT}/equipment/${id}`, null, { token });
}

export function get_xlsx_template(token) {
  return new Promise((resolve, reject) => {
    const url = `${SERVER_ENDPOINT}/equipment/excel-template`
    download_file(url, token, (status) => resolve(status))
  })
}

export async function send_glsx_template(e, token) {
  const url = `${SERVER_ENDPOINT}/equipment/excel`
  return changeFiles(url, e, token)
}
