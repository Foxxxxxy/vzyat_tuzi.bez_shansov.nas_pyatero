import { xfetch } from '~/core/fetch-system';
import { SERVER_ENDPOINT } from './_global';
import { download_file, changeFiles } from './route.common';

/**
 * @param {string} username
 * @param {string} surname
 */
export function get_district_suggestion(subtext, skip, limit) {
  return xfetch.$get(`${SERVER_ENDPOINT}/district/suggestions?subtext=${subtext}&skip=${skip}&limit=${limit}`);
}
