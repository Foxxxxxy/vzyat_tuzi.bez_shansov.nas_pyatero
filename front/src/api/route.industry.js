import { xfetch } from '~/core/fetch-system';
import { SERVER_ENDPOINT } from './_global';
import { download_file, changeFiles } from './route.common';

/**
 * @param {string} username
 * @param {string} surname
 */
export function get_industry_suggestion(subtext, skip, limit) {
  return xfetch.$get(`${SERVER_ENDPOINT}/industry/suggestions?subtext=${subtext}&skip=${skip}&limit=${limit}`);
}

export function get_industrys() {
  return xfetch.$get(`${SERVER_ENDPOINT}/industry`);
}

export function get_current_industry(id) {
  return xfetch.$get(`${SERVER_ENDPOINT}/industry/${id}`);
}

export function edit_current_industry(
  id,
  { name, average_price_rub } = {},
  token
) {
  return xfetch.$put(`${SERVER_ENDPOINT}/industry/${id}`, {
    name,
    average_price_rub,
  }, { token });
}

export function add_new_industry({ name, average_price_rub } = {}, token) {
  return xfetch.$post(
    `${SERVER_ENDPOINT}/industry`,
    {
      name,
      average_price_rub,
    },
    { token }
  );
}

export function delete_industry(id, token) {
  return xfetch.$delete(`${SERVER_ENDPOINT}/industry/${id}`, null, { token });
}

export function get_xlsx_template(token) {
  return new Promise((resolve, reject) => {
    const url = `${SERVER_ENDPOINT}/industry/excel-template`
    download_file(url, token, (status) => resolve(status))
  })
}

export async function send_glsx_template(e, token) {
  const url = `${SERVER_ENDPOINT}/industry/excel`
  return changeFiles(url, e, token)
}
