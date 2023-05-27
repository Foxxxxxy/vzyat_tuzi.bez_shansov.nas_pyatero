import { xfetch } from '~/core/fetch-system';
import { SERVER_ENDPOINT } from './_global';

/**
 * @param {string} username
 * @param {string} surname
 */
export function get_user_info(token) {
  return xfetch.$get(`${SERVER_ENDPOINT}/user/me`, { token });
}

export function get_users({ token } = {}) {
  return xfetch.$get(`${SERVER_ENDPOINT}/user`, { token });
}

export function get_user_review(id, { token } = {}) {
  return xfetch.$get(`${SERVER_ENDPOINT}/user/${id}/requests`, { token });
}

export function get_current_user(id, { token } = {}) {
  return xfetch.$get(`${SERVER_ENDPOINT}/user/${id}`, { token });
}

export function edit_current_user(
  id,
  { email, name, last_name, organisation_name, inn, web_site } = {},
  token
) {
  return xfetch.$patch(
    `${SERVER_ENDPOINT}/user/${id}`,
    {
      email,
      name,
      last_name,
      organisation_name,
      inn,
      web_site,
    },
    { token }
  );
}
