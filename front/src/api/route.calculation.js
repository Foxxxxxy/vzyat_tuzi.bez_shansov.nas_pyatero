import { xfetch } from '~/core/fetch-system';
import { SERVER_ENDPOINT } from './_global';

export function create_calculation({
  industry_id,
  subindustry_id,
  district_id,
  employee_amount,
  building_area_size,
  land_area_size,
  equipment,
  additional_services,
  legal_entity_type,
  predicted_income_per_year_rub,
  accounting_services_documents_amount,
  buildings
} = {}) {
  return xfetch.$post(
    `${SERVER_ENDPOINT}/calculation/create`,
    {
      buildings,
      industry_id,
      subindustry_id,
      district_id,
      employee_amount,
      building_area_size,
      land_area_size,
      equipment,
      additional_services,
      legal_entity_type,
      predicted_income_per_year_rub,
      accounting_services_documents_amount
    },
    { token: null }
  );
}

export function download_file(req_id, token) {
  let filename = ''
  const url = `${SERVER_ENDPOINT}/calculation/${req_id}/download-pdf`
  fetch(url, {
    headers: {
      Authorization: 'Bearer ' + token,
      Accept: '*/*',
      'Content-Type': 'application/json',
    },
    method: 'GET'
  })
    .then((res) => {
      return res.blob()
    })
    .then((blob) => {
      var url = window.URL.createObjectURL(blob)
      var a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a) // append the element to the dom
      a.click()
      a.remove() // afterwards, remove the element
      emit('submit')
    })
}

export function get_calculations({ token } = {}) {
  return xfetch.$get(`${SERVER_ENDPOINT}/calculation`, { token });
}
