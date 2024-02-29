from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder
from common_services.services.survey_service import frequency_value_calculation
from common_services.services.outlet_service import get_outlet_detail_by_site_id
import boto3

db_instance = CreateDBConnection()
log = Log().get_logger_service("Station master command deletenotification")

# Create client for parameter store and s3
ssm_client = boto3.client('ssm', region_name='ca-central-1')


def modify_response(data, language):
    modified_result = []
    for i in data:
        result_dict = {
            "kent_id": i.kent_id,
            "brand_marketer": i.brand_marketer,
            "address": i.address,
            "product_id": i.product_id,
            "product_description": i.product_description,
            "frequency_code": i.frequency_code,
            "frequency_values": frequency_value_calculation(i.frequency_code, language),
            "sort_order": i.sort_order,
            "json_time_list": i.json_time,
            "effective_date": i.effective_date,
            "expiry_date": i.expiry_date,
            "status": i.status,
            "is_competitor_active": i.is_competitor_active,
            "is_frequency_update": i.is_frequency_update

        }
        modified_result.append(result_dict)
    return modified_result


def get_survey_schedule_detail_by_site_id(site_id, request_date, competitor_status, include_rows, language):
    """
        This function is used to get the survey schedule details for given sites it
    """
    try:
        log.append_keys(service_function="get_survey_schedule_detail_by_site_id")
        log.debug("Entered into get_survey_schedule_detail_by_site_id service")
        with db_instance.create_writer_connection() as db:
            get_survey_schedule_detail_by_site_id_function_name = "dbo.fn_survey_schedule_detail_by_site_id"
            param_dict = {"site_id": site_id, "lang": language, "request_date": request_date,
                          "competitor_status": competitor_status,
                          "include_rows": include_rows}
            query = text(
                'SELECT * FROM '
                + get_survey_schedule_detail_by_site_id_function_name + '(:site_id,CAST(:lang AS character varying),'
                                                                        ':request_date,:competitor_status,'
                                                                        ':include_rows)')
            data = call_postgres_function(query=query, db=db, parameters=param_dict)
        log.debug("Received response from database")
        response_data = modify_response(data, language)
        response = {
            "status_code": 200,
            "message": "Received frequency schedule data from database successfully",
            "data": {"survey_schedule_list": response_data}
        }
    except Exception as e:
        raise e
    else:
        log.debug("get_survey_schedule_detail_by_site_id service executed successfully")
        return jsonable_encoder(response)


def get_survey_schedule_mail_header(site_id: int, language: str, user_id: str):
    """
    Get site survey schedule mail header text
    """
    try:
        if language == 'EN':
            subject = 'UPDATE: ' + str(site_id) + ' PRICE SURVEY SCHEDULE'
            body = ('Attached you will find a schedule of competitor price surveys your station is expected to '
                    'complete.<br>As you know, competitor price survey are the single most important piece of '
                    'information that Parkland receives daily, and as such, we thank you for your focus in this '
                    'area.<br><br>Please contact your Territory Manager or the Price Desk if you have any '
                    'questions.<br><br>Thanks')
            note1 = ('Those sites with a separate weekend schedule should also follow this weekend schedule on '
                     'statutory holidays')
            note2 = 'Competitors located directly across the street should be surveyed every hour'
            file_name = 'PriceSurveySchedule'

        else:
            subject = 'MISE-A-JOUR: ' + str(site_id) + ' CALENDRIER SONDAGE DE PRIX'
            body = ('Vous trouverez ci-joint un calendrier de sondage sur les prix des concurrents que votre station '
                    'devrait compléter.<br> Comme vous le savez, les sondages sur les prix des concurrents sont les '
                    'informations les plus importantes que Parkland reçoit quotidiennement, et à ce titre, '
                    'nous vous remercions de votre concentration dans ce domaine.<br><br>Veuillez contacter votre '
                    'responsable de territoire ou le bureau des prix si vous avez des questions.<br><br> Merci')
            note1 = ('Les sites avec un horaire de fin de semaine différents devraient également suivre cet horaire '
                     'de fin de semaine les jours fériés')
            note2 = ('Les concurrents situés directement de l’autre côté de la rue doivent produire un sondage '
                     'toutes les heures')
            file_name = 'CalendrierSondagePrix'

        get_outlet_detail_by_site_id_data = get_outlet_detail_by_site_id(site_id, language, user_id)

        if not get_outlet_detail_by_site_id_data:
            response = {
                "status_code": 204,
                "message": "Data not found in database",
                "data": None
            }
        else:
            get_outlet_detail_by_site_id_data_response = get_outlet_detail_by_site_id_data
            site_name = get_outlet_detail_by_site_id_data_response['name']
            site_no = get_outlet_detail_by_site_id_data_response['site_no']
            brand_name = get_outlet_detail_by_site_id_data_response['brand']
            address = get_outlet_detail_by_site_id_data_response['address']
            station_email = get_outlet_detail_by_site_id_data_response['station_email']
            territory_manager_email = get_outlet_detail_by_site_id_data_response['territory_manager_email']
            pricing_team_survey_email = \
                ssm_client.get_parameter(Name='/pic/pdf/survey/pricing_team_survey_email')['Parameter']['Value']

            output = {
                'subject': subject,
                'body': body,
                'note1': note1,
                'note2': note2,
                'file_name': file_name,
                'site_name': site_name,
                'site_no': site_no,
                'brand_name': brand_name,
                'address': address,
                'station_email': station_email,
                'territory_manager_email': territory_manager_email,
                'pricing_team_survey_email': pricing_team_survey_email
            }

            response_data = jsonable_encoder(output)
            response = {
                "status_code": 200,
                "message": "Received marketers data from Database successfully",
                "data": {"survey_schedule_mail_header": response_data}
            }

    except Exception as exc:
        raise exc
    else:
        log.debug("get_survey_schedule_mail_header service executed successfully")
        return response
