from sqlalchemy import text
import json
from common_component.src.core.helpers.encoder import jsonable_encoder
from outlet_schema import UpdateSite
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

db_instance = CreateDBConnection()
log = Log().get_logger_service()

def update_site(outlet: UpdateSite):
    """This function is to update site"""
    try:
        log.append_keys(service_function="update_site")
        log.debug("Entered into update_site service")
        with db_instance.create_writer_connection() as db:
            update_outlet_procedure_name = 'dbo.sp_site_update'
            param_dict = {
                "_SiteNo": outlet.site_no,
                "_AlternateSiteNo": outlet.alternative_site_no,
                "_Name": outlet.name,
                "_Retailer_name": outlet.retailer_name,
                "_BrandId": outlet.brand_id,
                "_Address": outlet.address,
                "_CrossStreet": outlet.cross_street,
                "_CityId": outlet.city_id,
                "_FacilityTypeId": outlet.facility_type_id,
                "_StatusId": outlet.status_id,
                "_LanguageId": outlet.language_id,
                "_TimeZoneId": outlet.timezone_id,
                "_TerritoryManagerId": outlet.territory_manager_id,
                "_HierarchyId": outlet.hierarchy_id,
                "_Pin": outlet.pin,
                "_IsRegieEnergy": outlet.is_regie_energy,
                "_IsDailyResetApplicable": outlet.is_daily_reset_applicable,
                "_ResetTime": outlet.reset_time,
                "_ResetNextDay": outlet.reset_next_day,
                "_PumpConfigurationTemplate": outlet.pump_configuration_template,
                "_Latitude": outlet.latitude,
                "_Longitude": outlet.longitude,
                "_RadiusForTableau": outlet.radius_for_tableau,
                "_UserId": outlet.user_id,
                "_SurveySubmissionCount": outlet.survey_submission_count,
                "_ConfidenceScore": outlet.confidence_score,
                "_AutoClearStartTime": outlet.auto_clear_start_time,
                "_AutoClearEndTime": outlet.auto_clear_end_time,
                "_IsGasBuddyActive": outlet.is_gas_buddy_active,
                "_TacticRegularPricingZoneId": outlet.tactic_regular_pricing_zoneId,
                "_TacticRegularPriceDifferential": outlet.tactic_regular_price_differential,
                "_TacticDieselPricingZoneId": outlet.tactic_diesel_pricing_zone_id,
                "_TacticDieselPriceDifferential": outlet.tactic_diesel_price_differential,
                "_IsRounding9": outlet.is_rounding_9,
                "_IsRounding0": outlet.is_rounding_0,
                "_RackFwdMissingTime": outlet.rack_fwd_missing_time,
                "_RackFwdMissingTimeActive": outlet.rack_fwd_missing_time_active,
                "_Effective_date": outlet.effective_date,
                "_Expiry_date": outlet.expiry_date
            }
            query = text(
                'call ' + update_outlet_procedure_name + '(:_SiteNo,'
                                                         ' CAST(:_AlternateSiteNo AS character varying), '
                                                         'CAST(:_Name AS character varying), CAST(:_Retailer_name AS '
                                                         'character varying), :_BrandId , CAST(:_Address AS character '
                                                         'varying), CAST(:_CrossStreet AS character varying), '
                                                         ':_CityId, :_FacilityTypeId , :_StatusId, :_LanguageId, '
                                                         ':_TimeZoneId, :_TerritoryManagerId, :_HierarchyId, '
                                                         'CAST(:_Pin AS character varying), CAST(:_IsRegieEnergy AS '
                                                         'numeric),'
                                                         'CAST(:_IsDailyResetApplicable AS numeric), CAST(:_ResetTime '
                                                         'AS character varying), CAST(:_ResetNextDay AS numeric), '
                                                         ':_PumpConfigurationTemplate, '
                                                         'CAST(:_Latitude AS decimal), CAST(:_Longitude AS decimal), '
                                                         ':_RadiusForTableau , CAST(:_UserId AS character varying), '
                                                         ':_SurveySubmissionCount, CAST(:_ConfidenceScore AS '
                                                         'decimal), CAST(:_AutoClearStartTime AS character varying) , '
                                                         'CAST(:_AutoClearEndTime AS character varying), '
                                                         'CAST(:_IsGasBuddyActive AS numeric), '
                                                         ':_TacticRegularPricingZoneId,'
                                                         'CAST(:_TacticRegularPriceDifferential AS decimal),'
                                                         ':_TacticDieselPricingZoneId,'
                                                         'CAST(:_TacticDieselPriceDifferential AS decimal), '
                                                         'CAST(:_IsRounding9 AS numeric), CAST(:_IsRounding0 AS '
                                                         'numeric), CAST(:_RackFwdMissingTime AS character varying), '
                                                         'CAST(:_RackFwdMissingTimeActive AS numeric),'
                                                         ':_Effective_date,:_Expiry_date)')

            call_postgres_function(query=query, parameters=param_dict, db=db)

        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Updated outlet in Database successfully",
            "data": {}
        }
    
    except SQLAlchemyError as sql_alchemy_exception:
        raise sql_alchemy_exception

    except Exception as e:
        error_message = f"An error occurred while executing the query: {str(e)}"
        raise e
    else:
        log.debug("update_site service executed successfully")
        return jsonable_encoder(response)