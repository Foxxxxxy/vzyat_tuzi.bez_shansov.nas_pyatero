import { xfetch } from '~/core/fetch-system';
import { SERVER_ENDPOINT } from './_global';
import { download_file } from './route.common';

export function create_calculation({
  industry_id,
  district_id,
  employee_amount,
  building_area_size,
  land_area_size,
  equipment,
  additional_services,
  legal_entity_type,
  predicted_income_per_year_rub,
  accounting_services_documents_amount,
  buildings,
  additional_needs
} = {}, { token } = {}) {
  return xfetch.$post(
    `${SERVER_ENDPOINT}/calculation/create`,
    {
      buildings,
      industry_id,
      district_id,
      employee_amount,
      building_area_size,
      land_area_size,
      equipment,
      additional_services,
      legal_entity_type,
      predicted_income_per_year_rub,
      accounting_services_documents_amount,
      additional_needs
    },
    { token: token }
  );
}

export function download_pdf(req_id, token) {
  return new Promise((resolve, reject) => {
    const url = `${SERVER_ENDPOINT}/calculation/${req_id}/download-pdf`
    download_file(url, token, (status) => resolve(status))
  })
}

export function download_detailed_pdf(req_id, token) {
  return new Promise((resolve, reject) => {
    const url = `${SERVER_ENDPOINT}/calculation/${req_id}/download-zip`
    download_file(url, token, (status) => resolve(status))
  })
}

export function get_calculations({ token } = {}) {
  return xfetch.$get(`${SERVER_ENDPOINT}/calculation`, { token });
}

export function get_calculation_preview(id, token) {
  return xfetch.$get(`${SERVER_ENDPOINT}/calculation/${id}/preview`, { token });
}
