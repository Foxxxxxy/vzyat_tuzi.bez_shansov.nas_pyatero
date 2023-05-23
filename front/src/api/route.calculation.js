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
  accounting_services_documents_amount
} = {}) {
  return xfetch.$post(
    `${SERVER_ENDPOINT}/calculation/create`,
    {
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
