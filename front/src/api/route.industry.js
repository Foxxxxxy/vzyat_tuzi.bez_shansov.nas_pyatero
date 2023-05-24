import { xfetch } from '~/core/fetch-system';
import { SERVER_ENDPOINT } from './_global';

/**
 * @param {string} username
 * @param {string} surname
 */
export function get_industry_suggestion(subtext, skip, limit) {
  return xfetch.$get(`${SERVER_ENDPOINT}/industry/suggestions?subtext=${subtext}&skip=${skip}&limit=${limit}`);
}
