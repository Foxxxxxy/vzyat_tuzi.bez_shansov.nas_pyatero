import { xfetch } from '~/core/fetch-system';
import { SERVER_ENDPOINT } from './_global';

/**
 * @param {string} username
 * @param {string} surname
 */
export function get_token(formBody) {
  console.log(formBody);
  return xfetch.$post(`${SERVER_ENDPOINT}/auth/get_token`, formBody, {
    type: 'application/x-www-form-urlencoded;charset=UTF-8',
  });
}

/**
 * @param {string} username
 * @param {string} surname
 */
export function register({
  password,
  level,
  email,
  name,
  last_name,
  organisation_name,
  inn,
  web_site,
} = {}) {
  return xfetch.$post(
    `${SERVER_ENDPOINT}/user/sign_up`,
    {
      password,
      level,
      email,
      name,
      last_name,
      organisation_name,
      inn,
      web_site,
    },
    { token: null }
  );
}

/**
 * @param {string} username
 * @param {string} surname
 */
export function sign_in({
  password,
  email,
} = {}) {
  return xfetch.$post(
    `${SERVER_ENDPOINT}/user/sign_in`,
    {
      password,
      email,
    },
    { token: null }
  );
}
