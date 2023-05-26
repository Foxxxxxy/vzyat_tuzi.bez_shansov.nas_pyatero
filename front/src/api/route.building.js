import { xfetch } from '~/core/fetch-system';
import { SERVER_ENDPOINT } from './_global';

/**
 * @param {string} username
 * @param {string} surname
 */
export function get_building_suggestion(subtext, skip, limit) {
  return xfetch.$get(`${SERVER_ENDPOINT}/building/suggestions?subtext=${subtext}&skip=${skip}&limit=${limit}`);
}

export function get_buildings() {
  return xfetch.$get(`${SERVER_ENDPOINT}/building`);
}

export function get_current_building(id) {
  return xfetch.$get(`${SERVER_ENDPOINT}/building/${id}`);
}

export function edit_current_building(
  id,
  { name, average_price_rub } = {},
  token
) {
  return xfetch.$put(`${SERVER_ENDPOINT}/building/${id}`, {
    name,
    average_price_rub,
  }, { token });
}

export function add_new_building({ name, average_price_rub } = {}, token) {
  return xfetch.$post(
    `${SERVER_ENDPOINT}/building`,
    {
      name,
      average_price_rub,
    },
    { token }
  );
}

export function delete_building(id, token) {
  return xfetch.$delete(`${SERVER_ENDPOINT}/building/${id}`, null, { token });
}
