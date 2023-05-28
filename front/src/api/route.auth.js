import { xfetch } from '~/core/fetch-system';
import { SERVER_ENDPOINT } from './_global';

/**
 * @param {string} username
 * @param {string} password
 */

export function get_token(email, password) {
  const makeFormData = () => {
    const user_data = {
      username: email,
      password: password,
    }

    const formBody = []
    for (let property in user_data) {
      let encodedKey = encodeURIComponent(property)
      let encodedValue = encodeURIComponent(user_data[property])
      formBody.push(encodedKey + '=' + encodedValue)
    }
    return formBody.join('&')
  }
  return xfetch.$post(`${SERVER_ENDPOINT}/user/get_token`, makeFormData(), {
    type: 'application/x-www-form-urlencoded;charset=UTF-8',
  }
  );
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
  fathers_name,
  inn,
  web_site,
  industry_id,
  country,
  city,
  position
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
      fathers_name,
      industry_id,
      country,
      city,
      position
    },
    { token: null }
  );
}
