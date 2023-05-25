import { xfetch } from '~/core/fetch-system';
import { SERVER_ENDPOINT } from './_global';

/**
 * @param {string} username
 * @param {string} surname
 */
export function get_equipment_suggestion(subtext, skip, limit) {
  return xfetch.$get(`${SERVER_ENDPOINT}/equipment/suggestions?subtext=${subtext}&skip=${skip}&limit=${limit}`);
}

/**
 * @param {string} username
 * @param {string} surname
 */
export function get_equipments() {
  return xfetch.$get(`${SERVER_ENDPOINT}/equipment`);
}
