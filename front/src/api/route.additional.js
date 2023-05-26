import { xfetch } from '~/core/fetch-system';
import { SERVER_ENDPOINT } from './_global';

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
