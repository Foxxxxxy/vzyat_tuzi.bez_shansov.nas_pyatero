import { xfetch } from '~/core/fetch-system';
import { SERVER_ENDPOINT } from './_global';

/**
 * @param {string} username
 * @param {string} surname
 */
export function get_user_info(token) {
  return xfetch.$get(`${SERVER_ENDPOINT}/user/me`, { token });
}

export function get_users() {
  return xfetch.$get(`${SERVER_ENDPOINT}/user`);
}

export function get_current_user(id) {
  return xfetch.$get(`${SERVER_ENDPOINT}/user/${id}`);
}
